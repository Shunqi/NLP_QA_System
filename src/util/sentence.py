import os
from nltk.parse import stanford
from collections import Counter
import spacy
import pandas as pd

os.environ['STANFORD_PARSER'] = 'stanford-parser-full-2018-10-17/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'
pcfg_parser = stanford.StanfordParser(model_path='stanford-parser-full-2018-10-17/englishPCFG.ser.gz')
dep_parser = stanford.StanfordDependencyParser(model_path='stanford-parser-full-2018-10-17/englishPCFG.ser.gz')
        
def stanford_parser(self, sentence):
    pcfg = pcfg_parser.raw_parse(sentence).__next__()
    dep = dep_parser.raw_parse(sentence).__next__()
    dep_list = list(dep.triples())
    return dep_list, pcfg

def Spacy_parser(sentence):
    
    # from tabulate import tabulate

    word_Pos = {}
    Pos_word = {}
    dep_dict = {}  # dict for dependency
    NER = []

    nlp = spacy.load('en_core_web_lg')

    doc = nlp(sentence)
    for ent in doc.ents:
        NER.append([ent.text, ent.label_])

    for token in doc:
        # print(token.text, token.dep_, token.head.text, token.head.pos_, token.tag_, [child for child in token.children])
        # result.append([token.text, token.dep_, token.pos_, token.tag_, [child for child in token.children]])

        # update the dict with the word as key
        word_Pos.update({token.text: [token.lemma_, token.pos_, token.tag_, [child for child in token.children]]})

        # update the dependency dict
        dep_dict.update({token.dep_: [token.text, token.tag_]})

        # update the dict with the Pos tag as key
        if token.tag_ not in Pos_word:
            Pos_word.update({token.tag_: token.text})
        else:
            temp = []
            value = Pos_word.get(token.tag_)
            if isinstance(value, list):  # check if the value is a list
                temp.extend(Pos_word.get(token.tag_))
            else:
                temp.append(Pos_word.get(token.tag_))
            temp.append(token.text)
            Pos_word.update({token.tag_: temp})

    return word_Pos, Pos_word, NER, dep_dict