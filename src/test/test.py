import sys
import traceback
sys.path.append('../')
from util.sentence import *
from util.parse_json import *
from ask_func.generate_question import *
from ask_func.rank import *
from answer_func.answer_question import *
from ask_func.rank_questions import *

def remove_clause_test():
    # paragraphs = open_txt('a7.txt')
    # sentences = tokenize_sentence(paragraphs)
    sentences = [
        'He accepted the role on advice from Ian Hart, the man who was cast as Quirrell, who told him that Professor Lupin was "the best part in the book.".'
    ]
    for i in range(0, len(sentences)):
        print('*'*60)
        print('Sentence #' + str(i))
        print('Sentence #' + str(i), file=sys.stderr)
        sentence = sentences[i]
        print(sentence)
        senList1 = extract_bracket(sentence)
        senList2 = []
        for s in senList1:
            senList2 += break_simple_andbut(s, 'but')
        senList = []
        for s in senList2:
            senList += break_simple_andbut(s, 'and')
        sList = []
        qList = []
        aList = []
        for sen in senList:
            dep_list, pcfg = stanford_parser(sen)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(sen)
            pcfg.pretty_print()
            remove = None
            for s in pcfg.subtrees():
                if s.label() == 'SBAR':
                    remove = s.leaves()
                    break
            print(remove)
            if remove != None:
                remove_s = ' '.join(x for x in remove)
                remove_s = remove_s.replace('`` ', '"')
                remove_s = remove_s.replace(" ''", '"')
                remove_s = remove_s.replace(" ,", ',')
                remove_s = remove_s.replace(" .", '.')
                remove_s = ', ' + remove_s + ','
                index = sen.find(remove_s)
                if index == -1:
                    remove_s = remove_s[:len(remove_s)-1]
                    index = sen.find(remove_s)
                    if index == -1:
                        remove_s = remove_s[2:]
                print(remove_s)
                new_s = sen.replace(remove_s, '')
                print(new_s)
            else:
                print(sen)

def test_what():
    paragraphs = open_txt('../../data/Development_data/set1/a4.txt')
    sentences = tokenize_sentence(paragraphs)
    sentences = [
        "Often, Middle, and Late Egyptian were all written using both the hieroglyphic and hieratic scripts."
    ]
    for i in range(0, 1):
        print('*'*60)
        print('Sentence #' + str(i))
        print('Sentence #' + str(i), file=sys.stderr)
        sentence = sentences[i]
        print(sentence)
        senList1 = extract_bracket(sentence)
        senList2 = []
        for s in senList1:
            senList2 += break_simple_andbut(s, 'but')
        senList = []
        for s in senList2:
            senList += break_simple_andbut(s, 'and')
        sList = []
        qList = []
        aList = []
        for s in senList:
            dep_list, pcfg = stanford_parser(s)
            s = remove_clause(s, pcfg)
            dep_list, pcfg = stanford_parser(s)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(s)

            sList.append(s)
            temp_qList = []
            temp_aList = []

            question = what_question(s, dep_list, pcfg, word_Pos, dep_dict)
            if question != '':
                question = format_question(question)
                temp_qList.append(question)
            
            qList.append(temp_qList)

        for i in range(len(sList)):
            print('S:', sList[i])
            for j in range(len(qList[i])):
                print('Q:', qList[i][j])

def test_match():
    paragraphs = open_html('../../data/Development_data/set1/a1.htm')
    sentences = tokenize_sentence(paragraphs)
    questions = [
        'What is the Old Kingdom?', 'What is the basic justification for a separation between the two periods?',
        'What did they also perceive?'
    ]
    
    for k in range(len(questions)):
        question = questions[k]
        scoreList = []
        for i in range(0, len(sentences)):
            print('*'*60)
            print('Sentence #' + str(i))
            print('Sentence #' + str(i), file=sys.stderr)
            sentence = sentences[i]
            # print(sentence)
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
                similarity = score(s, question, None, None)
                scoreList.append((similarity, s))
        scoreList.sort(reverse=True)

        for i in range(10):
            print(scoreList[i][0], scoreList[i][1])

# def question_type(question):
#     question = question.lower()

#     # TODO: in which year? whom? 
#     question_types = ["where", "when", "who", "what", "how"]
#     question_index = []
#     q_word = question.split(' ')[0]
#     if q_word not in question_types:
#         return "yn"
#     else:
#         for q_type in question_types:
#             if question.find(q_type) < 0:
#                 question_index.append(len(question))
#             else:
#                 question_index.append(question.find(q_type))
#         question_type = question_types[question_index.index(min(question_index))]
#         # print(question_type)
#         return question_type

# def test_answer():
#     questions = read_questions('questions_a1.txt')
#     paragraphs = open_txt('../../data/Development_data/set1/a1.txt')
#     sentences = tokenize_sentence(paragraphs)
#     aList = []
#     sList = []
#     for k in range(10):
#         question = questions[k]
#         scoreList = []
#         for i in range(0, len(sentences)):
#             print('Sentence #' + str(i), file=sys.stderr)
#             sentence = sentences[i]
#             # senList1 = extract_bracket(sentence)
#             # senList2 = []
#             # for s in senList1:
#             #     senList2 += break_simple_andbut(s, 'but')
#             senList = [sentence]
#             # for s in senList2:
#             #     senList += break_simple_andbut(s, 'and')
#             for s in senList:
#                 similarity = score(s, question, None, None)
#                 scoreList.append((similarity, s))
            
#         scoreList.sort(reverse=True)
#         q_type = question_type(question)
#         s = scoreList[0][1]
#         answer = ''
#         if q_type == "yn":
#             answer = answer_YN(s, question)
#         elif q_type == "what":
#             answer = answer_what(s, question)
#         elif q_type == "how":
#             answer = answer_how(s, question)
#         else:
#             answer = answer_when(s, question)
#         aList.append(answer)
#         sList.append(s)
    
    # for i in range(10):
    #     print('*'*60)
    #     print('Q:', questions[i])
    #     print('A:', aList[i])
    #     print('S:', sList[i])
        

def main():
    # paragraphs = open_html('../../data/Development_data/set1/a1.htm')
    paragraphs = open_txt('../../data/Development_data/set1/a2.txt')
    sentences = tokenize_sentence(paragraphs)[:50]
    # outputfile = open('questions_a2.txt', 'w')
    # sentences = [
    #     "Recent reexamination of evidence has led Egyptologist Vassil Dobrev to propose that the Sphinx had been built by Djedefra as a monument to his father Khufu."
    # ]
    # sentences = parse_json_sentences()[0:50]
    for i in range(0, len(sentences)):
        print('*'*60)
        print('Sentence #' + str(i))
        print('Sentence #' + str(i), file=sys.stderr)
        sentence = sentences[i]
        print(sentence)
        senList1 = extract_bracket(sentence)
        senList2 = []
        for s in senList1:
            senList2 += break_simple_andbut(s, 'but')
        senList = []
        for s in senList2:
            senList += break_simple_andbut(s, 'and')
        sList = []
        qList = []
        aList = []
        for s in senList:
            dep_list, pcfg = stanford_parser(s)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(s)
            s = remove_clause(s, pcfg)

            sList.append(s)
            temp_qList = []
            temp_aList = []
            question = create_YN(s, word_Pos, Pos_word, dep_dict)
            if question != '':
                temp_qList.append(question)
                # answer = answer_YN(s, question)
                # temp_aList.append(answer)

            question = what_question(s, dep_list, pcfg, word_Pos, dep_dict)
            if question != '':
                temp_qList.append(question)
                # answer = answer_what(s, question, dep_list, pcfg, word_Pos, dep_dict)
                # temp_aList.append(answer)

            question = create_how(s)
            if question != '':
                temp_qList.append(question)
                # answer = answer_how(s, question)
                # temp_aList.append(answer)

            questions = create_when(s)
            if questions != []:
                for q in questions:
                    temp_qList.append(q)
                    # answer = answer_when(s, q)
                    # temp_aList.append(answer)
            
            qList.append(temp_qList)
            # aList.append(temp_aList)

        for i in range(len(sList)):
            # score(sList[i], qList[i], None, None)
            print('S:', sList[i])
            for j in range(len(qList[i])):
                print('Q:', qList[i][j])
                # print(qList[i][j], file=outputfile)
                # print('A:', aList[i][j])
    # outputfile.close()
    
def test_ask():
    n = 10
    paragraphs = open_txt('../../data/Development_data/set3/a5.txt')
    sentences = tokenize_sentence(paragraphs)
    sentences = select_sentence(sentences, n)
    # sentences = [
    #     "This experience is what inspired Ash into becoming a Pokémon trainer."
    # ]
    y_n_list = []
    what_list = []
    who_list = []
    when_list = []
    where_list = []
    how_list = []
    for i in range(0, len(sentences)):
        print('Sentence #' + str(i), file=sys.stderr)
        sentence = sentences[i]
        print(sentence)
        senList = []
        try:
            senList1 = extract_bracket(sentence)
            senList2 = []
            for s in senList1:
                senList2 += break_simple_andbut(s, 'but')
            for s in senList2:
                senList += break_simple_andbut(s, 'and')
        except:
            traceback.print_exc()
        sList = []
        qList = []
        aList = []

        word_Pos, Pos_word, NER, dep_dict = Spacy_parser(sentence)
        try:
            question, tag = create_YN(sentence, word_Pos, Pos_word, dep_dict)
            question = format_question(question)
            y_n_list.append((question, tag))
        except:
            traceback.print_exc()


        for s in senList:
            dep_list, pcfg = stanford_parser(s)
            s = remove_clause(s, pcfg)
            dep_list, pcfg = stanford_parser(s)
            word_Pos, Pos_word, NER, dep_dict = Spacy_parser(s)

            try:
                question = what_question(s, dep_list, pcfg, word_Pos, dep_dict)
                if question != '':
                    question = format_question(question)
                    what_list.append(question)
            except:
                traceback.print_exc()

            try:
                question = create_how(s)
                if question != '':
                    question = format_question(question)
                    how_list.append(question)
            except:
                traceback.print_exc()

            try:
                questions = create_when(s)
                if questions != []:
                    for qt in questions:
                        question = qt[0]
                        tag = qt[1]
                        qtype = qt[2]
                        question = format_question(question)
                        if qtype == 'Who':
                            who_list.append((question, tag))
                        elif qtype == 'When':
                            when_list.append((question, tag))
                        else:
                            where_list.append((question, tag))
            except:
                traceback.print_exc()

    # print(y_n_list)
    # print(what_list)
    # print(who_list)
    # print(when_list)
    # print(where_list)
    # print(how_list)
    qList = question_rank(n, y_n_list, what_list, who_list, when_list, where_list, how_list)
    for i in range(len(qList)):
        print(qList[i])

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

def test_answer():
    questions = read_questions('questions_a1.txt')
    paragraphs = open_txt('../../data/Development_data/set3/a5.txt')
    sentences = tokenize_sentence(paragraphs)
    aList = []
    tList = []
    for k in range(len(questions)):
        print('Question' + str(k))
        question = questions[k]
        q_type = question_type(question)
        answer = ''
        target = ''
        if len(question.split()) > 7:
            # scoreList = []
            # for i in range(0, len(sentences)):
            #     sentence = sentences[i]
            #     similarity = score_spacy(sentence, question)
            #     print(similarity)
            #     scoreList.append((similarity, sentence))
                
            # scoreList.sort(reverse=True)
            # q_type = question_type(question)
            # s = scoreList[0][1]
            # answer = s
            answer = score_short(sentences, question)
        else:
            answer = score_short(sentences, question)
            
        target = answer
        tList.append(target)
        if q_type == "yn":
            answer = answer_YN(answer, question)
        elif q_type == "what":
            answer = answer_what(answer, question)
        elif q_type == "how":
            answer = answer_how(answer, question)
        else:
            answer = answer_when(answer, question)
        aList.append(answer)
    
    for i in range(len(questions)):
        print(questions[i])
        print(tList[i])
        print(aList[i])

if __name__ == "__main__":
    # main()
    # test_what()
    # test_match()
    # remove_clause()
    # test_ask()
    test_answer()