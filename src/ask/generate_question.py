import nltk
import spacy





nlp = spacy.load("en_core_web_sm")

# sentence = "The Normans were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France."
sentence = "Jackson went to park at 3 pm."
doc = nlp(sentence)

questions = {}

for i in range(len(doc)):
    token = doc[i]
    if token.pos_ == "VERB":
        verb = token
        break


for ent in doc.ents:
    # print(ent.text, ent.start_char, ent.end_char, ent.label_)
    question_type = ""
    if ent.label_ == "PERSON":
        question_type = "Who"

    elif ent.label_ in ["DATE", "TIME"]:
        question_type = "When"

    elif ent.label_ == "LOCATION":
        question_type = "Where"

    if question_type != "":
        if verb.dep_ != "aux" and ent.start_char > 0:
            if verb.tag_ == "VBD":
                question_verb = "did"
            else:
                question_verb = "does"
            q = question_type + " " + question_verb + " " + doc.text[0:ent.start_char].replace(verb.text, verb.lemma_) + doc.text[ent.end_char:].replace(verb.text, verb.lemma_)
        else:
            question_verb = verb.text
            q = question_type + " " + question_verb + doc.text[ent.end_char:].replace(question_verb, "")[1:]

        print(q)
