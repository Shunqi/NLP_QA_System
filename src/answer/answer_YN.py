from nltk.corpus import wordnet as wn  # import wordnet


# a function to answer yes/no question, s is the original sentence, q is the question
def answer_YN(s, q):
    # count the number of not, 't, no in original sentence
    doc = nlp(s)
    words = ['not', "'n", 'no']
    count = 0  # number of negative words
    JJ_word = []

    for token in doc:
        if token.text.lower() in words:
            count += 1
        if token.tag_ == "JJ":
            JJ_word.append(token.text)  # update the ADJ word in list

    JJ_word_q = []
    doc_q = nlp(q)  # tokenize the question
    for token in doc_q:
        if token.tag_ == "JJ":  # there is an adjective word
            JJ_word_q.append(token.text)
        else:  # there is no adjective word
            if count % 2 == 0:
                return "Yes"
            else:
                return "No"

    for i, word in enumerate(JJ_word_q):
        if word in s:  # if the original sentence contains this word
            if count % 2 == 0:
                return "Yes"
            else:
                return "No"
        else:  # the word is not in the original sentence
            wordnet = word_net(word)
            synonyms = wordnet[0]
            antonyms = wordnet[1]

            if word in synonyms:  # if the words are synonyms
                if count % 2 == 0:
                    return "Yes"
                else:
                    return "No"
            if word in antonyms:  # if the words are antonyms
                if count % 2 == 0:
                    return "No"
                else:
                    return "Yes"