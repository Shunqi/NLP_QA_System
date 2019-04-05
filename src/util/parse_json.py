import nltk
import json
import spacy
from bs4 import BeautifulSoup

def parse_json_sentences():
    with open('../../data/dev-v2.0.json') as json_data:
        content = json.load(json_data)
        json_data.close()
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        #parse json into a list of paragraphs
        result = []
        for data in content['data']:
            for paragraphs in data['paragraphs']:
                
                #parse paragraph into list of sentences
                sentences = sent_detector.tokenize(paragraphs['context'].strip())
                result += sentences
        
        return result

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

def open_html(filename):
    soup = BeautifulSoup(open(filename), "html.parser")
    page = soup.find_all('p')
    paragraphs = ''
    for p in page:
        paragraphs += p.getText()
    return paragraphs

def parse_sentences(paragraph): 
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(paragraph.strip())
    return sentences