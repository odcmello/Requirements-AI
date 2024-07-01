import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
from verb_test import *

class contradiction_test():
  
    def test(self, sentence, sentence2):

        nlp = spacy.load("en_core_web_lg")

        if "WordnetAnnotator" not in nlp.pipe_names:
            nlp.add_pipe(WordnetAnnotator(nlp, name="spacy_wordnet"), after='tagger')

        doc = nlp(sentence)
        doc2 = nlp(sentence2)

        # Extract nouns with adjectives
        nouns = []
        nouns2 = []

        for token in doc:
            if token.pos_ == "NOUN" or (token.pos_ == "ADJ" and (token.head.pos_ == "NOUN" or token.head.head.pos_ == "NOUN")) or (token.pos_ == "PROPN" and (token.head.pos_ == "NOUN" or token.head.head.pos_ == "NOUN")):
                # Check if the token is a noun or an adjective related to a noun
                nouns.append(token)

        for token in doc2:
            if token.pos_ == "NOUN" or (token.pos_ == "ADJ" and (token.head.pos_ == "NOUN" or token.head.head.pos_ == "NOUN")) or (token.pos_ == "PROPN" and (token.head.pos_ == "NOUN" or token.head.head.pos_ == "NOUN")):
                # Check if the token is a noun or an adjective related to a noun
                nouns2.append(token)

        compatibility = []
        compatibility2 = []
        compatnouns = []
        aux = []
        aux2 = []
        count = 0

        for noun in nouns:
            self.check_near_nouns(noun,doc,aux)
            for noun2 in nouns2:
                if count == 0:
                    self.check_near_nouns(noun2,doc2,aux2)
                if not noun._.wordnet.lemmas() or not noun2._.wordnet.lemmas():
                    if(noun.similarity(noun2) >= 0.8):
                        compatibility.append(noun.i)
                        compatibility2.append(noun2.i)
                        compatnouns.append([noun,noun2])
                    continue
                else:
                    for lm in noun._.wordnet.lemmas():
                        if lm in noun2._.wordnet.lemmas():
                            compatibility.append(noun.i)
                            compatibility2.append(noun2.i)
                            compatnouns.append([noun,noun2])
                            break
            count = count + 1

        noun_chunks = []
        noun_chunks_strings = []
        noun_chunks2 = []
        noun_chunks2_strings = []

        self.check_noun_chunks(doc,noun_chunks)
        self.check_noun_chunks(doc2,noun_chunks2)

        self.check_compatibles(compatibility,aux)
        self.check_compatibles(compatibility2,aux2)

        self.convert_chunks_to_strings(noun_chunks,noun_chunks_strings)
        self.convert_chunks_to_strings(noun_chunks2,noun_chunks2_strings)

        nc1 = set(noun_chunks_strings)
        nc2 = set(noun_chunks2_strings)
        complete = set()
        complete_nouns = set()

        n1 = set(nouns)
        n2 = set(nouns2)

        if(len(nc2)>len(nc1)):
            nc3 = nc2-nc1
            complete_nouns = noun_chunks + list(nc3)
        else:
            nc3 = nc1-nc2
            complete_nouns = noun_chunks2 + list(nc3)

        if(len(n2)>len(n1)):
            all_nouns = n2-n1
        else:
            all_nouns = n1-n2

        self.extra_check_compat(compatibility,complete_nouns,aux,doc)
        self.extra_check_compat(compatibility2,complete_nouns,aux2,doc2)

        cp1 = set(compatibility)
        cp2 = set(compatibility2)

        if(len(cp2)>len(cp1)):
            cp3 = cp2-cp1
            complete = list(compatibility) + list(cp3)
        else:
            cp3 = cp1-cp2
            complete = list(compatibility2) + list(cp3)

        counter = 0
        ids = []
        ids2 = []

        for a in aux:
            ids.append(a[1])
        for a2 in aux2:
            ids2.append(a2[1])

        for comp in compatibility:
                if(comp not in ids):
                    counter = counter + 1
        for comp2 in compatibility2:
                if(comp2 not in ids2):
                    counter = counter + 1

        if(len(complete) + counter >= int((len(complete_nouns)+len(all_nouns))/2)):
            return verb_tester(doc,doc2,compatnouns)

    def check_near_nouns(self,noun,doc,aux):
        if(noun.i+1 < len(doc)):
            if(any(item in doc[noun.i+1].pos_ for item in ["NOUN","ADJ","PROPN"])):
                aux.append(["next_noun",noun.i])
        if(noun.i-1 >= 0):
            if(any(item in doc[noun.i-1].pos_ for item in ["NOUN","ADJ","PROPN"])):
                aux.append(["prev_noun",noun.i])
        return 1

    def check_compatibles(self,compatibility, aux):
        compatibility_aux = list(compatibility)
        for compat in compatibility_aux:
            for a in aux:
                if compat == a[1]:
                    if a[0] == 'next_noun':
                        if(aux[aux.index(a)+1][1] not in compatibility):
                            compatibility.remove(compat)
                    elif a[0] == 'prev_noun':
                        if(aux[aux.index(a)-1][1] not in compatibility):
                            compatibility.remove(compat)

    def extra_check_compat(self,compatibility,complete_nouns,aux,doc):
        for a in aux:
            for complete_noun in complete_nouns:
                if(doc[a[1]].text in str(complete_noun) and a[1] in compatibility):
                    compatibility.remove(a[1])

    def check_noun_chunks(self,doc,noun_chunks):
        for token in doc:
            found = False
            for noun_chunk in noun_chunks:
                if (isinstance(noun_chunk,list)):
                    if (token in noun_chunk):
                        found = True
                        continue
                else:
                    if token == noun_chunk:
                        found = True
                        continue
            if (found == True):
                continue
            if(token.i+1 < len(doc)):
                if token.pos_ == "NOUN" and (doc[token.i+1].pos_ in ["NOUN","ADJ","PROPN"]):
                    noun_chunks.append([token,doc[token.i+1]])
                    continue
            if(token.i-1 >= 0):
                if token.pos_ == "NOUN" and (doc[token.i-1].pos_ in ["NOUN","ADJ","PROPN"]):
                    noun_chunks.append([doc[token.i-1],token])
                    continue
            if(token.pos_ == "NOUN"):
                noun_chunks.append(token)

    def convert_chunks_to_strings(self,noun_chunks,noun_chunks_strings):
        for noun_chunk in noun_chunks:
            noun_chunk_string = ''
            if(isinstance(noun_chunk,list)):
                noun_chunk_string = ' '.join(map(str,noun_chunk))
            else:
                noun_chunk_string = str(noun_chunk)
            noun_chunks_strings.append(noun_chunk_string)