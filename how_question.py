
# coding: utf-8

# In[21]:


import nltk
import json
import spacy
import re, urllib, json
from bs4 import BeautifulSoup


# In[2]:


# #read json file
# with open('dev-v2.0.json') as json_data:
#     content = json.load(json_data)
#     json_data.close()

# #parse json into a list of paragraphs
# para = []
# for data in content['data']:
#     for paragraphs in data['paragraphs']:
#         para.append(paragraphs['context'])

# #parse paragraph into list of sentences
# def parse_sentences(paragraph): 
#     sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#     sentences = sent_detector.tokenize(paragraph.strip())
#     return sentences

# squad_sentences = []
# for p in para:
#     squad_sentences += parse_sentences(p)


# In[3]:


# for s in squad_sentences:
#      if 'CARDINAL' in get_entity(s) or 'QUANTITY' in get_entity(s):
#             print(s)


# In[4]:


nlp = spacy.load("en_core_web_lg")


# In[5]:


def countable_noun(noun):
    url = 'https://books.google.com/ngrams/graph?content=many+' + noun + '%2C+much+' + noun + '&year_start=1800&year_end=2000'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    try:
        many_data = json.loads(re.search('\{"ngram": "many ' + noun + '".*?\}', html).group(0))['timeseries']
        many = sum(many_data) / float(len(many_data))
    except:
        many = 0.0
    try:
        much_data = json.loads(re.search('\{"ngram": "much ' + noun + '".*?\}', html).group(0))['timeseries']
        much = sum(much_data) / float(len(much_data))
    except:
        much = 0.0
    if many > much:
        return True
    return False


# In[41]:


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


# In[42]:


def gen_question_type1(sentence,obj):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp): #'CARDINAL' in get_entity(pp) or
                    prep = pp
            if (pp.upper().split()[0] == 'IN' or pp.upper().split()[0] == 'ON' or pp.upper().split()[0] == 'AT') and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp
                    
    if subj != None:
        return "How many "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'
    else:
        return "How many "+obj+" were "+root[0].lower()+' '+prep.lower()+' '+loc+'?'


# In[43]:


def gen_question_type2(sentence,obj):
    prep = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] == 'IN' and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    prep = pp

    return "How many "+obj+" are there "+prep.lower()+'?'


# In[50]:


def gen_question_type3(sentence,obj):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    if obj == '' and root == '' :
        return ''
    if obj == '' and subj == '' :
        return ''
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'CARDINAL' in get_entity(pp) or 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp):
                    prep = pp
            if (pp.upper().split()[0] == 'IN' or pp.upper().split()[0] == 'ON') and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp

    return "How much "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'


# In[52]:


def select_question(sentence):
    obj = ''
    for chunk in get_namechunks(sentence).keys():
        if 'CARDINAL' in get_entity(chunk) or 'QUANTITY' in get_entity(chunk):
            obj = get_namechunks(sentence)[chunk]

    if obj == '':
        return gen_question_type3(sentence, obj)
    
    if countable_noun(obj):
        if 'there' in sentence.lower():
            return gen_question_type2(sentence, obj)
        else:
            return gen_question_type1(sentence, obj)
    else:
        return gen_question_type3(sentence, obj)


# In[22]:


def open_html(filename):
    soup = BeautifulSoup(open(filename,encoding='utf-8'), "html.parser")
    page = soup.find_all('p')
    paragraphs = ''
    for p in page:
        paragraphs += p.getText()
    return paragraphs

def parse_sentences(paragraph): 
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(paragraph.strip())
    return sentences


# In[24]:


paragraphs = open_html("a2.htm")


# In[53]:


for sentence in parse_sentences(paragraphs):
    #print(sentence)
    print(select_question(sentence))

