from nltk.corpus import wordnet as wn  # import wordnet
import sys
sys.path.append('../')
from util.sentence import *

# a function to answer yes/no question, s is the original sentence, q is the question
def answer_YN(s, q):
    # count the number of not, 't, no in original sentence
    doc = nlp(s)
    words = ['not','n','no','cannot']
    count = 0 # number of negative words
    JJ_word =[]
    
    for token in doc:        
        if token.text.lower() in words:
            count +=1
        if token.tag_ =="JJ":
            JJ_word.append(token.text) # update the ADJ word in list
    
    JJ_word_q = []
    doc_q = nlp(q) # tokenize the question 
    for token in doc_q:        
        if token.tag_ == "JJ": # there is an adjective word 
            JJ_word_q.append(token.text)         
        
    if not JJ_word_q:
        if count%2 == 0:
            return "Yes"
        else:
            return "No"
            
    target_word = []
    
    for i, word in enumerate(JJ_word_q):
        if word not in JJ_word: # the word does not exists in original sentence
            target_word.append([word, JJ_word])
    # print(target_word)
                
    if not target_word: # if the list is empty
        if count%2 == 0:
            return "Yes"
        elif count == 1:
            return 'No'
        else:
            return "No"
        
    else: # the list is not empty
        
        for i, words in enumerate(target_word):
            word_q = words[0]
            word_s_list = words[1] # it's a list
            
            wordnet = word_net(word_q)
            synonyms = wordnet[0]
            antonyms =  wordnet[1]
        
            for word in word_s_list:
                if word in synonyms: # if the words are synonyms
                    if i == len(target_word)-1:
                        if count%2 == 0:
                            return "Yes"
                        else:
                            return "No"                    
                    else:
                         continue
                elif word in antonyms: # if the words are antonyms
                    if count%2 == 0:
                        return "No"
                    elif count ==1:
                        return "No"
                    else:
                        return "Yes"
                else: # word doesn't belong to any of those
                    continue 


def word_net(word):  # input is a word
    synonyms = []
    antonyms = []

    for syn in wn.synsets(word, pos=wn.ADJ):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    return synonyms, antonyms

def answer_what(sentence, question):
    dependency, pas = stanford_parser(sentence)
    word_Pos, _, _, dep_dict, doc = Spacy_parser(sentence)
    # there is no be_words, check what is the tense of the sentence
    temp = dep_dict.get("ROOT")
    root_word = temp[0]  # the root word
    tag = temp[1]  # the pos tag of the root word
    # print(root_word)
    # dependency, pas = stanford_parser(sentence)
    # print(dependency)
    # pas.pretty_print()

    keyword = ''
    copula = ''
    verb = ''
    aux = ''
    auxpass = ''
    for i in range(len(dependency)):
        # print(dependency[i])
        if (dependency[i][1] == 'cop'):
            keyword = dependency[i][0][0]
            copula = dependency[i][2][0]
            break
    if keyword == '':
        for i in range(len(dependency)):
            # print(dependency[i])
            if (dependency[i][1] == 'dobj'):
                keyword = dependency[i][2][0]
                verb = dependency[i][0][0]
                break
    if keyword != root_word:
        keyword = ''
    if keyword == '':
        verb = root_word
    # print(keyword, copula, verb)

    for i in range(len(dependency)):
        if (dependency[i][1] == 'aux' and verb == dependency[i][0][0]):
            aux = dependency[i][2][0]
            break
    if verb != '':
        for i in range(len(dependency)):
            if (dependency[i][1] == 'auxpass' and verb == dependency[i][0][0]):
                auxpass = dependency[i][2][0]
                break
    
    keyphrase = None
    if keyword != '':
        for s in pas.subtrees():
            if s.label() == 'NP' and keyword in s.leaves() and keyphrase == None:
                keyphrase = s.leaves()
    elif verb != '':
        for s in pas.subtrees():
            if s.label() == 'VP' and verb in s.leaves() and keyphrase == None:
                keyphrase = s.leaves()
    # print(keyphrase)
    if keyphrase is None:
        return sentence

    sentence = lower_firstword(sentence, word_Pos)

    if verb != '' and keyword != '':
        # find the original word in word_Pos dict
        verb_s = word_Pos.get(root_word)[0]

        length = len(keyphrase)
        keyphrase_s = ' '.join(x for x in keyphrase)
        keyphrase_s = keyphrase_s.replace(' ,', ',')
        return keyphrase_s
    elif copula != '':
        obj_index = sentence.find(' '+copula+' ')
        if obj_index == -1:
            obj_index = sentence.find(' '+copula+',')
            if obj_index == -1:
                return ''
        answer = sentence[obj_index+len(copula)+2:]
        return answer
    else:
        # find the original word in word_Pos dict
        verb_s = word_Pos.get(root_word)[0]
        length = len(keyphrase)
        keyphrase_s = ' '.join(x for x in keyphrase)
        keyphrase_s = keyphrase_s.replace(' ,', ',')
        return keyphrase_s

def get_ent(sentences):
    entity = []
    doc = nlp(sentences)
    for ent in doc.ents:
        entity.append( (ent.text,ent.label_))
    return entity

def get_noun(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.pos_ == 'NOUN':
            return token.text

def locate_cardinal(sentence):
    cardinal = []
    for en in get_ent(sentence):
        if en[1] == 'CARDINAL' or en[1] == 'QUANTITY':
            cardinal.append(en[0])
    return cardinal

def locate_cardinal2(sentence):
    cardinal = []
    for en in get_ent(sentence):
        if en[1] in ['CARDINAL', 'QUANTITY','PERCENT','MONEY']:
            cardinal.append(en[0])
    return cardinal

def get_lemma(word):
    token = nlp(word)
    lemma = token[0].lemma_
    return lemma

def answer_how(sentence, question):
    noun = get_noun(question)
    if noun is None:
        card_list = locate_cardinal2(sentence)
        if len(card_list) != 0:
            return card_list[0]
        else:
            return sentence
           
    else:
        noun_lemma = get_lemma(noun)
        if 'how much' in question.lower():
            card_list = locate_cardinal2(sentence)
        else:
            card_list = locate_cardinal(sentence)
        min_dist = 9999
        answer = sentence
        for card in card_list:
            #print(card)
            dist = calculate_word_distance(noun_lemma, card, sentence)
            #print(dist)
            if dist < min_dist:
                min_dist = dist
                answer = card
                #print(answer)
        return answer

def get_question_type(question):
    question = question.lower()

    # TODO: in which year? whom? 
    question_types = ["where", "when", "who"]
    question_index = []

    for q_type in question_types:
        if question.find(q_type) < 0:
            question_index.append(len(question))
        else:
            question_index.append(question.find(q_type))

    question_type = question_types[question_index.index(min(question_index))]

    # print(question_type)
    return question_type

def answer_when(candidate, question):
    question_type = get_question_type(question)
    doc = nlp(candidate)

    ents = []
    for ent in doc.ents:
        if len(ents) == 0:
            e = dict()
            e['text'] = ent.text
            e['start'] = ent.start_char
            e['end'] = ent.end_char
            e['label'] = ent.label_
            e['level'] = 0
            ents.append(e)
        else:
            prev = ents[-1]
            if ent.start_char - prev['end'] < 4 and prev['label'] == ent.label_:
                prev['text'] += candidate[prev['end']:ent.end_char]
                prev['end'] = ent.end_char
                prev['level'] = 1
            elif ent.start_char - prev['end'] < 8 and prev['label'] == ent.label_ and "and" in candidate[prev['end']:ent.start_char]:
                prev['text'] += candidate[prev['end']:ent.end_char]
                prev['end'] = ent.end_char
                prev['level'] = 1
            else:
                e = dict()
                e['text'] = ent.text
                e['start'] = ent.start_char
                e['end'] = ent.end_char
                e['label'] = ent.label_
                e['level'] = 0
                ents.append(e)

    type_label_map = dict()
    type_label_map["where"] = ["LOCATION", "GPE"]
    type_label_map["when"] = ["DATE", "TIME"]
    type_label_map["who"] = ["PERSON", "ORG"]

    for ent in ents:
        if ent['label'] in type_label_map[question_type] and ent['text'] not in question:
            return ent['text']
    
    for ent in doc.ents:
        if ent.label_ in type_label_map[question_type] and ent.text not in question:
            return ent.text
    
    return candidate