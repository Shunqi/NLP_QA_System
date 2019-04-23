import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from util.sentence import *


# you need to install gensim and download the glove.6b.200d.txt online

# inputs are two sentence, s1 is the question, s2 is the sentence from the text
# the output is the distance between two sentences. When the number is smaller, the two sentences are more similar.
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

def remove_stopwords(s):
    # remove stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    word_tokens = word_tokenize(s)
    filtered_sentence = [w.strip() for w in word_tokens if w not in stopwords]
    text = " ".join(str(x) for x in filtered_sentence)
    return text

def score(sentence, question, type, replace):
    score = 0
    score += sentence_similarity(sentence, question)
    # print(score)
    return score

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'

    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
    # print(synsets1)
    # print(synsets2)
 
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        socres = []
        for ss in synsets2:
            # print(synset.path_similarity(ss))
            if synset.path_similarity(ss) != None:
                socres.append(synset.path_similarity(ss))
            else:
                socres.append(0.0)
        best_score = max(socres)
 
        # Check that the similarity could have been computed
        if best_score != None:
            score += best_score
            count += 1
 
    # Average the values
    score /= count
    return score

def score_spacy(s, question):
    doc_s = nlp(s)
    doc_q = nlp(question)
    score = doc_s.similarity(doc_q)
    return score

def process_an_sentences(senteces):
    pass

def score_short(s, question):
    pass