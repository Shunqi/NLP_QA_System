import os
from nltk.parse import stanford
from collections import Counter
import spacy

os.environ['STANFORD_PARSER'] = '../stanford-parser-full-2018-10-17/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '../stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'
pcfg_parser = stanford.StanfordParser(model_path='../stanford-parser-full-2018-10-17/englishPCFG.ser.gz')
dep_parser = stanford.StanfordDependencyParser(model_path='../stanford-parser-full-2018-10-17/englishPCFG.ser.gz')

nlp = spacy.load('en_core_web_lg')

def stanford_parser(sentence):
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

    # nlp = spacy.load('en_core_web_lg')

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

def get_nsubj(sentence):
    doc = nlp(sentence)
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            return chunk.text
    return ''

def get_ROOT(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'ROOT':
            return token.text, token.lemma_,token.tag_
    return ''

def get_entity(sentences):
    entity = []
    doc = nlp(sentences)
    for ent in doc.ents:
        entity.append( ent.label_)
    return entity

def get_namechunks(sentence):
    chunks = {}
    doc = nlp(sentence)
    for chunk in doc.noun_chunks:
        chunks[chunk.text] = chunk.root.text
        #chunks.append(chunk.text)
    return chunks

def get_tense(verb_t):
    # the verb is present third person singular
    if verb_t == 'VBZ':
        result = " does "
    elif verb_t in ['VBP', 'VBG', 'VB']:
        # tense = "present"
        result = " do " 
    elif verb_t in ['VBD', 'VBN']:
        # tense = "past"
        result = " did "
    else:
        result = ' does '
    return result

def get_pps(sentence):
    doc = nlp(sentence)
    pps = []
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
    return pps

def lower_firstword(sentence, word_Pos):
    doc = nlp(sentence)
    first_word = str(doc[0])
    first_word_tag = word_Pos.get(first_word)[2]  # the tag of the first word
    if first_word_tag != "NNP" and first_word != "I":
        first_word_lower = first_word.lower()
        sentence = sentence.replace(first_word, first_word_lower, 1)
    return sentence

def get_nearest_prep(keyphrase, word_Pos, verb):
    filtered_list = ['the', 'that']
    prep = ''
    start = 0
    if keyphrase.count(verb) >= 1:
        start = keyphrase.index(verb) + 1
    for i in range(start, len(keyphrase)):
        if i > 1 + start:
            break
        temp_prep = keyphrase[i]
        if temp_prep not in filtered_list and word_Pos.get(temp_prep) != None \
            and ('IN' in word_Pos.get(temp_prep) or 'TO' in word_Pos.get(temp_prep)):
            prep = temp_prep
            if i == start and temp_prep == 'to' and word_Pos.get(keyphrase[i+1]) != None and 'VB' in word_Pos.get(keyphrase[i+1]):
                prep = prep + ' ' + keyphrase[i+1]
            if i == 1 + start:
                prep = keyphrase[i-1] + ' ' + prep
            break
    return prep

def find_first_comma(doc, word_Pos, sentence, verb, copula):
    location_or_time = ''
    first_word = str(doc[0])
    first_word_tag = word_Pos.get(first_word)[2]  # the tag of the first word
    # print(first_word, first_word_tag)
    if first_word != 'The' and ('IN' in first_word_tag or first_word_tag == 'TO' or first_word_tag == 'VBG'):
        first_comma = sentence.find(',')
        if (verb != '' and first_comma < sentence.find(verb)) or (copula != '' and first_comma < sentence.find(copula)):
            location_or_time = sentence[:first_comma+1]
    if location_or_time == '':
        temp_commalist = sentence.split(',')
        if temp_commalist[0] == first_word.lower():
            first_comma = sentence.find(',')
            location_or_time = sentence[:first_comma+1]
    return location_or_time

def replace_first_comma(question, location_or_time, neg_rb):
    if location_or_time != '' and location_or_time in question:
        question = question.replace(location_or_time, '')[1:]
        location_or_time = ' ' + location_or_time[:-1]
        if location_or_time[1:] in neg_rb:
            location_or_time = ''
        return question, location_or_time
    else:
        if location_or_time in neg_rb:
            location_or_time = ''
        return question, location_or_time

def replace_verb(question, verb, verb_s):
    index = question.find(' ' + verb + ' ')
    if index == -1:
        index = question.find(' ' + verb)
    if index == -1:
        index = question.find(verb + ' ')
    