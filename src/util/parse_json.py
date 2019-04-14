import nltk
import json
import spacy
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

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
    with open(filename,  encoding="utf8") as json_data:
        content = json.load(json_data)
        json_data.close()
    #parse json into a list of paragraphs
    para = []
    for data in content['data']:
        for paragraphs in data['paragraphs']:
            para.append(paragraphs['context'])
    return para

def open_html(filename):
    soup = BeautifulSoup(open(filename,  encoding="utf8"), "html.parser")
    page = soup.find_all('p')
    paragraphs = ''
    for p in page:
        paragraphs += p.getText() + ' '
    return paragraphs

def open_txt(filename):
    textfile = open(filename, 'r', encoding="utf8")
    lines_txt = [line.rstrip("\n") for line in textfile]
    textfile.close()
    paragraphs = ''
    end = ['.', '?', '!']
    for line in lines_txt:
        if line == '':
            continue
        if line == 'References':
            break
        if line[len(line)-1] in end:
            paragraphs += line + ' '
    return paragraphs

def tokenize_sentence(paragraph):
    temp = sent_tokenize(paragraph)
    sent_tokenize_list = []
    #handle special cases
    end = ['.', '?', '!']
    i = 0
    while i < len(temp):
        sentence = temp[i]
        words = sentence.split(' ')
        if words[len(words)-1] == 'ca.':
            sentence += ' ' + temp[i + 1]
            i += 1
        if sentence[len(sentence)-1] not in end:
            sentence += '.'
        sent_tokenize_list.append(sentence)
        i += 1
    return sent_tokenize_list

def parse_sentences(paragraph): 
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(paragraph.strip())
    return sentences

def read_questions(filename):
    textfile = open(filename, 'r',  encoding="utf8")
    lines_txt = [line.rstrip("\n") for line in textfile]
    textfile.close()
    return lines_txt