# input should be a sentence
def Spacy_parser(sentence):
    from collections import Counter
    import spacy
    import pandas as pd
    # from tabulate import tabulate

    word_Pos = {}
    Pos_word = {}
    dep_dict = {}  # dict for dependency
    NER = []

    nlp = spacy.load('en_core_web_lg')

    doc = nlp(sentence)
    for ent in doc.ents:
        NER.append([ent.text, ent.label_])

    for token in doc:
        # print(token.text, token.dep_, token.head.text, token.head.pos_, token.tag_, [child for child in token.children])
        # result.append([token.text, token.dep_, token.pos_, token.tag_, [child for child in token.children]])

        # update the dict with the word as key
        word_Pos.update({token.text: [token.lemma_, token.pos_, token.tag_, [child for child in token.children]]})

        # update the dependency dict
        dep_dict.update({token.dep_: [token.text, token.tag_]})

        # update the dict with the Pos tag as key
        if token.tag_ not in Pos_word:
            Pos_word.update({token.tag_: token.text})
        else:
            temp = []
            value = Pos_word.get(token.tag_)
            if isinstance(value, list):  # check if the value is a list
                temp.extend(Pos_word.get(token.tag_))
            else:
                temp.append(Pos_word.get(token.tag_))
            temp.append(token.text)
            Pos_word.update({token.tag_: temp})

    return word_Pos, Pos_word, NER, dep_dict


# In[242]:


result = Spacy_parser("Mary walks to school today.")
print(result[0])
print(result[1])
print(result[2])
print(result[3])


# # YES/NO question

# the inputs are the original sentence and its POS tag list
def create_YN(sentence, word_Pos, Pos_word, dep_dict):
    '''
    retract the VERB pos and check if it's be verb (is, are, were, was)
    If not, add does/did/do at the beginning
    Add question mark at the end

    MD  Modal verb (can, could, may, must)
    VB  Base verb (take)
    VBC Future tense, conditional
    VBD Past tense (took)
    VBF Future tense
    VBG Gerund, present participle (taking)
    VBN Past participle (taken)
    VBP Present tense (take)
    VBZ Present 3rd person singular (takes)
    '''
    result = ""  # the string to return
    tense = ""  # the tense of the sentence
    be_words = ['is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may', 'will', 'would', 'have', 'had', 'has']

    for x in be_words:
        if x in word_Pos:
            sentence = sentence.replace(x + " ", "")
            result = x.capitalize() + " " + sentence + "?"
            return result

    # there is no be_words, check what is the tense of the sentence
    temp = dep_dict.get("ROOT")
    root_word = temp[0]  # the root word
    verb = temp[1]  # the pos tag of the root word

    # find the original word in word_Pos dict
    verb_s = word_Pos.get(root_word)[0]

    # check the type of first word, if it's not proper noun, convert to lower case
    nlp = spacy.load('en_core_web_lg')
    tokens = nlp(sentence)
    first_word = tokens[0]
    print(first_word)
    print(word_Pos.get(first_word)[2])

    if word_Pos.get(first_word)[2] != "NNP":
        first_word_lower = first_word.lower()
        sentence = sentence.replace(first_word, first_word_lower)

    # the verb is present third person singular
    if verb == 'VBZ':
        sentence = sentence.replace(verb, verb_s)
        result = "Does " + sentence + "?"

    '''
    if verb_s in ['VBP','VBG','VB']:
        #tense = "present"


    if verb_s in ['VBF','VBC']:
        #tense = "future"

    if verb_s in ['VBD','VBN']:
        #tense = "past" 
    '''

    return result

print(create_YN("Mary walks to school today.", result[0], result[1], result[3]))
