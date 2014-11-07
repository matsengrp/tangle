from collections import OrderedDict
from sage.all import gap
# Depends on curvature/tree-fun.py

gap.eval("""
Read("tangle-fun.gap");
""")


# Groups and cosets

def size(domain):
    return gap.function_call('Size', domain)


def as_list(domain):
    return gap.function_call('AsList', domain)


def inverse(group_elt):
    return gap.function_call('Inverse', group_elt)


def double_coset(U, g, V):
    return gap.function_call('DoubleCoset', [gap(U), gap(g), gap(V)])


def representative(coset):
    return gap.function_call('Representative', coset)


def left_acting_group(coset):
    return gap.function_call('LeftActingGroup', coset)


def right_acting_group(coset):
    return gap.function_call('RightActingGroup', coset)


# Described in SAGE manual, but not yet implemented?
def orbit(G, x, action):
    return gap.function_call('Orbit', [G, x, action])


def stabilizer(G, x, action):
    return gap.function_call('Stabilizer', [G, x, action])



def double_coset_as_list(coset):
    """
    Turn a double coset into a list of its elements.
    AsList is not defined for them in GAP because they don't have a canonical
    order.
    """
    s = set()
    for l in as_list(left_acting_group(coset)):
        for r in as_list(right_acting_group(coset)):
            s.add(l * representative(coset) * r)
    return list(s)


def double_cosets(G, U, V):
    return gap.function_call('DoubleCosets', [gap(G), gap(U), gap(V)])


def as_set(l):
    return gap.function_call('AsSet', l)


def right_on_double_cosets(coset, g):
    """
    Act on a double coset. Note that this does not always give a well-defined
    group action. The double coset UaV is by definition the same as UavV,
    although UagV need not be the same as UavgV.
    """
    return gap.function_call('RightOnDoubleCosets', [coset, gap(g)])


def conjugation_on_double_cosets(coset, g):
    """
    Act on a double coset via conjugation.
    """
    return gap.function_call('ConjugationOnDoubleCosets', [coset, gap(g)])


def double_coset_inverse(coset):
    """
    Given UgV returns Vg^{-1}U.
    """
    return gap.function_call('DoubleCosetInverse', coset)


def inverse_unique_double_cosets(G, U):
    """
    This function returns a list of double cosets of the form UgU in G that are
    unique under inversion. That is, a complete list of such double cosets
    where we consider UgU and Ug^{-1}U to be the same.
    """
    return gap.function_call('InverseUniqueDoubleCosets', [gap(G), gap(U)])


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


def graph_of_tangle(t1, t2, coset, symmetric=True):
    """
    Symmetric determines if we want to add a feature to t2 to differentiate it
    from t1.
    """
    mu_d = symmetric_group_dict(t1, t2, representative(coset))
    if symmetric:
        g = t1.disjoint_union(t2)
    else:
        # By duplicating root edge we can distinguish between t1 and t2.
        g = t1.disjoint_union(duplicate_zero_edge(t2))
    for i in range(1, n_leaves(t1)):
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


def make_tangles_extras(n, symmetric=True):
    """
    Make all the tangles with n leaves, along with the number of labeled
    tangles isomorphic to that tangle, and the indices of the mu = id version
    of those trees in enumerate_rooted_trees.
    symmetric determines if we should consider all ordered or unordered pairs
    of trees.
    """
    fS = SymmetricGroup(n)
    order_fS = order(fS)

    trees = enumerate_rooted_trees(n)
    # So that we can recognize trees after acting on t2 by mu^{-1}.
    # `d_trees` is a dictionary keyed on Newick strings to their index.
    d_trees = OrderedDict((to_newick(trees[i]), i) for i in range(len(trees)))
    shapes = []
    # `d_shapes` is a map from Newick shape strings to their indices.
    d_shapes = OrderedDict()
    for i in range(len(trees)):
        shape_i = to_newick_shape(trees[i])
        if shape_i in d_shapes:
            d_shapes[shape_i] = d_shapes[shape_i] + [i]
        else:
            shapes.append(trees[i])
            d_shapes[shape_i] = [i]
    shape_autos = [leaf_autom_group(s) for s in shapes]
    newick_shapes = d_shapes.keys()
    # Iterate over all pairs of tree shape representatives.
    tangles = []
    for i in range(len(shapes)):
        print "Tree {} of {}".format(i+1, len(shapes))
        for j in range(0, len(shapes)):
            total_n_labelings = 0
            if symmetric and i > j:
                # If symmetric we only have to generate unordered pairs of
                # representatives.
                continue
            elif symmetric and i == j:
                # If symmetric and we have identical tree shapes, then we can
                # rotate the trees around, "inverting" the coset.
                cosets = inverse_unique_double_cosets(fS, shape_autos[i])
            else:
                # Enumerate all double cosets.
                cosets = double_cosets(fS, shape_autos[i], shape_autos[j])
            for c in cosets:
                tangle = (shapes[i], shapes[j], c)
                (s_t1, s_t2p) = to_newick_pair(*tangle).split("\t")
                A1 = shape_autos[i]  # Automorphisms of t1.
                A2 = shape_autos[j]  # Automorphisms of t2.
                coset_size = size(c)
                n_planar_ordered_labelings = order_fS * coset_size
                if symmetric and i == j:
                    if fS.identity() in c:
                        print "identity", order_fS, "before", n_planar_ordered_labelings
                        # Artificially "double" the identity tangles:
                        n_planar_ordered_labelings_with_repetition = n_planar_ordered_labelings + order_fS
                        print "wr", n_planar_ordered_labelings_with_repetition
                    elif not inverse(representative(c)) in c:
                        # We have enumerated inverse-unique double cosets, so
                        # if we are interested in counting all elements in a
                        # double coset then we need to double here.
                        # This is mutually exclusive with the above because if
                        # the identity is in a coset then it must have some
                        # overlap with its inverse, and thus must be identical
                        # to its inverse.
                        print "also inverse so double", n_planar_ordered_labelings
                        n_planar_ordered_labelings_with_repetition = 2*n_planar_ordered_labelings
                    else:
                        n_planar_ordered_labelings_with_repetition = n_planar_ordered_labelings
                    # With that, we have doubles of everything:
                    n_planar_labelings = n_planar_ordered_labelings_with_repetition/2
                else:
                    # We don't have to worry the symmetry of exchanging t1 and t2.
                    n_planar_labelings = n_planar_ordered_labelings / 2
                n_labelings = n_planar_labelings / (order(A1) * order(A2))
                print ">>> "+to_newick_pair(*tangle)
                print(c)
                print n_labelings
                total_n_labelings += n_labelings
                tangles.append((tangle, d_trees[s_t1], d_trees[s_t2p],
                               n_labelings))
            print "tot", total_n_labelings
            if symmetric and i == j:
                # d_shapes_values()[i] is the number of phylogenetic trees with
                # shape i. Recall that binomial(q+1, 2) gives the number of
                # unordered pairs of q items allowing repetition.
                print "eqn", binomial(len(d_shapes.values()[i])+1, 2)
            else:
                assert(True)
                # assert(
                #     total_n_labelings ==
                #     len(d_shapes.values()[i])*len(d_shapes.values()[j]))
            print ""
    return tangles
