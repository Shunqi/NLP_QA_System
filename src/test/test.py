import sys
sys.path.append('../')
from util.sentence import *
from util.parse_json import parse_json_sentences
from ask.generate_question import *
from answer.answer_question import *

def main():
    sentences = [
        'In 1900, Andrew donated $1 million for the creation of a technical institute for the city of Pittsburgh.'
    ]
    # sentences = parse_json_sentences()[0:50]
    for i in range(0, len(sentences)):
        print('*'*60)
        print('Sentence #' + str(i))
        sentence = sentences[i]
        print(sentence)
        senList1 = extract_bracket(sentence)
        senList = []
        for s in senList1:
            senList += break_simple_and(s)
        sList = []
        qList = []
        aList = []
        for s in senList:
            dep_list, pcfg = stanford_parser(s)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(s)
            sList.append(s)
            temp_qList = []
            temp_aList = []
            question = create_YN(sentence, word_Pos, Pos_word, dep_dict)
            if question != '':
                temp_qList.append(question)
                answer = answer_YN(s, question)
                temp_aList.append(answer)

            question = what_question(s, dep_list, pcfg, word_Pos, dep_dict)
            if question != '':
                temp_qList.append(question)
                answer = answer_what(s, question, dep_list, pcfg, word_Pos, dep_dict)
                temp_aList.append(answer)

            question = create_how(sentence)
            if question != '':
                temp_qList.append(question)
                answer = answer_how(s, question)
                temp_aList.append(answer)

            questions = create_when(sentence)
            if questions != []:
                for q in questions:
                    temp_qList.append(q)
                    answer = answer_when(s, q)
                    temp_aList.append(answer)
            
            qList.append(temp_qList)
            aList.append(temp_aList)

        for i in range(len(sList)):
            # score(sList[i], qList[i], None, None)
            print('S:', sList[i])
            for j in range(len(qList[i])):
                print('Q:', qList[i][j])
                print('A:', aList[i][j])
    

if __name__ == "__main__":
    main()