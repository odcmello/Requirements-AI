from nltk.corpus import wordnet as wn
import json

class completeness_test():

    trigger_verb = ''
    trigger_index = -1

    def test(self,sentence,predictor):
        print(sentence)
        print("\n")
        parts_sentence = []
        result = predictor.predict(sentence)
        self.check_role(result,parts_sentence)
        self.check_purpose(result,parts_sentence)
        self.check_what(result,parts_sentence)
        json_dump = json.dumps(parts_sentence)
        json_dump = json.loads(json_dump)
        return json_dump

      
    def check_role(self,result,parts_sentence):
        role = ''
        previous = False
        for verb_index, verb in enumerate(result["verbs"]):
            for arg_index, arg in enumerate(verb["tags"]):
                if(previous == True and (arg == 'I-ARGM-PRD' or arg == 'I-ARGM-ADV' or arg == 'I-ARGM-MNR') ):
                    previous = True
                else:
                    previous = False
                if(((arg == 'B-ARGM-PRD' or arg == 'B-ARGM-ADV' or arg == 'B-ARGM-MNR') and result["words"][arg_index].lower() in "as") or ((arg == 'I-ARGM-PRD' or arg == 'I-ARGM-ADV' or arg == 'I-ARGM-MNR') and previous)):
                    role += result["words"][arg_index] + " "
                    previous = True

        if(role != ''):
            parts_sentence.append({"role":role.capitalize().replace(",","")})
            return parts_sentence
        else:
            parts_sentence.append({"role":''})
            print("Incomplete user story. Role missing.\n")
            return parts_sentence
            
    
    def check_purpose(self,result,parts_sentence):
        purpose = ''
        for verb_index, verb in enumerate(result["verbs"]):
            for arg_index, arg in enumerate(verb["tags"]):
                if(arg == 'B-ARGM-PRP' and self.trigger_index == -1):
                    self.trigger_index = arg_index
                    purpose += result["words"][arg_index] + " "
                if(arg == 'I-ARGM-PRP'):
                    purpose += result["words"][arg_index] + " "
        if(purpose != ''):
            parts_sentence.append({"purpose":purpose.capitalize().replace(",","")})
            return parts_sentence
        else:
            parts_sentence.append({"purpose":''})
            print("Incomplete user story. Purpose missing.\n")
            return parts_sentence

    def check_what(self,result,parts_sentence):
        trigger_word = wn.synset('want.v.02')
        trigger_word2 = wn.synset('need.v.01')
        what = ''

        for verb_index,verb in enumerate(result["verbs"]):
            synonyms = wn.synsets(verb["verb"])
            for synonym in synonyms:
                if(synonym.path_similarity(trigger_word) is not None):
                    if(synonym.path_similarity(trigger_word) > 0.8 or synonym.path_similarity(trigger_word2) > 0.8):
                        self.trigger_verb = verb["verb"]
                        break

            if self.trigger_verb != '':
                break

        if self.trigger_verb == '':
            print("Incomplete user story. Description missing.\n")
            parts_sentence.append({"what":''})
            return parts_sentence
        else:
            if(self.trigger_index == -1):
                self.trigger_index = len(result["words"])

            for x in range(result["words"].index(self.trigger_verb), self.trigger_index):
                what += result["words"][x] + " "
            parts_sentence.append({"what":what.capitalize().replace(",","")})
            return parts_sentence
            

