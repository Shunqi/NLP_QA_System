import nltk
import spacy





nlp = spacy.load("en_core_web_sm")

# sentence = "The Normans were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France."
sentence = "Jackson went to Shanghai in the year of 1987."
sentence = "In the 1060s, Robert Crispin led the Normans of Edessa against the Turks."
# sentence = "I was in Shanghai."
doc = nlp(sentence)

nsubj = ""
for chunk in doc.noun_chunks:
    if chunk.root.dep_ == "nsubj":
        nsubj = chunk.text

questions = {}

for i in range(len(doc)):
    token = doc[i]
    if token.pos_ == "VERB":
        verb = token
        break


for ent in doc.ents:
    # print(ent.text, ent.start_char, ent.end_char, ent.label_)
    question_type = ""
    start_char = 0
    end_char = 0

    if ent.label_ == "PERSON":
        question_type = "Who"
        start_char = ent.start_char
        end_char = ent.end_char

    elif ent.label_ in ["DATE", "TIME"]:
        question_type = "When"
        start_char = doc.text[0:ent.start_char - 1].rfind(" ") + 1
        end_char = ent.end_char

    elif ent.label_ in ["LOCATION", "GPE"]:
        question_type = "Where"
        start_char = doc.text[0:ent.start_char - 1].rfind(" ") + 1
        end_char = ent.end_char


    if question_type != "":
        # print(ent.text, nsubj)
        if verb.dep_ != "aux" and ent.text != nsubj:
            if verb.tag_ == "VBD":
                question_verb = "did"
            else:
                question_verb = "does"
            q = question_type + " " + question_verb + " " + doc.text[0:start_char].replace(verb.text, verb.lemma_) + doc.text[end_char:].replace(verb.text, verb.lemma_)[1:]
        else:
            question_verb = verb.text
            q = question_type + " " + question_verb + " " + doc.text[0:start_char] + doc.text[end_char:].replace(question_verb, "")[2:]

        print(q)
