from collections import OrderedDict
from sage.all import gap
# Depends on curvature/tree-fun.py

# Groups and cosets

def size(domain):
    return gap.function_call('Size', domain)


def as_list(domain):
    return gap.function_call('AsList', domain)


def inverse(group_elt):
    return gap.function_call('Inverse', group_elt)


# Group action on double cosets.
# Note that this is not always a well defined group action as described below.
gap.eval("""
OnDoubleCosets := function(coset, g)
      return DoubleCoset(LeftActingGroup(coset),
               OnRight(Representative(coset), g),
               RightActingGroup(coset));;
end
""")


# Given UgV returns Vg^{-1}U.
gap.eval("""
DoubleCosetInverse := function(coset)
      return DoubleCoset(RightActingGroup(coset),
               Inverse(Representative(coset)),
               LeftActingGroup(coset));;
end
""")


def double_coset(U, g, V):
    return gap.function_call('DoubleCoset', [gap(U), gap(g), gap(V)])


def representative(coset):
    return gap.function_call('Representative', coset)


def left_acting_group(coset):
    return gap.function_call('LeftActingGroup', coset)


def right_acting_group(coset):
    return gap.function_call('RightActingGroup', coset)


def double_coset_as_list(coset):
    """
    Turn a double coset into a list of its elements.
    Apparently AsList is not defined for them in GAP.
    """
    s = set()
    for l in as_list(left_acting_group(coset)):
        for r in as_list(right_acting_group(coset)):
            s.add(l * representative(coset) * r)
    return list(s)


def double_cosets(G, U, V):
    return gap.function_call('DoubleCosets', [gap(G), gap(U), gap(V)])


def on_double_cosets(coset, g):
    """
    Act on a double coset. Note that this does not always give a well-defined
    group action. The double coset UaV is by definition the same as UavV,
    although UagV need not be the same as UavgV.
    """
    return gap.function_call('OnDoubleCosets', [coset, gap(g)])


def double_coset_inverse(coset):
    """
    Given UgV returns Vg^{-1}U.
    """
    return gap.function_call('DoubleCosetInverse', coset)


def shortest_fewest_cycles_sorted(perm_list):
    """
    Sort first by the number of cycles, then by the length of those cycles.
    """
    l = list(perm_list)
    l.sort(key=lambda x: len(x.cycles()))

    def my_max(lp):
        if lp == []:
            return 0
        else:
            return max(lp)

    # Sort according to the maximum length of any cycle in the permutation.
    l.sort(key=lambda x: my_max(list(len(c) for c in x.cycle_tuples())))
    return l


# Tangles

def symmetric_group_dict(t1, t2, mu):
    n = n_leaves(t1) - 1
    assert(n == n_leaves(t2) - 1)
    return SymmetricGroup(n)(mu).dict()


def graph_of_tangle(t1, t2, coset):
    n = n_leaves(t1) - 1
    mu_d = symmetric_group_dict(t1, t2, representative(coset))
    g = t1.disjoint_union(duplicate_zero_edge(t2))
    for i in range(1, n+1):
        g.add_edge((0, i), (1, mu_d[i]), True)
    return g


def print_tangle(t1, t2, coset):
    print to_newick(t1)
    print to_newick(t2)
    print coset


def _to_newick_pair(t1, t2, mu):
    t2p = t2.copy()
    # Need inverse below because we are relabeling t2's labels in order that
    # they will line up with t1's.
    t2p.relabel(symmetric_group_dict(t1, t2, inverse(mu)))
    return "{}\t{}".format(to_newick(t1), to_newick(t2p))


def to_newick_pair(t1, t2, coset):
    return _to_newick_pair(t1, t2, representative(coset))


def to_newick_pairs(t1, t2, coset):
    """
    Make a list of all Newick pairs corresponding to that coset.
    """
    return [_to_newick_pair(t1, t2, mu) for mu in double_coset_as_list(coset)]


def saveable_tangle(t1, t2, coset):
    return (t1, t2, str(coset))


def reanimate_tangle(t1, t2, coset_str):
    return (t1, t2, gap(coset_str))


def load_tangles(fname):
    return list(reanimate_tangle(*x) for x in load(fname))


def make_tangles_extras(n, symmetric=True, verbose=True):
    """
    Make all the tangles with n leaves, along with the number of labeled
    tangles isomorphic to that tangle, and the indices of the mu = id version
    of those trees in enumerate_rooted_trees.
    symmetric determines if we should consider all ordered or unordered pairs
    of trees.
    """
    fS = SymmetricGroup(n)

    trees = enumerate_rooted_trees(n)
    # So that we can recognize trees after acting on t2 by mu^{-1}.
    # `dn` is short for a dictionary keyed on Newick strings.
    dn_trees = {to_newick(trees[i]): i for i in range(len(trees))}
    shapes = []
    dn_shapes = OrderedDict()
    for i in range(len(trees)):
        shape_i = to_newick_shape(trees[i])
        if shape_i in dn_shapes:
            dn_shapes[shape_i] = dn_shapes[shape_i] + [i]
        else:
            shapes.append(trees[i])
            dn_shapes[shape_i] = [i]
    shape_autos = [leaf_autom_group(s) for s in shapes]
    newick_shapes = dn_shapes.keys()
    # Iterate over all pairs of tree shape representatives.
    tangles = []
    for i in range(len(shapes)):
        n_with_same_shape = len(dn_shapes[newick_shapes[i]])
        print "Tree {} of {}".format(i+1, len(shapes))
        for j in range(0, len(shapes)):
            if symmetric and i > j:
                # If symmetric we only have to check unordered pairs of
                # representatives.
                continue
            cosets = double_cosets(fS, shape_autos[i], shape_autos[j])
            if verbose:
                print newick_shapes[i]
                print newick_shapes[j]
                print cosets
                print ""
            # If symmetric and we have identical tree shapes, then we can
            # rotate the trees around, "inverting" the coset.
            if symmetric and i == j:
                deduped = []
                for c in cosets:
                    if double_coset_inverse(c) not in deduped:
                        deduped.append(c)
                cosets = deduped
            for c in cosets:
                tangle = (shapes[i], shapes[j], c)
                (s_t1, s_t2p) = to_newick_pair(*tangle).split("\t")
                tangles.append((tangle, dn_trees[s_t1], dn_trees[s_t2p],
                               n_with_same_shape))
    return tangles
