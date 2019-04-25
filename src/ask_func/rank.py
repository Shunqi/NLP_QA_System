import nltk
from nltk import word_tokenize
# from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

#from gensim.scripts.glove2word2vec import glove2word2vec
#from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from util.sentence import *

lemmatizer = WordNetLemmatizer()
# you need to install gensim and download the glove.6b.200d.txt online

# inputs are two sentence, s1 is the question, s2 is the sentence from the text
# the output is the distance between two sentences. When the number is smaller, the two sentences are more similar.
'''
def calculate_distance(s1, s2):
    glove_input_file = 'glove.6B.200d.txt'
    word2vec_output_file = 'glove.6B.200d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)

    # remove stopwords
    s1 = remove_stopwords(s1)
    s2 = remove_stopwords(s2)

    # load the Stanford GloVe model
    filename = 'glove.6B.200d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)

    # calculate distance between two sentences using WMD algorithm
    distance = model.wmdistance(s1, s2)

    return distance
'''

def remove_stopwords(s):
    # remove stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    word_tokens = word_tokenize(s)
    filtered_sentence = [w.strip() for w in word_tokens if w not in stopwords]
    text = " ".join(str(x) for x in filtered_sentence)
    return text

def lemmatize(s):
    # lemmatize sentence
    word_tokens = word_tokenize(s)
    filtered_sentence = [lemmatizer.lemmatize(w.strip()) for w in word_tokens]
    text = " ".join(str(x) for x in filtered_sentence)
    return text


def score_spacy(s, question):
    doc_s = nlp(s)
    doc_q = nlp(question)
    score = doc_s.similarity(doc_q)
    return score

def process_an_sentences(sentences):
    newlist = []
    for s in sentences:
        s = remove_stopwords(s)
        newlist.append(s)
    return newlist

def score_short(sentences, question):
    senf = sentence_frequency(sentences)
    avgl = get_avglenth(sentences)
    question = remove_stopwords(question)
    scoreList = []
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        sentence = remove_stopwords(sentence)
        # similarity = match_words(sentence, question)
        sentence_lemma = lemmatize(sentence)
        question_lemma = lemmatize(question)
        similarity = match_words(sentence_lemma, question_lemma, senf, avgl)
        # print(similarity)
        scoreList.append((similarity, sentences[i]))
        
    scoreList.sort(reverse=True)
    if scoreList[0][0] == 0:
        return None
    s = scoreList[0][1]
    # print(scoreList[0][1], scoreList[0][0])
    # print(scoreList[1][1], scoreList[1][0])
    # print(scoreList[2][1], scoreList[2][0])
    return s

def match_words(s, question, senf, avgl):
    q_words = ['what', 'when', 'which', 'where', 'how', 'who', 'whom', 'much', 'many', 'whose', 'why']
    words = question.split()
    swords = s.split()
    score = 0
    for w in words:
        if len(w) > 1 and w.lower() not in q_words:
            if w in senf:
                score += s.count(w) * 1.0 / senf[w]
            else:
                score += s.count(w) * 1.0 / 5
    score = score / (len(swords) / avgl)
    return score

def get_avglenth(sentences):
    total = 0
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        sentence = remove_stopwords(sentence)
        sentence_lemma = lemmatize(sentence)
        words = sentence.split()
        total += len(words)
    return total * 1.0 / len(sentences)

def get_vocabulary(sentences):
    vocabulary = {}
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        sentence = remove_stopwords(sentence)
        sentence_lemma = lemmatize(sentence)
        words = sentence.split()
        for w in words:
            if w not in vocabulary:
                vocabulary[w] = 0
    return vocabulary

def sentence_frequency(sentences):
    vocabulary = get_vocabulary(sentences)
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        sentence = remove_stopwords(sentence)
        sentence_lemma = lemmatize(sentence)
        words = sentence.split()
        wdic = {}
        for w in words:
            if w not in wdic:
                wdic[w] = 1
        for key, value in wdic.items():
            vocabulary[key] += 1
    return vocabulary