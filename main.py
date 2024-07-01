from file_loader import *
import time
from file_saver import *
from completeness_test import *
from ambiguity_test import *
from contradiction_test import *
from keyword_test import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
from transformer_srl import dataset_readers, models, predictors
import torch
from rake_nltk import *

device = "cuda:0" if torch.cuda.is_available() else "cpu"

loader = file_loader()
user_stories = loader.load_file()

sentence_parts = []
detected_c = []
complete_input = []
ambiguity_input = []
consistent_input = []
complete_timer = []
ambiguity_timer = []
consistent_timer = []

print('==============COMPLETENESS TEST==================')
predictor_complete = predictors.SrlTransformersPredictor.from_path("models/srl_bert_base_conll2012.tar.gz", "transformer_srl")

for user_story in user_stories:
    print("\n")
    start = time.time()
    completeness = completeness_test()
    sentence_parts.append(completeness.test(user_story,predictor_complete))
    end = time.time()
    complete_timer.append(end-start)

    user_input = input ("Problems Found? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        detected_c.append("Problems Found")
    else:
        detected_c.append("No Problems Found")

    user_input = input ("Is the result correct? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        complete_input.append("Passed")
    else:
        complete_input.append("Failed")

    #continue_input = input ("Proceed with the execution? (Y,N)\n")
    #if (continue_input  == 'N'):
    #    exit()

detected_a = []

print('==============AMBIGUITY TEST==================')
nlp = load("en_core_web_sm")
loader = file_loader()
dictionary = loader.loader('vague_terms_dict.txt','','\n')
vague_words = []

for vague_word in dictionary:
    vague_words.append(vague_word.split(",",1))

for sentence_part in sentence_parts:
    print("\n")
    start = time.time()
    unambiguity = ambiguity_test()
    print(user_stories[sentence_parts.index(sentence_part)])
    unambiguity.test(sentence_part[2]['what'],nlp,vague_words)
    end = time.time()
    ambiguity_timer.append(end-start)

    user_input = input ("Problems Found? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        detected_a.append("Problems Found")
    else:
        detected_a.append("No Problems Found")

    user_input = input ("Is the result correct? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        ambiguity_input.append("Passed")
    else:
        ambiguity_input.append("Failed")

    #continue_input = input ("Proceed with the execution? (Y,N)\n")
    #if (continue_input  == 'N'):
    #    exit()

detected_cs = []

print('==============CONSISTENCY TEST==================')

for sentence_part in sentence_parts[:len(sentence_parts):]:
    print("\n")
    start = time.time()
    inconsistency = contradiction_test()

    counter = 0
    for sentence_part2 in sentence_parts[sentence_parts.index(sentence_part)::]:
        counter = 0
        print("\n" + user_stories[sentence_parts.index(sentence_part)])
        print(user_stories[sentence_parts.index(sentence_part2)] + "\n")
        print(sentence_part[0]['role'])
        print(sentence_part2[0]['role'])
        if sentence_part[0]['role'] in sentence_part2[0]['role'] or sentence_part2[0]['role'] in sentence_part[0]['role']:
            print("\n Entering consistency check...\n")
            contradiction1 = inconsistency.test(sentence_part[2]['what'], sentence_part[1]['purpose'])
            contradiction2 = inconsistency.test(sentence_part2[2]['what'],sentence_part2[1]['purpose'])
            contradiction3 = inconsistency.test(sentence_part[2]['what'],sentence_part2[1]['purpose'])
            contradiction3 = inconsistency.test(sentence_part2[2]['what'],sentence_part[1]['purpose'])
            contradiction3 = inconsistency.test(sentence_part[1]['purpose'],sentence_part2[1]['purpose'])
            contradiction3 = inconsistency.test(sentence_part[2]['what'],sentence_part2[2]['what'])
        else:
            print("User stories not contradicting")

    end = time.time()
    consistent_timer.append(end-start)

    user_input = input ("Problems Found? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        detected_cs.append("Problems Found")
    else:
        detected_cs.append("No Problems Found")

    user_input = input ("Is the result correct? (Y,N)\n")
    if(user_input.upper() == 'Y'):
        consistent_input.append("Passed")
    else:
        consistent_input.append("Failed")

    #continue_input = input ("Proceed with the execution? (Y,N)\n")
    #if (continue_input == 'N'):
    #    exit()
    
saver = file_saver()
saver.save_file(user_stories,detected_c,complete_input,detected_a,ambiguity_input,detected_cs,consistent_input,complete_timer,ambiguity_timer,consistent_timer)