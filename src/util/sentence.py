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

#input should be a sentence
def Spacy_parser(sentence): 
    from collections import Counter
    import spacy
    import pandas as pd
    #from tabulate import tabulate
    
    word_Pos = {}
    Pos_word = {}
    dep_dict = {} # dict for dependency 
    ner_list = []
    NER = False # boolean value

    nlp = spacy.load('en_core_web_lg')

    doc = nlp(sentence)
    
    for ent in doc.ents:
        ner_list.append([ent.text, ent.label_])
        
    if not ner_list: # if the list is not empty
        NER = True
        
    for token in doc:        
        # update the dict with the word as key
        word_Pos.update({token.text:[token.lemma_, token.pos_, token.tag_, [child for child in token.children]]})
        
        # update the dependency dict
        dep_dict.update({token.dep_:[token.text, token.tag_]})
        
        # update the dict with the Pos tag as key
        if token.tag_ not in Pos_word:
            Pos_word.update({token.tag_: token.text})
        else: 
            temp = []
            value = Pos_word.get(token.tag_)
            if isinstance(value, list): # check if the value is a list
                temp.extend(Pos_word.get(token.tag_))
            else:
                temp.append(Pos_word.get(token.tag_))
            temp.append(token.text)
            Pos_word.update({token.tag_:temp})
        
    return word_Pos, Pos_word, NER, dep_dict, doc 

def get_NE(sentence):
    l = []
    doc = nlp(sentence)
    for ent in doc.ents:
        l.append(ent.label_)
    return l
def get_nsubj(doc):
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            return chunk.text
    return ''

def get_ROOT(doc):
    for token in doc:
        if token.dep_ == 'ROOT':
            return token.text, token.lemma_,token.tag_
    return ''

def get_entity(doc):
    entity = []
    for ent in doc.ents:
        entity.append( ent.label_)
    return entity


def get_namechunks(doc):
    chunks = {}
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

def get_pps(doc):
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
        if temp_commalist[0] == first_word.lower() and 'RB' in first_word_tag:
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
    start = question.find(' ' + verb + ' ')
    if start == -1:
        start = question.find(' ' + verb)
    if start != -1:
        start = start + 1
    else:
        start = question.find(verb + ' ')
    if start == -1:
        return question
    end = start + len(verb)
    question = question[:start] + verb_s + question[end:]
    return question

def format_question(question):
    if question == None:
        return ''
    words = question.split()
    if len(words) < 1:
        return question
    words[0] = words[0].capitalize()
    if words[len(words)-1] == '?':
        words = words[:len(words)-1]
        words[len(words)-1] = words[len(words)-1] + '?'
    question = " ".join(words)
    return question

def format_answer(answer):
    if answer == None:
        return ''
    words = answer.split()
    if len(words) < 1:
        return answer
    words[0] = words[0].capitalize()
    if words[len(words)-1] == '.':
        words = words[:len(words)-1]
        words[len(words)-1] = words[len(words)-1] + '.'
    answer = " ".join(words)
    return answer

def filter_what(question, sentence):
    question = format_question(question)
    question_list = question.split()
    sentence_list = sentence.split()
    if len(question_list) < 5 or len(question_list) > len(sentence_list) - 3:
        return ''
    else:
        return question
    
def select_sentence(sentences, n):
    if n >= len(sentences):
        return sentences
    
    keywordlist1 = [' and', ' but', ' it', 'it ', 'they', 'them', 'their', ' him', ' his', 'he ', ' he' \
        'her', 'she ', ' she', 'which', 'what', 'who', 'whom', 'where', 'when', 'while', ',', ';']
    keywordlist2 = ['They', 'He', 'She', 'It']
    rank_list = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        score = 0
        words = sentence.split()
        if sentence[0].isalpha() == False:
            score += 50
        if sentence[-1] != '.':
            score += 50
        if sentence.count('(') != sentence.count(')'):
            score += 60
        if words[0] in keywordlist2:
            score += 40
        if len(words) < 10:
            score += 50
        for word in keywordlist1:
            score += sentence.count(word) * 2
        score += len(words) * 0.1
        rank_list.append((sentence, score))
    rank_list.sort(key=lambda tup: tup[1])
    filtered_sentences = [x[0] for x in rank_list]
    filtered_sentences = filtered_sentences[:n+5]
    return filtered_sentences