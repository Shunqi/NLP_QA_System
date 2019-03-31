
# coding: utf-8

# In[1]:


import nltk
import json
import spacy


# In[2]:


#read json file
with open('dev-v2.0.json') as json_data:
    content = json.load(json_data)
    json_data.close()


# In[3]:


#parse json into a list of paragraphs
para = []
for data in content['data']:
    for paragraphs in data['paragraphs']:
        para.append(paragraphs['context'])


# In[4]:


#parse paragraph into list of sentences
def parse_sentences(paragraph): 
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(paragraph.strip())
    return sentences


# In[51]:


parsed_sentenses = parse_sentences(text)


# In[337]:


nlp = spacy.load("en_core_web_lg")


# In[253]:


parag1 = []
for data in content['data']:
    for paragraphs in data['paragraphs']:
        for qas in paragraphs['qas']:
            question = qas['question']
            if 'HOW MUCH' in question.upper() and not qas['is_impossible']:
                parag1.append(paragraphs['context'])
                print(question)
                print(paragraphs['context'])


# In[ ]:


##How Many questions:
    #Question Type1 : Subj + verb + number + noun
    #Question Type2 : There is/are + number + noun + in + place
    #Question type3: noun + with + number + noun phrase
    #被动句


# In[191]:


def get_nsubj(sentence):
    doc = nlp(sentence)
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            return chunk.text


# In[414]:


def get_ROOT(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'ROOT':
            return token.text, token.lemma_,token.tag_


# In[416]:


get_ROOT(txt)


# In[122]:


def get_entity(sentences):
    entity = []
    doc = nlp(sentences)
    for ent in doc.ents:
        entity.append( ent.label_)
    return entity


# In[214]:


def get_namechunks(sentence):
    chunks = {}
    doc = nlp(sentence)
    for chunk in doc.noun_chunks:
        chunks[chunk.text] = chunk.root.text
        #chunks.append(chunk.text)
    return chunks


# In[425]:


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


# In[421]:


def gen_question_type1(sentence):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    obj = ''
    for chunk in get_namechunks(sentence).keys():
        #print(chunk)
        if 'CARDINAL' in get_entity(chunk) or 'QUANTITY' in get_entity(chunk):
            obj = get_namechunks(sentence)[chunk]
            #obj = chunk.split()[-1]
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'CARDINAL' in get_entity(pp) or 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp):
                    prep = pp
            if pp.upper().split()[0] == 'IN' and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp
                    
    if subj != None:
        return "How many "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'
    else:
        return "How many "+obj+" were "+root[0].lower()+' '+prep.lower()+' '+loc+'?'


# In[419]:


def gen_question_type2(sentence):
    obj = ''
    for chunk in get_namechunks(sentence).keys():
        if 'CARDINAL' in get_entity(chunk) or 'QUANTITY' in get_entity(chunk):
            obj = get_namechunks(sentence)[chunk]
    prep = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] == 'IN' and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    prep = pp

    return "How many "+obj+" are there "+prep.lower()+'?'


# In[420]:


def gen_question_type3(sentence):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    obj = ''
    for chunk in get_namechunks(sentence).keys():
        if 'CARDINAL' in get_entity(chunk) or 'QUANTITY' in get_entity(chunk):
            obj = get_namechunks(sentence)[chunk]

            #obj = chunk.split()[-1]
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'CARDINAL' in get_entity(pp) or 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp):
                    prep = pp
            if pp.upper().split()[0] == 'IN' and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp
    return "How much "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'


# In[237]:


def get_pps(sentence):
    doc = nlp(sentence)
    pps = []
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
    return pps


# In[393]:


temp = dep_dict.get("ROOT")
root_word = temp[0]  # the root word
verb = temp[1]  # the pos tag of the root word

# find the original word in word_Pos dict
verb_s = word_Pos.get(root_word)[0]


# In[408]:


txt = "Each year, the southern California area has about 10,000 earthquakes"


# In[409]:


txt2 ="In southern California there are also twelve cities with more than 200,000 residents and 34 cities over 100,000 in population."


# In[410]:


txt3 = "Booth donated $300 million to the university's Booth School of Business"


# In[422]:


gen_question_type2(txt2)


# In[423]:


gen_question_type1(txt)


# In[424]:


gen_question_type3(txt3)


# In[145]:


for sentence in parsed_sentense:
    for chunk in get_namechunks(sentence):
        if 'CARDINAL' in get_entity(chunk):
            #print(chunk+'\n'+sentence)
            start = sentence.find(chunk)
            end = sentence.find(chunk) + len(chunk)
            print(chunk+'\n'+sentence[0:start]+'\n'+sentence[end:])
            print(get_entity(sentence[0:start]))
            print(get_entity(sentence[end:]))
            

