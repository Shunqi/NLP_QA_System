# the inputs are the original sentence and its POS tag list
import random


def create_YN(sentence, word_Pos, Pos_word, dep_dict):
    result = ""  # the string to return
    tense = ""  # the tense of the sentence
    be_words = ['is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may', 'will', 'would', 'have', 'had', 'has']

    # the function to change syn and ant words
    Adj_words = []
    # find all the adj words
    if "JJ" in Pos_word:
        temp = Pos_word.get("JJ")
        status = isinstance(temp, list)
        if status == False:
            Adj_words.append(temp)
        else:
            Adj_words.extend(temp)

    print(Adj_words)
    num = random.randint(1, 10)

    # create synonyms and antonyms
    for word in Adj_words:
        print(word)
        wordnet = word_net(word)
        synonyms = wordnet[0]
        antonyms = wordnet[1]

        print(synonyms)
        print(antonyms)

        if num > 5 and antonyms:  # change to antonyms
            sentence = sentence.replace(word, antonyms[0])
        elif 5 >= num and synonyms:  # change to synonyms
            sentence = sentence.replace(word, synonyms[0])

    tokens = nlp(sentence)
    # check the type of first word, if it's not proper noun, convert to lower case
    first_word = str(tokens[0])

    # find the root word
    temp = dep_dict.get("ROOT")
    root_word = temp[0]  # the root word
    verb = temp[1]  # the pos tag of the root word
    if root_word in be_words:
        if first_word != "I":
            first_word_lower = first_word.lower()
            sentence = sentence.replace(first_word, first_word_lower)
        sentence = sentence.replace(str(tokens[-1]), "")
        sentence = sentence.replace(root_word + " ", "")
        result = root_word.capitalize() + " " + sentence + "?"
        return result

    for x in tokens:
        x = str(x)
        if x in be_words:  # find the first verb and return the sentence
            if first_word != "I":
                first_word_lower = first_word.lower()
                sentence = sentence.replace(first_word, first_word_lower)

            sentence = sentence.replace(str(tokens[-1]), "")
            sentence = sentence.replace(x + " ", "")
            result = x.capitalize() + " " + sentence + "?"
            return result

    # there is no be_words, check what is the tense of the sentence
    # find the original word in word_Pos dict
    verb_s = word_Pos.get(root_word)[0]

    first_word_tag = word_Pos.get(first_word)[2]  # the tag of the first word
    print(first_word_tag)

    if first_word_tag != "NNP" and first_word != "I":
        first_word_lower = first_word.lower()
        sentence = sentence.replace(first_word, first_word_lower)
    # replace the verb with original word
    sentence = sentence.replace(root_word, verb_s, 1)
    sentence = sentence.replace(str(tokens[-1]), "")

    # the verb is present third person singular
    if verb == 'VBZ':
        result = "Does " + sentence + "?"

    if verb in ['VBP', 'VBG', 'VB']:
        # tense = "present"
        result = "Do " + sentence + "?"

        '''
    if verb_s in ['VBF','VBC']:
        #tense = "future"
        '''
    if verb in ['VBD', 'VBN']:
        # tense = "past"
        result = "Did " + sentence + "?"

    return result