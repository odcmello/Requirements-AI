import contractions
import nltk
from nltk import CFG
from textblob import TextBlob
from file_loader import * 
from spacy import *
from enum import Enum

class ambiguity_test():

    def test(self,sentence,nlp,vague_words):
        sentence = self.expand_words(sentence)
        print("\n")
        self.detect_ambiguities(sentence)
        self.detect_vagueness(sentence,nlp,vague_words)
        print("\n")

    def detect_ambiguities(self,sentence):

        pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence))
        
        cfg_tags = {
            'CC': 'Conj',  # Coordinating conjunction
            'CD': 'Num',   # Cardinal number
            'DT': 'Det',   # Determiner
            'EX': 'Pron',  # Existential there
            'FW': 'X',     # Foreign word
            'IN': 'P',     # Preposition or subordinating conjunction
            'JJ': 'Adj',   # Adjective
            'JJR': 'Adj',  # Adjective, comparative
            'JJS': 'Adj',  # Adjective, superlative
            'LS': 'X',     # List item marker
            'MD': 'V',     # Modal
            'NN': 'N',     # Noun, singular or mass
            'NNS': 'N',    # Noun, plural
            'NNP': 'PropN', # Proper noun, singular
            'NNPS': 'PropN', # Proper noun, plural
            'PDT': 'Det',  # Predeterminer
            'POS': 'P',    # Possessive ending
            'PRP': 'Pron', # Personal pronoun
            'PRP$': 'Det', # Possessive pronoun
            'RB': 'Adv',   # Adverb
            'RBR': 'Adv',  # Adverb, comparative
            'RBS': 'Adv',  # Adverb, superlative
            'RP': 'P',     # Particle
            'SYM': 'X',    # Symbol
            'TO': 'P',     # to
            'UH': 'X',     # Interjection
            'VB': 'V',     # Verb, base form
            'VBD': 'V',    # Verb, past tense
            'VBG': 'V',    # Verb, gerund or present participle
            'VBN': 'V',    # Verb, past participle
            'VBP': 'V',    # Verb, non-3rd person singular present
            'VBZ': 'V',    # Verb, 3rd person singular present
            'WDT': 'Det',  # Wh-determiner
            'WP': 'Pron',  # Wh-pronoun
            'WP$': 'Det',  # Possessive wh-pronoun
            'WRB': 'Adv'   # Wh-adverb
        }

        # Initialize the list to store the CFG rules
        cfg_rules = [
            "S -> NP VP",
            "NP -> Det N | NP PP | Pron",
            "VP -> V NP | VP PP",
            "PP -> P NP"
        ]

        # Convert POS tags to CFG-like tags and create rules
        for word, pos in pos_tags:
            cfg_pos = cfg_tags.get(pos, 'Other')
            if(word.startswith('\'')):
                cfg_rules.append(f"{cfg_pos} -> '{word[1:]}'")
            else:
                cfg_rules.append(f"{cfg_pos} -> '{word}'")

        # Create the CFG from rules
        cfg_string = "\n".join(cfg_rules)

        cfg = CFG.fromstring(cfg_string)

        # Initialize the parser
        parser = nltk.ChartParser(cfg)

        count = 0

        tokens = nltk.word_tokenize(sentence)

        for index, token in enumerate(tokens):
            if token.startswith('\''):
                tokens[index] = token[1:]

        # Parse the sentence and display trees
        for tree in parser.parse(tokens):
            count += 1
        
        if(count>1):
            print('The user story have multiple interpretations.')

    def detect_vagueness(self,sentence,nlp,vague_words):

        pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence.lower()), tagset='universal')
        possible_vagues = []

        for word, pos in pos_tags:
            if pos == 'ADJ' or 'DET' or 'ADV' or 'NOUN':
                possible_vagues.append(word)

        vague_terms = []

        for term in vague_words:
            if term[0] in possible_vagues:
                    vague_terms.append(term)
                        
        if vague_terms:
                for vague_term in vague_terms:
                    print("The user story contains the word \"" + vague_term[0] + "\" which can indicate the presence of " + vague_term[1] + ".")
        else:
                print("The user story does not contain vague words.")

    def expand_words(self,sentence):
        expanded_words = []   
        for word in sentence.split():
            # using contractions.fix to expand the shortened words
            expanded_words.append(contractions.fix(word))  
        return " ".join(expanded_words)