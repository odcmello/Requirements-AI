import spacy
from nltk.corpus import wordnet as wn

def find_noun_verbs(doc,noun_verb_list):
    for token in doc:
        negation = False
        positive = 0
        if token.pos_ in ("NOUN"):
            verb_list = []
            for ancestor in token.ancestors:
                if(ancestor.pos_ == 'VERB'):
                    verb_list.append(ancestor)
                    positive = positive + 1
            for verb in verb_list:
                for child in verb.children:
                    if child.dep_ == 'neg':
                        negation = True
        if(positive!=0):
            noun_verb_list.append([token,verb_list,negation])
    return noun_verb_list

def numeric_contradiction(doc,doc2,compatnouns):
    contradiction = False
    for compat in compatnouns:
        if(contradiction == True):
                break
        for token in doc:
            tokenNum1 = -1
            if(contradiction == True):
                break
            if(token.i == compat[0].i):
                if(token.i < len(doc)-1):
                    if(doc[token.i+1].pos_ == 'NUM'):
                        tokenNum1 = token.i+1
                if(token.i-1 >= 0):
                    if(doc[token.i-1].pos_ == 'NUM' and tokenNum1 < 0):
                        tokenNum1 = token.i-1
                if(tokenNum1 >= 0):
                    for token2 in doc2:
                        tokenNum2 = -1
                        if(token2.i == compat[1].i):
                            if(token2.i < len(doc2)-1):
                                if doc2[token2.i+1].pos_ == 'NUM':
                                    tokenNum2 = token2.i+1
                            if(token2.i-1 >= 0):
                                if doc2[token2.i-1].pos_ == 'NUM' and tokenNum2 < 0:
                                    tokenNum2 = token2.i-1
                            if(tokenNum2 >= 0):
                                if(doc[tokenNum1].text != doc2[tokenNum2].text):
                                    contradiction = True
                                    break
    return contradiction

def verb_tester(doc, doc2, compatnouns):

    noun_verb_list = []
    noun_verb_list2 = []
        
    noun_verb_list = find_noun_verbs(doc,noun_verb_list)
    noun_verb_list2 = find_noun_verbs(doc2,noun_verb_list2)

    contradiction = False

    for item in noun_verb_list:
        for item2 in noun_verb_list2:
            for compatnoun in compatnouns:
                if(compatnoun[0] == item[0]):
                    if(item2[0] == compatnoun[1]):
                        for verb in item[1]:
                            trigger_verb = False
                            antonym_check = False
                            negation_check = False
                            for verb2 in item2[1]:
                                for lm in verb._.wordnet.lemmas():
                                    if(lm in wn.synset('want.v.02').lemmas() or lm in wn.synset('need.v.01').lemmas()):
                                        trigger_verb = True
                                        break
                                if trigger_verb == False:
                                    for ss in verb._.wordnet.synsets():
                                        if antonym_check == True or negation_check == True:
                                            break
                                        for lm in ss.lemmas():
                                            if antonym_check == True:
                                                break
                                            if lm.antonyms():
                                                for antonym in lm.antonyms():
                                                    if(antonym.name() in doc2.text):
                                                        antonym_check = True #VERB ANTONYM CONTRADICTION
                                                        contradiction = True
                                                        break
                                        if antonym_check == False:
                                            for lm in verb._.wordnet.lemmas():
                                                if negation_check == True:
                                                    break
                                                if lm in verb2._.wordnet.lemmas():
                                                    if item[2] != item2[2]:
                                                        negation_check = True
                                                        contradiction = True #NEGATION CONTRADICTION
                                                        break
    if (contradiction != True):
        contradiction = numeric_contradiction(doc,doc2,compatnouns)

    return contradiction