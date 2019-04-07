#!/usr/bin/env python3
import sys
sys.path.append('../')
from util.sentence import *
from util.parse_json import *
from ask_func.rank import *
from answer_func.answer_question import *

def question_type(question):
    question = question.lower()

    # TODO: in which year? whom? 
    question_types = ["where", "when", "who", "what", "how"]
    question_index = []
    q_word = question.split(' ')[0]
    if q_word not in question_types:
        return "yn"
    else:
        for q_type in question_types:
            if question.find(q_type) < 0:
                question_index.append(len(question))
            else:
                question_index.append(question.find(q_type))
        question_type = question_types[question_index.index(min(question_index))]
        # print(question_type)
        return question_type

def main():
    article_file = sys.argv[1]
    questions_file = sys.argv[2]
    questions = read_questions(questions_file)
    paragraphs = open_txt(article_file)
    # questions = read_questions('questions_a1.txt')
    # paragraphs = open_txt('../../data/Development_data/set1/a1.txt')
    sentences = tokenize_sentence(paragraphs)
    aList = []
    for k in range(len(questions)):
        question = questions[k]
        scoreList = []
        for i in range(0, len(sentences)):
            sentence = sentences[i]
            senList = [sentence]
            for s in senList:
                similarity = score(s, question, None, None)
                scoreList.append((similarity, s))
            
        scoreList.sort(reverse=True)
        q_type = question_type(question)
        s = scoreList[0][1]
        answer = ''
        if q_type == "yn":
            answer = answer_YN(s, question)
        elif q_type == "what":
            answer = answer_what(s, question)
        elif q_type == "how":
            answer = answer_how(s, question)
        else:
            answer = answer_when(s, question)
        aList.append(answer)
    
    for i in range(len(questions)):
        print(aList[i])

if __name__ == "__main__":
    main()