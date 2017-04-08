from grafeno.transformers.base import Transformer as Base

default_sempos = {
    'noun': 'n',
    'verb': 'v',
    'adjective': 'j',
    'adverb': 'r'
}

class Transformer (Base):
    '''This transformer carries over all morphological nodes and syntactic
    dependencies to the semantic level. It is good for developing/debugging
    purposes, since it directly translates the dependency tree into the semantic
    graph.'''
    def __init__ (self, sempos = default_sempos, **kwds):
        # print("(t/all.py): __init__")
        super().__init__(**kwds)
        self.__list = sempos.keys()
        self.__dict = sempos
        # print("( t/all.py): sempos es %r" % sempos)
        

    def transform_node (self, msnode):
        '''The concept is the lemma of the morphological node.'''
        # print("(t/all.py): transform_node")
        sem = super().transform_node(msnode)
        sem.update(msnode)
        sem['concept'] = msnode['lemma']
        return sem

    def transform_dep (self, dependency, parent, child):
        '''The functor is the dependency name.'''
        # print("(t/all.py): transform_dep")
        # se sacan las aristas de base.transform_dep
        edge = super().transform_dep(dependency, parent, child)
        p = self.nodes[edge['parent']]
        c = self.nodes[edge['child']]
        # print("(t/all.py): transform_dep: edge-->%r" % edge)
        # print("(t/all.py): transform_dep: parent-->%r" % p)
        # print("(t/all.py): transform_dep: child-->%r" % c)
        edge['functor'] = dependency
        return edge
