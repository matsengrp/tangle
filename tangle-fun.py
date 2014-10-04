from sage.all import gap

### Groups

def conjugate_subgroups(G, H):
    return [G.subgroup(gap_group=X) for X in
            gap.function_call('ConjugateSubgroups', [gap(G), gap(H)])]


def representative(coset):
    return gap.function_call('Representative', coset)


def right_coset(U, g):
    return gap.function_call('RightCoset', [gap(U), gap(g)])


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


### Tangles

def graph_of_tangle(t1, t2, coset):
    n = n_leaves(t1) - 1
    assert(n == n_leaves(t2) - 1)
    mu_d = SymmetricGroup(n)(representative(coset)).dict()
    g = t1.disjoint_union(duplicate_zero_edge(t2))
    for i in range(1, n+1):
        g.add_edge((0, i), (1, mu_d[i]), True)
    return g


def print_tangle(t1, t2, coset):
    print to_newick(t1)
    print to_newick(t2)
    print coset


def saveable_tangle(t1, t2, coset):
    return (t1, t2, str(coset))


def reanimate_tangle(t1, t2, coset_str):
    return (t1, t2, gap(coset_str))


def load_tangles(fname):
    return list(reanimate_tangle(*x) for x in load(fname))


def make_tangles(n, symmetric=True, verbose=True):
    """
    Make all the tangles with n leaves.
    symmetric determines if we should consider all ordered or unordered pairs of trees.
    """
    fS = SymmetricGroup(n)

    trees = equivalence_class_representatives(rooted_is_isomorphic, enumerate_rooted_trees(n))
    tree_autos = list(leaf_autom_group(t) for t in trees)
    # Iterate over all pairs of tree shape representatives.
    tangles = []
    for i in range(len(trees)):
        print "Starting with on tree {} of {}".format(i+1, len(trees))
        for j in range(i, len(trees)):
            if symmetric and i > j:
                # If symmetric we only have to check unordered pairs of
                # representatives.
                continue
            cosets = []
            for sigma in fS:
                c = right_coset(fS.subgroup(tree_autos[i].conjugate(sigma).gens()+tree_autos[j].gens()), sigma)
                if not any(c == cp for cp in cosets):
                    cosets.append(c)
            if verbose:
                print to_newick(trees[i])
                print to_newick(trees[j])
                print cosets
                print ""

            for c in cosets:
                tangles.append((trees[i], trees[j], c))
    return tangles
