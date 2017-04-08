from nltk.corpus import wordnet as wn

from grafeno.transformers.base import Transformer as Base

class Transformer (Base):

    def post_process (self):
        # print("(___wordnet.py): post_process")
        super().post_process()
        for n in self.nodes.values():
            concept = n.get('concept')
            if not concept:
                continue
            pos = n.get('sempos')
            if pos in {'n','v'}:
                ss = wn.synsets(concept, pos, lang="spa")
            elif pos == 'j':
                ss = wn.synsets(concept, 'a', lang="spa")
            else:
                ss = wn.synsets(concept, lang="spa")
            if len(ss):
                # WSD by MFS
                n['synset'] = ss[0]
