def shortest_fewest_cycles_sort(perm_set):
    """
    Sort first by the number of cycles, then by the length of those cycles.
    """
    l = list(perm_set)
    l.sort(key=lambda x: len(x.cycles()))

    def my_max(lp):
        if lp == []:
            return 0
        else:
            return max(lp)

    # Sort according to the maximum length of any cycle in the permutation.
    l.sort(key=lambda x: my_max(list(len(c) for c in x.cycle_tuples())))
    return l


def graph_of_tangle(t1, t2, orbit):
    sigma_d = orbit[0].dict()
    n = len(sigma_d)  # Number of rooted leaves.
    assert(n == n_leaves(t1) - 1)
    assert(n == n_leaves(t2) - 1)
    g = t1.disjoint_union(t2)
    for i in range(1, n+1):
        g.add_edge((0, i), (1, sigma_d[i]), i)
    return g


def print_tangle(t1, t2, orbit, print_orbit=False):
    print to_newick(t1)
    print to_newick(t2)
    if print_orbit:
        print orbit
    else:
        print orbit[0]


def make_tangles(n, symmetric=True, verbose=True):
    """
    Make all the tangles with n leaves.
    symmetric determines if we should consider all ordered or unordered pairs of trees.
    """
    trees = enumerate_rooted_trees(n)
    fS = SymmetricGroup(n)
    # sidxs are the indices of the representatives, and sigmatilde are the standard permutations extended to all internal nodes.
    # Each of these are indexed by the trees.
    (sidxs, sigmas_tilde) = equivalence_classes(rooted_is_isomorphic, trees)
    # Here we get the standard permutations, restricted to the leaves.
    sigmas = list(fS(list(sigma[i] for i in range(1,n+1))) for sigma in sigmas_tilde)
    # Here the automorphisms are indexed the trees, but they are of the corresponding representatives.
    # Wasteful computation as we are recomputing the automorphism group for every representative many times,
    # but it probably doesn't matter compared to the following quadratic step.
    autos = list(leaf_autom_group(trees[sidx]) for sidx in sidxs)
    tangles = set()
    # Iterate over all pairs of trees. Some of these will be duplicates for
    # sure.
    for i in range(len(trees)):
        if verbose:
            print "Working on tree {} of {}".format(i+1, len(trees))
        for j in range(i+1, len(trees)):
            if symmetric and sidxs[i] > sidxs[j]:
                # If symmetric we only have to check unordered pairs of
                # representatives.
                continue
            orbit = set()
            # Again, autos[i] is the automorphism group of the _representative_
            # of the ith tree.
            for ai in autos[i]:
                for aj in autos[j]:
                    orbit.add((sigmas[j] * aj).inverse() * sigmas[i] * ai)
                    if symmetric:
                        orbit.add((sigmas[i] * ai).inverse() * sigmas[j] * aj)
            tangles.add((sidxs[i], sidxs[j], frozenset(orbit)))
    return list((trees[si], trees[sj], tuple(shortest_fewest_cycles_sort(o)))
                for (si, sj, o) in tangles)
