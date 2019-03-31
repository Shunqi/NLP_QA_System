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

    tokens = nlp(sentence)

    for x in tokens:
        x = str(x)
        if x in be_words:  # find the first verb and return the sentence
            sentence = sentence.replace(str(tokens[-1]), "")
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
    first_word = str(tokens[0])
    first_word_tag = word_Pos.get(first_word)[2]  # the tag of the first word

    if first_word_tag != "NNP" and first_word_tag != "PRP":
        first_word_lower = first_word.lower()
        sentence = sentence.replace(first_word, first_word_lower)
    # replace the verb with original word
    sentence = sentence.replace(verb, verb_s)
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