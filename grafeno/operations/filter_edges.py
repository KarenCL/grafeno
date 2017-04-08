from collections import defaultdict

# cgraph: puede tratarse de un grafo de conceptos
# sds

def filter_edges (cgraph, remove=[], rename={}, frequency=None):
    # print("(____filter_Edges.py): dentro de")
    g = cgraph._g
    to_rem = []
    if frequency:
        # print("(____filter_Edges.py): frequency ->%r" % frequency)
        freqs = defaultdict(lambda:0)
        for n, m, d in g.edges_iter(data=True):
            freqs[d['functor']] += 1
    # n, m, d pueden representar los extremos de una arista y su 'peso'
    for n, m, d in g.edges_iter(data=True):
        ftor = d['functor']
        if frequency and (freqs[ftor]>frequency['max'] or freqs[ftor]<frequency['min']):
            to_rem.append((n,m))
        if ftor in rename:
            d['functor'] = rename[ftor]
        if ftor in remove:
            to_rem.append((n,m))
    g.remove_edges_from(to_rem)

def operate (graph, **args):
    filter_edges(graph, **args)
    return graph
