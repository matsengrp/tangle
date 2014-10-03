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
    fS = SymmetricGroup(n)
    trees = tree_shape_representatives(n)
    tree_autos = list(leaf_autom_group(t) for t in trees)
    # Iterate over all pairs of tree shape representatives.
    tangles = []
    for i in range(len(trees)):
        if verbose:
            print "Working on tree {} of {}".format(i+1, len(trees))
        for j in range(i+1, len(trees)):
            if symmetric and i > j:
                # If symmetric we only have to check unordered pairs of
                # representatives.
                continue
            tangle_autos = fS.subgroup(tree_autos[i].gens() + tree_autos[j].gens())
            for coset in fS.cosets(tangle_autos):
                tangles.append((trees[i], trees[j], coset))
    return tangles
