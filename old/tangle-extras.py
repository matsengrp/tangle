def plot_tangle(n_leaves, tangle_num, out_fname, title):
    """
    Note that tangle_num is 0-indexed.
    """
    return subprocess.check_call([
        "./plot-tangle.R",
        "rooted-symmetric/tangle{}.idx".format(n_leaves),
        str(tangle_num),
        out_fname,
        title])

def ricci_tangles(n, n_extremes = 1):
    tangles = load_tangles("rooted-symmetric/tangle{}.sobj".format(n))
    with open('../analysis/curvatures/rspr/lurw/ricci{}.tsv'.format(n), 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        results = list((row[2],row[3], row[4], int(row[5]), row[6]) for row in reader)
        assert(len(tangles) == len(results))
        # i is 0 indexed
        sort_idx = [i for i in range(len(results)) if results[i][4] != '-']
        sort_idx.sort(key=lambda i: QQ(results[i][4])) # Sort by curvature.
        for i in [sort_idx[j] for j in range(n_extremes) + range(-n_extremes,0)]:
            [t1_s, t2_s, coset, dist, ricci_s] = results[i]
            our_newick_pair = "\t".join([t1_s, t2_s])
            tangle = tangles[i]
            #with open('tangle{}.dot'.format(i), 'w') as f:
            #    f.write(graphviz_str_of_tangle(tangle))
            plot_tangle(n, i,
                'unif-MH-tangle{}-{}.svg'.format(str(n), str(i)),
                'd = {}, κ = {}'.format(results[i][3], results[i][4]))
            nb_show_tangle(tangle)
            print "ricci = {}, dist = {}".format(ricci_s,dist)
            print t1_s
            print t2_s
            print tangle[2]

            assert(our_newick_pair in to_newick_pairs(*tangle)) # Check that we are talking about the same tangle.
def graphviz_str_of_tangle(tangle):
    s = Graph(
        [(i, j, 'within') if l is None else (i, j, 'between')
            for (i, j, l) in graph_of_tangle(*tangle).edges()]
        ).graphviz_string(edge_labels=True)
    s = re.sub(r'label="\(0,.*\)"', 'fillcolor="white" XXX', s)
    s = re.sub(r'label="\(1,.*\)"', 'fillcolor="black" XXX', s)
    s = re.sub(r'XXX', 'shape="point" style="filled" label="" ', s)
    s = re.sub(r'label="within"', 'weight=4', s)
    s = re.sub(r'label="between"', 'style="dotted"', s)
    return s



# TODO: Don't really belong?

def equivalence_classes(criterion, things):
    """
    Given a criterion for isomporphism (returning a boolean and a certificate)
    and a list of things, return an array such that the ith entry is the first
    appearance of the ith thing's equivalence class under the criterion, as
    well as the certificates that show the isomorphism.
    """
    found = []
    map_to_class = []
    certs = []
    identity = {i: i for i in range(things[0].order())}
    for test_i in range(len(things)):
        # Begin search.
        for found_i in found:
            (is_same, cert) = criterion(things[found_i], things[test_i])
            if is_same:
                map_to_class.append(found_i)  # This maps test_i to found_i.
                certs.append(cert)
                break  # We are done searching.
        else:  # Else statement for the for loop (!).
            found.append(test_i)
            map_to_class.append(test_i)  # Isomorphic to self, of course.
            certs.append(identity)
    return (map_to_class, certs)


def equivalence_class_representatives(criterion, things):
    (map_to_class, _) = equivalence_classes(criterion, things)
    return list(things[i] for i in list(set(map_to_class)))


def llt_isomorphism_matrix(l):
    n = len(l)
    return matrix(n, n, lambda i, j: int(l[i].llt_is_isomorphic(l[j])))
