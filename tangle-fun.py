from collections import OrderedDict
import os
import sage.all as sg
# Depends on all-hail-sage/phylogeny.py

wd = os.path.dirname(os.path.realpath(__file__));
gap.eval("""
Read("{}/tangle-fun.g");
""".format(wd))


# Groups and cosets

def size(domain):
    return gap.function_call('Size', domain)


def as_list(domain):
    return gap.function_call('AsList', domain)


def inverse(group_elt):
    return gap.function_call('Inverse', group_elt)


def generators_of_group(G):
    return gap.function_call('GeneratorsOfGroup', G)


def right_coset(U, g):
    return gap.function_call('RightCoset', [gap(U), gap(g)])


def right_cosets(G, U):
    return gap.function_call('RightCosets', [gap(G), gap(U)])


def double_coset(U, g, V):
    return gap.function_call('DoubleCoset', [gap(U), gap(g), gap(V)])


def representative(coset):
    return gap.function_call('Representative', coset)


def acting_domain(coset):
    return gap.function_call('ActingDomain', coset)


def left_acting_group(coset):
    return gap.function_call('LeftActingGroup', coset)


def right_acting_group(coset):
    return gap.function_call('RightActingGroup', coset)


def orbit(G, x, action):
    return gap.function_call('Orbit', [G, x, action])


def orbits(G, seeds, action):
    return gap.function_call('Orbits', [G, seeds, action])


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


# Tangles

def leaf_symmetric_group(t1, t2, mu):
    n = t1.n_leaves()
    assert(n == t2.n_leaves())
    return SymmetricGroup(n)

def symmetric_group_dict(t1, t2, mu):
    return leaf_symmetric_group(t1, t2, mu)(mu).dict()

def graph_of_tangle(t1, t2, coset, symmetric=True):
    """
    Symmetric determines if we want to add a feature to t2 to differentiate it
    from t1.
    """
    mu_d = symmetric_group_dict(t1, t2, representative(coset))
    if symmetric:
        g = t1.disjoint_union(t2)
    else:
        # Make t2 special so that we can distinguish it from t1.
        g = t1.disjoint_union(t2.make_special())
    for i in range(1, t1.n_leaves()+1):
        g.add_edge((0, i), (1, mu_d[i]), True)
    return g


def print_tangle(t1, t2, coset):
    print t1.to_newick()
    print t2.to_newick()
    print coset


def _to_newick_pair(t1, t2, mu):
    t2p = t2.copy()
    # Need inverse below because we are relabeling t2's labels in order that
    # they will line up with t1's.
    t2p.relabel(symmetric_group_dict(t1, t2, inverse(mu)))
    return "{}\t{}".format(t1.to_newick(), t2p.to_newick())


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
    return list(reanimate_tangle(*x) for x in sg.load(fname))


def trees_shapes_autos_dn(n, rooted=True):
    trees = enumerate_bifurcating_trees(n, rooted)
    # So that we can recognize trees after acting on t2 by mu^{-1}.
    # `dn` is short for a dictionary keyed on Newick strings.
    dn_trees = {trees[i].to_newick(): i for i in range(len(trees))}
    shapes = []
    # Use Newick shape representation to get a non-redundant collection. Works
    # for rooted and unrooted trees because we are always writing trees as
    # being rooted at zero.
    dn_shapes = OrderedDict()
    for i in range(len(trees)):
        shape_i = trees[i].to_newick_shape()
        if shape_i in dn_shapes:
            dn_shapes[shape_i] = dn_shapes[shape_i] + [i]
        else:
            shapes.append(trees[i])
            dn_shapes[shape_i] = [i]
    shape_autos = [s.automorphism_group() for s in shapes]
    return (trees, shapes, shape_autos, dn_trees)


def make_tangles_extras(n, symmetric=True, rooted=True, sametree=False):
    """
    Make all the tangles with n leaves, along with the number of labeled
    tangles isomorphic to that tangle, and the indices of the mu = id version
    of those trees in enumerate_bifurcating_trees.
    `symmetric` determines if we should consider all ordered or unordered pairs
    of trees.
    If `sametree` is True, then only consider tanglegrams on isomorphic pairs
    of trees.
    """
    fS = sg.SymmetricGroup(n)
    (trees, shapes, shape_autos, dn_trees) = trees_shapes_autos_dn(n, rooted)
    # Iterate over all pairs of tree shape representatives.
    tangles = []
    for i in range(len(shapes)):
        print "Shape {} of {}".format(i+1, len(shapes))
        if sametree:
            j_range = [i]
        else:
            j_range = range(0, len(shapes))
        for j in j_range:
            # Enumerate all double cosets.
            A1 = shape_autos[i]
            A2 = shape_autos[j]
            if symmetric and i > j:
                # If symmetric we only have to generate unordered pairs of
                # representatives.
                continue
            elif symmetric and i == j:
                # If symmetric and we have identical tree shapes, then we can
                # rotate the trees around, "inverting" the coset.
                cosets = inverse_unique_double_cosets(fS, A1)
            else:
                cosets = double_cosets(fS, A1, A2)
            for c in cosets:
                tangle = (shapes[i], shapes[j], c)
                (s_t1, s_t2p) = to_newick_pair(*tangle).split("\t")
                tangles.append((tangle, dn_trees[s_t1], dn_trees[s_t2p]))
    return tangles
