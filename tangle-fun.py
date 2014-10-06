from sage.all import gap
# Depends on curvature/tree-fun.py

# Cosets


def double_coset(U, g, V):
    return gap.function_call('DoubleCoset', [gap(U), gap(g), gap(V)])


def representative(coset):
    return gap.function_call('Representative', coset)


def left_acting_group(coset):
    return gap.function_call('LeftActingGroup', coset)


def right_acting_group(coset):
    return gap.function_call('RightActingGroup', coset)


def as_list(coset):
    return gap.function_call('AsList', coset)


def size(domain):
    return gap.function_call('Size', domain)


gap.eval("""
OnDoubleCosets := function(coset, g)
      return DoubleCoset(LeftActingGroup(coset),
               OnRight(Representative(coset), g),
               RightActingGroup(coset));;
end
""")


def on_double_cosets(coset, g):
    """
    Act on a double coset.
    """
    return gap.function_call('OnDoubleCosets', [coset, gap(g)])


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

def coset_dict(t1, t2, coset):
    n = n_leaves(t1) - 1
    assert(n == n_leaves(t2) - 1)
    return SymmetricGroup(n)(representative(coset)).dict()


def graph_of_tangle(t1, t2, coset):
    n = n_leaves(t1) - 1
    mu_d = coset_dict(t1, t2, coset)
    g = t1.disjoint_union(duplicate_zero_edge(t2))
    for i in range(1, n+1):
        g.add_edge((0, i), (1, mu_d[i]), True)
    return g


def print_tangle(t1, t2, coset):
    print to_newick(t1)
    print to_newick(t2)
    print coset


def to_newick_pair(t1, t2, coset):
    t2p = t2.copy()
    t2p.relabel(coset_dict(t1, t2, coset))
    return "{}\t{}".format(to_newick(t1), to_newick(t2p))


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
        print "Tree {} of {}".format(i+1, len(trees))
        for j in range(0, len(trees)):
            if symmetric and i > j:
                # If symmetric we only have to check unordered pairs of
                # representatives.
                continue
            cosets = []
            for mu in fS:
                c = double_coset(tree_autos[i], mu, tree_autos[j])
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
