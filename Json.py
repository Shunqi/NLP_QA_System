
# coding: utf-8

# In[1]:


import nltk
import json
import spacy
from bs4 import BeautifulSoup


# In[2]:


#read SQUAD file
#return 1024 paragraphs
def read_squad(filename):
    with open(filename) as json_data:
        content = json.load(json_data)
        json_data.close()
    #parse json into a list of paragraphs
    para = []
    for data in content['data']:
        for paragraphs in data['paragraphs']:
            para.append(paragraphs['context'])
    return para


# In[3]:


#read the development data from html file
def open_html(filename):
    soup = BeautifulSoup(open(filename), "html.parser")
    page = soup.find_all('p')
    paragraphs = ''
    for p in page:
        paragraphs += p.getText()
    return paragraphs


# In[4]:


#parse paragraph into list of sentences
def parse_sentences(paragraph): 
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(paragraph.strip())
    return sentences


# In[5]:


#read squad file into sentnces
par = read_squad('dev-v2.0.json')
squad_sentences = []
for p in par:
    squad_sentences += parse_sentences(p)


# In[6]:


# parse development document
paragraphs = open_html("a2.htm")
parse_sentences(paragraphs)

