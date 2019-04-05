
# coding: utf-8

# In[1]:


import nltk
import json
import spacy
nltk.download('stopwords')


# In[18]:


nlp = spacy.load("en_core_web_lg")


# In[225]:


q = "How many combinatory and graph theoretical problems, formerly believed to be plagued by intractability, did Karp's paper address?"
sentence = "Reducibility Among Combinatorial Problems, in which he showed that 21 diverse combinatorial and graph theoretical problems, each infamous for its computational intractability, are NP-complete. "


# In[180]:


def get_entity(sentences):
    entity = []
    doc = nlp(sentences)
    for ent in doc.ents:
        entity.append( (ent.text,ent.label_))
    return entity


# In[203]:


#find cardinal entity
#input: sentence
def locate_cardinal(sentence):
    cardinal = []
    for en in get_entity(sentence):
        if en[1] == 'CARDINAL' or en[1] == 'QUANTITY':
            cardinal.append(en[0])
    return cardinal


# In[138]:


def get_lemma(word):
    token = nlp(word)
    lemma = token[0].lemma_
    return lemma


# In[210]:


def calculate_word_distance(lemma, card, sentence):
    sentence_token = nlp(sentence)
    idx = 0
    obj_idx = 0
    card_idx = sentence.find(card)
    for s in sentence_token:
        #print(s.text)
        if s.lemma_ == lemma:
            obj_idx = idx
#         if s.text == card:
#             card_idx = idx
        idx += 1
    if card_idx - obj_idx == 0:
        return 9999
    else:
        return abs(card_idx - obj_idx)


# In[221]:


def answer_how(question, sentence):
    noun = get_noun(question)
    noun_lemma = get_lemma(noun)
    card_list = locate_cardinal(sentence)
    min_dist = 9999
    answer = ''
    for card in card_list:
        #print(card)
        dist = calculate_word_distance(noun_lemma, card, sentence)
        #print(dist)
        if dist < min_dist:
            min_dist = dist
            answer = card
            #print(answer)
    return answer


# In[222]:


def get_noun(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.pos_ == 'NOUN':
            return token.text


# In[226]:


answer_how(q, sentence)

