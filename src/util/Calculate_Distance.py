from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

# you need to install gensim and download the glove.6b.200d.txt online

# inputs are two sentence, s1 is the question, s2 is the sentence from the text
# the output is the distance between two sentences. When the number is smaller, the two sentences are more similar.
def calculate_distance(s1, s2):
    glove_input_file = 'glove.6B.200d.txt'
    word2vec_output_file = 'glove.6B.200d.txt.word2vec'
    glove2word2vec(glove_input_file, word2vec_output_file)

    # load the Stanford GloVe model
    filename = 'glove.6B.200d.txt.word2vec'
    model = KeyedVectors.load_word2vec_format(filename, binary=False)

    # calculate distance between two sentences using WMD algorithm
    distance = model.wmdistance(s1, s2)

    return distance
