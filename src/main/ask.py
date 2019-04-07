#!/usr/bin/env python3
import sys
sys.path.append('../')
from util.sentence import *
from util.parse_json import *
from ask_func.generate_question import *
from ask_func.rank import *

def main():
    article_file = sys.argv[1]
    nquestions = int(sys.argv[2])
    # paragraphs = open_txt('../../data/Development_data/set1/a1.txt')
    paragraphs = open_txt(article_file)
    sentences = tokenize_sentence(paragraphs)
    count = 0
    qList = []
    logfile = open('log.txt', 'w')
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        print(sentence, file=logfile)
        senList1 = extract_bracket(sentence)
        senList2 = []
        for s in senList1:
            senList2 += break_simple_andbut(s, 'but')
        senList = []
        for s in senList2:
            senList += break_simple_andbut(s, 'and')
        
        for s in senList:
            dep_list, pcfg = stanford_parser(s)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(s)
            temp_qList = []
            question = create_YN(s, word_Pos, Pos_word, dep_dict)
            if question != '':
                temp_qList.append(question)

            question = what_question(s, dep_list, pcfg, word_Pos, dep_dict)
            if question != '':
                temp_qList.append(question)

            question = create_how(s)
            if question != '':
                temp_qList.append(question)

            questions = create_when(s)
            if questions != []:
                for q in questions:
                    temp_qList.append(q)
            
            qList += temp_qList
            count = len(qList)

        if count >= nquestions:
            break
    
    for i in range(nquestions):
        print(qList[i])
        

if __name__ == "__main__":
    main()