from collections import deque

class Transformer:

    def __init__ (self, graph=None):
        self.graph = graph

    def transform_sentence (self, tree):
        '''Transform the tree according to the rules and add
        resulting nodes and edges to the graph'''
        self.pre_process(tree)
        nodes = self.process_nodes(tree)
        deps = self.extract_dependencies(tree)
        deps.reverse()
        edges = self.process_edges(nodes, deps)
        nodes, edges = self.post_process(nodes, edges)
        sentence_nodes = self.add_to_graph(nodes, edges)
        self.post_insertion(sentence_nodes)

    def process_nodes (self, tree):
        nodes = {}
        for ms in tree['tokens']:
            sem = self.transform_node(ms)
            if sem:
                nodes[sem['id']] = sem
        return nodes

    def transform_node (self, msnode):
        '''take a morfosyntactic node (dict) and return a semantic node (dict).
        Semantic nodes get dropped in the end if they don't have a concept
        attribute.'''
        return { 'id': msnode['id'] }

    def extract_dependencies (self, tree):
        deps = deque([(tree['dependencies'][0],None)])
        edges = []
        while len(deps)>0:
            d, parent = deps.popleft()
            if parent:
                edges.append((d['function'], parent, d['token']))
            for c in d.get('children', []):
                deps.append((c,d['token']))
        return edges

    def process_edges (self, nodes, deps):
        edges = []
        for d in deps:
            name, parent, child = d
            if parent not in nodes or child not in nodes:
                continue
            edges.append(self.transform_dep(name, nodes[parent], nodes[child]))
        return edges

    def transform_dep (self, dependency, parent, child):
        '''take a dependency relation (str) and the parent and child nodes
        (semnodes, dict) and return a semantic edge (dict). Semantic edges get
        dropped in the end if they don't have a functor attribute.'''
        return { 'parent': parent['id'],
                 'child': child['id'] }

    def add_to_graph (self, nodes, edges):
        g = self.graph
        tokens = {}
        for k in nodes:
            node = nodes[k]
            if 'concept' in node:
                tokid = node['id']
                del node['id']
                concept = node['concept']
                del node['concept']
                nid = g.add_node(concept, **node)
                tokens[tokid] = nid
        for edge in edges:
            if 'functor' in edge:
                parent, child = edge['parent'], edge['child']
                del edge['parent']
                del edge['child']
                if parent in tokens:
                    parent = tokens[parent]
                if child in tokens:
                    child = tokens[child]
                functor = edge['functor']
                del edge['functor']
                g.add_edge(parent, child, functor, **edge)
        return [tokens[i] for i in tokens]

    def pre_process (self, tree):
        pass

    def post_process (self, nodes, edges):
        return nodes, edges

    def post_insertion (self, sentence_nodes):
        pass

    def after_all (self):
        pass