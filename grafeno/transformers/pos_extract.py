from grafeno.transformers.base import Transformer as Base

default_sempos = {
    'noun': 'n',
    'verb': 'v',
    'adjective': 'j',
    'adverb': 'r'
}

class Transformer (Base):

    def __init__ (self, sempos = default_sempos, **kwds):
        # print("(t/pos_extract.py): __init__")
        super().__init__(**kwds)
        self.__list = sempos.keys()
        self.__dict = sempos
        # print("( t/pos_extract.py): sempos es %r" % sempos)
        

    def transform_node (self, msnode):
        # print("(t/pos_extract.py): transform_node")
        sem = super().transform_node(msnode)
        pos = msnode.get('pos')
        if pos in self.__list:
            sem['concept'] = msnode.get('lemma')
            sem['sempos'] = self.__dict[pos]
        return sem
