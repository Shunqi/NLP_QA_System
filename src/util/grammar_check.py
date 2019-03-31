import spacy

nlp = spacy.load("en_core_web_sm")

def check_sentence(sentence):
    sentence = check_space(sentence)
    sentence = check_question_mark(sentence)
    return sentence

def check_space(sentence):
    words = sentence.split(" ")
    words = [word for word in words if word != ""]
    return " ".join(words)

def check_question_mark(sentence):
    if sentence[-1].isalnum() :
        return sentence + "?"
    else:
        return sentence[:-1] + "?"
