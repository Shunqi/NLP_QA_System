import random
# n is the number of questions from command line
def question_rank(n, y_n_list, what_list, who_list, when_list, where_list, how_many_list, how_much_list):
    count = 0
    result_question = []

    tough_max = int(n * 0.5)
    # assign 50% to tough questions
    # 1 is tough question and 0 easy question

    # generate hard question list for yes and where/ when/ who/
    y_n_temp = generate_hard(y_n_list)
    hard_y_n = y_n_temp[0]
    easy_y_n = y_n_temp[1]

    where_temp = generate_hard(where_list)
    hard_where = where_temp[0]
    easy_where = where_temp[1]

    when_temp = generate_hard(when_list)
    hard_when = when_temp[0]
    easy_when = when_temp[1]

    who_temp = generate_hard(who_list)
    hard_who = who_temp[0]
    easy_who = who_temp[1]

    # include only hard questions up to 50% of n
    while count <= tough_max:
        result_question, result1 = include_q(result_question, hard_y_n)
        if result1 == True:
            print("tough q is " + str(count))
            count += 1
        if count == tough_max:
            break

        result_question, result2 = include_q(result_question, hard_where)
        if result2 == True:
            print("tough q is " + str(count))
            count += 1
        if count == tough_max:
            break

        result_question, result3 = include_q(result_question, hard_when)
        if result3 == True:
            print("tough q is " + str(count))
            count += 1
        if count == tough_max:
            break

        result_question, result4 = include_q(result_question, hard_who)
        if result4 == True:
            print("tough q is " + str(count))
            count += 1
        if count == tough_max:
            break

    # start to include easy questions
    while count <= n:
        result_question, result5 = include_q(result_question, how_many_list)
        if result5 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result6 = include_q(result_question, how_much_list)
        if result6 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result7 = include_q(result_question, what_list)
        if result7 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result8 = include_q(result_question, easy_y_n)
        if result8 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result9 = include_q(result_question, easy_where)
        if result9 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result10 = include_q(result_question, easy_when)
        if result10 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

        result_question, result11 = include_q(result_question, easy_who)
        if result11 == True:
            print("easy q is " + str(count))
            count += 1
        if count == n:
            break

    # return the list of questions
    return result_question

#functin to generate hard and easy question lists
def generate_hard(q_list):
    hard = []
    easy = []
    for q in q_list:
        if q[1] == 1:
            hard.append(q[0])
        else:
            easy.append(q[0])
    return hard, easy

def include_q(result_question, hard_list):
    # if the hard_y_n is not empty
    if hard_list:
        temp = random.choice(hard_list)
        if temp not in result_question:
            result_question.append(temp)
            return result_question, True
        return result_question, False