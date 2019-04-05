import nltk
import spacy


nlp = spacy.load("en_core_web_sm")

questions = [
    "Where did The area correspond to the northern part of present-day Upper Normandy down to the  but the Duchy would eventually extend west beyond the Seine?",

]


def get_question_type(question):
    question = question.lower()

    # TODO: in which year? whom? 
    question_types = ["where", "when", "who"]
    question_index = []

    for q_type in question_types:
        if question.find(q_type) < 0:
            question_index.append(len(question))
        else:
            question_index.append(question.find(q_type))

    question_type = question_types[question_index.index(min(question_index))]

    print(question_type)
    return question_type




def answer(question, candidate):
    question_type = get_question_type(question)
    doc = nlp(candidate)

    if question_type == "where":
        for ent in doc.ents:
            if ent.label_ in ["LOCATION", "GPE"]:
                return ent.text

    elif question_type == "when":
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                return ent.text

    elif question_type == "who":
        for ent in doc.ents:
            if ent.label_ in ["PERSON"]:
                return ent.text

    else:
        return candidate


s = 'The area corresponded to the northern part of present-day Upper Normandy down to the river Seine, but the Duchy would eventually extend west beyond the Seine.'
for question in questions:
    print(answer(question, s))
