import sys
sys.path.append('../')
from util.sentence import *
from util.parse_json import parse_json_sentences
import random
from answer_func.answer_question import *

def create_YN(sentence, word_Pos, Pos_word, dep_dict):
    tag = 0 # 0 is easy and 1 is hard
    result = ""  # the string to return
    tense = ""  # the tense of the sentence
    be_words = ['cannot', 'is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may', 'will', 'would', 'have',
                'had', 'has']

    tokens = nlp(sentence)

    # check the type of first word, if it's not proper noun, convert to lower case
    first_word = str(tokens[0])
    while (first_word == " "):
        sentence = sentence.replace(first_word, "", 1)
        tokens = tokens[1:]
        first_word = str(tokens[0])

    if str(tokens[-1]) == '.':
        sentence = sentence.replace(str(tokens[-1]), "")

    first_word_tag = word_Pos.get(first_word)[2]  # the tag of the first word

    # the function to change syn and ant words
    Adj_words = []
    # find all the adj words
    if "JJ" in Pos_word:
        temp = Pos_word.get("JJ")
        status = isinstance(temp, list)
        if status == False:
            Adj_words.append(temp)
        else:
            Adj_words.extend(temp)

    # create synonyms and antonyms
    for word in Adj_words:
        wordnet = word_net(word)
        synonyms = wordnet[0]
        antonyms = wordnet[1]

        if antonyms:  # change to antonyms
            sentence = sentence.replace(word, antonyms[0])
            tag = 1
        elif synonyms:  # change to synonyms
            sentence = sentence.replace(word, synonyms[0])

    if first_word_tag != "NNP" and first_word != "I":
        first_word_lower = first_word.lower()
        sentence = sentence.replace(first_word, first_word_lower)

    # find the root word
    temp = dep_dict.get("ROOT")
    root_word = temp[0]  # the root word
    verb = temp[1]  # the pos tag of the root word
    if root_word in be_words:
        sentence = sentence.replace(root_word + " ", "")
        if root_word == "cannot":
            root_word = "can"
        result = root_word.capitalize() + " " + sentence + "?"
        return result

    for x in tokens:
        x = str(x)
        if x in be_words:  # find the first verb and return the sentence
            if "cannot" in sentence and x == 'can':
                sentence = sentence.replace("cannot" + " ", "")
            sentence = sentence.replace(x + " ", "")
            result = x.capitalize() + " " + sentence + "?"
            return result

    # there is no be_words, check what is the tense of the sentence
    # find the original word in word_Pos dict
    verb_s = word_Pos.get(root_word)[0]

    # replace the verb with original word
    sentence = sentence.replace(root_word, verb_s, 1)

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

    return result, tag

def what_question(sentence, dependency, pas, word_Pos, dep_dict):
    be_words = ['cannot', 'is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may', 'will', 'would', 'have',
                'had', 'has']
    neg_rb = ['however', 'but', 'yet', 'often']
    doc = nlp(sentence)
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)
    # there is no be_words, check what is the tense of the sentence
    temp = dep_dict.get("ROOT")
    root_word = temp[0]  # the root word
    tag = temp[1]  # the pos tag of the root word
    # print(root_word)
    # dependency, pas = stanford_parser(sentence)
    # print(dependency)
    # pas.pretty_print()

    keyword = ''
    copula = ''
    verb = ''
    aux = ''
    auxpass = ''
    keyword_tag = ''
    for i in range(len(dependency)):
        # print(dependency[i])
        if (dependency[i][1] == 'cop'):
            keyword = dependency[i][0][0]
            copula = dependency[i][2][0]
            keyword_tag = dependency[i][0][1]
            break
    if keyword == '':
        for i in range(len(dependency)):
            # print(dependency[i])
            if (dependency[i][1] == 'dobj'):
                keyword = dependency[i][2][0]
                verb = dependency[i][0][0]
                keyword_tag = dependency[i][2][1]
                break

    if copula == '' and verb != root_word and root_word != keyword and 'VB' in tag:
        keyword = ''
    if keyword == '':
        verb = root_word
    if keyword != '' and copula != '' and verb == '' and root_word != copula:
        verb = root_word
    # print(keyword, copula, verb, root_word)

    if verb != '':
        temp_list = sentence.split()
        if temp_list[len(temp_list)-1][:-1] == verb or (temp_list[len(temp_list)-1] == '.' and temp_list[len(temp_list)-2] == verb):
            return ''

    question_type = "What"
    if keyword != '':
        for ent in doc.ents:
            if keyword in ent.text:
                if ent.label_ == "PERSON":
                    question_type = "Whom"
                elif ent.label_ in ["DATE", "TIME"]:
                    question_type = "When"
                elif ent.label_ in ["LOCATION", "GPE"]:
                    question_type = "Where"
                break

    for i in range(len(dependency)):
        if dependency[i][1] == 'aux':
            aux = dependency[i][2][0]
            break
    if verb != '':
        for i in range(len(dependency)):
            if (dependency[i][1] == 'auxpass' and verb == dependency[i][0][0]):
                auxpass = dependency[i][2][0]
                break

    keyphrase = None
    if keyword != '':
        if 'VB' in keyword_tag:
            label = 'VP'
        else:
            label = 'NP'
        for s in pas.subtrees():
            # s.pretty_print()
            # print(s.label())
            # print(s.leaves())
            if s.label() == label and keyword in s.leaves() and keyphrase == None:
                keyphrase = s.leaves()
    elif verb != '':
        for s in pas.subtrees():
            if s.label() == 'VP' and verb in s.leaves() and keyphrase == None:
                keyphrase = s.leaves()
    # print(keyphrase)
    if keyphrase is None:
        return ''

    keyphrase = ['"' if x == '``' or x == "''" else x for x in keyphrase]

    sentence = lower_firstword(sentence, word_Pos)

    location_or_time = find_first_comma(doc, word_Pos, sentence, verb, copula)
    # print(location_or_time)

    if verb != '' and keyword != '':
        # find the original word in word_Pos dict
        verb_s = ''
        tag = ''
        if '-' in verb:
            verb_temp = verb.split('-')
            if word_Pos.get(verb_temp[1]) == None:
                return ''
            verb_s = word_Pos.get(verb_temp[1])[0]
            verb_s = verb_temp[0] + '-' + verb_s
            tag = word_Pos.get(verb_temp[1])[2]
        else:
            if word_Pos.get(verb) == None:
                return ''
            verb_s = word_Pos.get(verb)[0]
            tag = word_Pos.get(verb)[2]

        length = len(keyphrase)
        keyphrase_s = ' '.join(x for x in keyphrase)
        keyphrase_s = keyphrase_s.replace(' ,', ',')
        # print(keyphrase_s)
        obj_index = sentence.find(keyphrase_s)
        while obj_index == -1:
            length = int(length/2)
            keyphrase_s = ' '.join(x for x in keyphrase[:length])
            obj_index = sentence.find(keyphrase_s)
        if sentence[obj_index - 2] == ',':
            obj_index -= 1
        question = sentence[:obj_index-1]
        # print(keyphrase)
        prep = get_nearest_prep(keyphrase, word_Pos, verb)
        temp_wordlist = sentence.split()
        if aux != '' and ((auxpass != '' and temp_wordlist.index(aux) < temp_wordlist.index(auxpass)) or auxpass == ''):
            if auxpass == 'been' and temp_wordlist.index(aux) + 1 == temp_wordlist.index(auxpass):
                verb = auxpass + ' ' + verb
            obj_index = sentence.find(aux)
            question = sentence[:obj_index-1]
            question, location_or_time = replace_first_comma(question, location_or_time, neg_rb)
            question = question_type + ' ' + aux + ' ' + question + ' ' + verb + ' ' + prep + location_or_time + '?'
        elif auxpass != '':
            obj_index = sentence.find(auxpass)
            question = sentence[:obj_index-1]
            question, location_or_time = replace_first_comma(question, location_or_time, neg_rb)
            question = question_type + ' ' + auxpass + ' ' + question + ' ' + verb + ' ' + prep + location_or_time + '?'
        else:
            # replace the verb with original word
            question, location_or_time = replace_first_comma(question, location_or_time, neg_rb)
            question = replace_verb(question, verb, verb_s)
            # question = question.replace(verb, verb_s, 1)
            do_tense = get_tense(tag)
            question = question_type + do_tense + question + ' ' + prep + location_or_time + '?'

        return filter_what(question, sentence)
    elif copula != '':
        obj_index = sentence.find(' '+copula+' ')
        if obj_index == -1:
            obj_index = sentence.find(' '+copula+',')
            if obj_index == -1:
                return ''
        if sentence[obj_index - 1] == ',':
            obj_index -= 1
        question = sentence[:obj_index]

        question, location_or_time = replace_first_comma(question, location_or_time, neg_rb)

        question = question_type + ' ' + copula + ' ' + question + location_or_time + '?'

        return filter_what(question, sentence)
    else:
        # find the original word in word_Pos dict
        verb_s = word_Pos.get(root_word)[0]
        length = len(keyphrase)
        keyphrase_s = ' '.join(x for x in keyphrase)
        keyphrase_s = keyphrase_s.replace(' ,', ',')
        # print(keyphrase_s)
        obj_index = sentence.find(keyphrase_s)
        while obj_index == -1:
            length = int(length/2)
            keyphrase_s = ' '.join(x for x in keyphrase[:length])
            obj_index = sentence.find(keyphrase_s)
        question = sentence[:obj_index-1]
        # print(question)
        question, location_or_time = replace_first_comma(question, location_or_time, neg_rb)
        # replace the verb with original word
        question = replace_verb(question, root_word, verb_s)
        # question = question.replace(root_word, verb_s, 1)
        prep = ''
        if verb != '':
            prep = get_nearest_prep(keyphrase, word_Pos, verb)
        # print(aux, auxpass)
        temp_wordlist = sentence.split()
        if aux != '' and ((auxpass != '' and temp_wordlist.index(aux) < temp_wordlist.index(auxpass)) or auxpass == ''):
            if verb == '':
                question = question_type + ' ' + aux + ' ' + question + ' do' + location_or_time + '?'
                return ''
            else:
                if temp_wordlist.index(aux) < temp_wordlist.index(verb):
                    if auxpass == 'been' and temp_wordlist.index(aux) + 1 == temp_wordlist.index(auxpass):
                        verb = auxpass + ' ' + verb
                    elif temp_wordlist[temp_wordlist.index(verb)-1] != aux:
                        verb = temp_wordlist[temp_wordlist.index(verb)-1] + ' ' + verb
                    question = question_type + ' ' + aux + ' ' + question + ' ' + verb + ' ' + prep + location_or_time + '?'
                else:
                    do_tense = get_tense(tag)
                    question = question_type + do_tense + question + ' ' + verb_s + ' ' + prep + location_or_time + '?'
        elif auxpass != '':
            question = question_type + ' ' + auxpass + ' ' + question + ' ' + verb + ' ' + prep + location_or_time + '?'
        else:
            do_tense = get_tense(tag)
            if verb == '' or verb in be_words:
                question = question_type + do_tense + question + ' do' + location_or_time + '?'
                return ''
            else:
                question = question_type + do_tense + question + ' ' + verb_s + ' ' + prep + location_or_time + '?'
        
        return filter_what(question, sentence)

#How Many questions:
    #Question Type1 : Subj + verb + number + noun
    #Question Type2 : There is/are + number + noun + in + place
    #Question type3: noun + with + number + noun phrase
    #被动句
def gen_question_type1(sentence,obj):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp): #'CARDINAL' in get_entity(pp) or
                    prep = pp
            if (pp.upper().split()[0] == 'IN' or pp.upper().split()[0] == 'ON' or pp.upper().split()[0] == 'AT') and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp
                    
    if subj != None:
        if root[1].lower() != 'be':
            return "How many "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'
        else:
            return ''
    else:
        return "How many "+obj+" were "+root[0].lower()+' '+prep.lower()+' '+loc+'?'

def gen_question_type2(sentence,obj):
    prep = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] == 'IN' and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    prep = pp

    return "How many "+obj+" are there "+prep.lower()+'?'

def gen_question_type3(sentence,obj):
    root = get_ROOT(sentence)
    subj =get_nsubj(sentence)
    if obj == '' and root == '' :
        return ''
    if obj == '' and subj == '' :
        return ''
    prep = ''
    loc = ''
    if root[1] == 'be':
        return ''
    prep = ''
    loc = ''
    if len(get_pps(sentence)) > 0:
        for pp in get_pps(sentence):
            if pp.upper().split()[0] in ['DURING','IN','WHITIN','FROM','UNTIL'] and len(get_entity(pp))>0:
                if 'CARDINAL' in get_entity(pp) or 'DATE' in get_entity(pp) or 'TIME' in get_entity(pp):
                    prep = pp
            if (pp.upper().split()[0] == 'IN' or pp.upper().split()[0] == 'ON') and len(get_entity(pp))>0:
                if get_entity(pp)[0] in ['GPE','FAC','ORG','LOC']:
                    loc = pp

    return "How much "+obj+get_tense(root[2])+subj+" "+root[1].lower()+' '+prep.lower()+' '+loc+'?'

def create_when(sentence):
    be_words = ['cannot', 'is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may', 'will', 'would', 'have', 'had', 'has']
    doc = nlp(sentence)

    dep_list, pcfg = stanford_parser(sentence)
    word_Pos, Pos_word, _, dep_dict = Spacy_parser(sentence)
    root_word, tag = dep_dict.get("ROOT")

    dependency = dep_list

    keyword = ''
    copula = ''
    verb = ''
    aux = ''
    auxpass = ''
    keyword_tag = ''
    for i in range(len(dependency)):
        # print(dependency[i])
        if (dependency[i][1] == 'cop'):
    #         keyword = dependency[i][0][0]
            copula = dependency[i][2][0]
            keyword_tag = dependency[i][0][1]
            break
    if keyword == '':
        for i in range(len(dependency)):
            # print(dependency[i])
            if (dependency[i][1] == 'nsubj'):
                keyword = dependency[i][2][0]
                verb = dependency[i][0][0]
                keyword_tag = dependency[i][2][1]
                break

    if copula == '' and verb != root_word and root_word != keyword and 'VB' in tag:
        keyword = ''
    if keyword == '':
        verb = root_word

    for i in range(len(dependency)):
        if dependency[i][1] == 'aux':
            aux = dependency[i][2][0]
            break
    if verb != '':
        for i in range(len(dependency)):
            if (dependency[i][1] == 'auxpass' and verb == dependency[i][0][0]):
                auxpass = dependency[i][2][0]
                break

    questions = []
    ent_type_map = dict()
    ent_type_map["PERSON"] = "Who"
    ent_type_map["ORG"] = "Who"
    ent_type_map["DATE"] = "When"
    ent_type_map["TIME"] = "When"
    ent_type_map["LOCATION"] = "Where"
    ent_type_map["GPE"] = "Where"

    subject = keyword

    ents = []

    for ent in doc.ents:
        if len(ents) == 0:
            e = dict()
            e['text'] = ent.text
            e['start'] = ent.start_char
            e['end'] = ent.end_char
            e['label'] = ent.label_
            ents.append(e)
        else:
            prev = ents[-1]
            if ent.start_char - prev['end'] < 3 and prev['label'] == ent.label_:
                prev['text'] += " " + ent.text
                prev['end'] = ent.end_char
            elif ent.start_char - prev['end'] < 8 and prev['label'] == ent.label_ and "and" in sentence[prev['end']:ent.start_char]:
                prev['text'] += " " + ent.text
                prev['end'] = ent.end_char
            else:
                e = dict()
                e['text'] = ent.text
                e['start'] = ent.start_char
                e['end'] = ent.end_char
                e['label'] = ent.label_
                ents.append(e)

    for ent in ents:
        question_type = ""
        if ent['label'] in ent_type_map:
            question_type = ent_type_map[ent['label']]
        start_char = ent['start']
        end_char = ent['end']

        if question_type != "":
            if subject == "" or root_word == "":
                continue
            
            question = question_type
            verb_first = True
            # asking what is the subject
            if subject in ent['text']:
                verb_first = False
                
                # subject + be_words -> ask for the object
                # subject + non-be -> ask for the subject
                is_be = root_word in be_words
                if is_be:
                    question += " " + root_word + " " + ent['text']
                else:            
                    question += sentence[0:start_char]
                    question += sentence[end_char:-1]
            else:
                if ent['label'] == "ORG":
                    continue
                    
                if verb_first:
                    is_be = root_word in be_words
                    if is_be:
                        q_verb = root_word
                    else:
                        if aux != "":
                            q_verb = " " + aux + " "
                        elif auxpass != "":
                            q_verb = " " + auxpass + " "
                        else:
                            q_verb = get_tense(root_word)
                    
                    question += q_verb 
                    # first part
                    if " " + q_verb in sentence[0:start_char]:
                        question += sentence[0:start_char].replace(" " + q_verb, "")
                        question += sentence[end_char:-1]
                    else:
                        question += sentence[0:start_char]
                        question += sentence[end_char:-1].replace(" " + q_verb, "")
                
            question += "?"
            questions.append(question)

        return questions
        

def create_how(sentence):
    return select_question(sentence)

def countable_noun(noun):
    url = 'https://books.google.com/ngrams/graph?content=many+' + noun + '%2C+much+' + noun + '&year_start=1800&year_end=2000'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    try:
        many_data = json.loads(re.search('\{"ngram": "many ' + noun + '".*?\}', html).group(0))['timeseries']
        many = sum(many_data) / float(len(many_data))
    except:
        many = 0.0
    try:
        much_data = json.loads(re.search('\{"ngram": "much ' + noun + '".*?\}', html).group(0))['timeseries']
        much = sum(much_data) / float(len(much_data))
    except:
        much = 0.0
    if many > much:
        return True
    return False


def select_question(sentence):
    obj = ''
    ner = get_NE(sentence)
    if 'MONEY' in ner or 'CARDINAL' in ner or 'PERCENT' in ner or 'QUANTITY' in ner:
        for chunk in get_namechunks(sentence).keys():
            if 'CARDINAL' in get_entity(chunk) or 'QUANTITY' in get_entity(chunk):
                obj = get_namechunks(sentence)[chunk]

        if obj == '':
            return gen_question_type3(sentence, obj)

        if 'there' in sentence.lower():
            return gen_question_type2(sentence, obj)
        else:
            return gen_question_type1(sentence, obj)
    else:
        return ''
        
def checkValidSentence(sentence):
    dependency, pas = stanford_parser(sentence)
    isSentence = False
    for s in pas.subtrees():
        if s.label() == 'S':
            isSentence = True
            break
    hasSubj = False
    for i in range(len(dependency)):
        if (dependency[i][1] == 'nsubj' or dependency[i][1] == 'nsubjpass'):
            hasSubj = True
            break
    return isSentence and hasSubj

def extract_bracket(sentence):
    left = [i for i, a in enumerate(sentence) if a == '(']
    right = [i for i, a in enumerate(sentence) if a == ')']
    senList = []
    oldSentence = ''
    start = 0
    for i in range(len(left)):
        oldSentence += sentence[start:left[i] - 1]
        start = right[i] + 1
        # brackSentence = sentence[left[i] + 1:right[i]] + '.'
        # if checkValidSentence(brackSentence):
        #     senList.append(brackSentence)
    oldSentence += sentence[start:]
    senList.append(oldSentence)
    return senList

def break_simple_andbut(sentence, andORbut):
    senList = []
    position = sentence.find(', ' + andORbut + ' ')
    if position == -1:
        senList.append(sentence)
        return senList
    s1 = sentence[:position] + '.'
    s2 = sentence[position+len(', ' + andORbut + ' '):]
    dependency, pas = stanford_parser(s2)
    if checkValidSentence(s2):
        dependency1, pas1 = stanford_parser(s1)
        # print(dependency1)
        # pas1.pretty_print()
        subj = ''
        subjphrase = None
        for i in range(len(dependency1)):
            if (dependency1[i][1] == 'nsubj' or dependency1[i][1] == 'nsubjpass'):
                subj = dependency1[i][2][0]
                break
        
        for s in pas1.subtrees():
            if s.label() == 'NP' and subj in s.leaves() and subjphrase == None:
                subjphrase = s.leaves()
        
        if subjphrase is None:
            senList.append(sentence)
            return senList

        subjphrase_s = ' '.join(x for x in subjphrase)
        subjphrase_s = subjphrase_s.replace(' ,', ',')
        prp = ''
        for i in range(len(dependency)):
            # print(dependency[i])
            if (dependency[i][1] == 'nsubj'):
                if dependency[i][2][1] == 'PRP':
                    prp = dependency[i][2][0]
        if prp != '':
            s2 = s2.replace(prp, subjphrase_s, 1)
        # else:
        #     s2 = subjphrase_s + ' ' + s2
        # print(s1)
        # print(s2)
        senList.append(s1)
        senList.append(s2)
    else:
        senList.append(sentence)
        # print("false")
    return senList

def remove_clause(sentence, pcfg):
    remove = None
    for s in pcfg.subtrees():
        if s.label() == 'SBAR':
            remove = s.leaves()
            break
    if remove != None:
        remove_s = ' '.join(x for x in remove)
        remove_s = remove_s.replace('`` ', '"')
        remove_s = remove_s.replace(" ''", '"')
        remove_s = remove_s.replace(" ,", ',')
        remove_stmp = remove_s.replace(" .", '.')
        remove_s = ', ' + remove_stmp + ','
        index = sentence.find(remove_s)
        if index == -1:
            remove_s = ', ' + remove_stmp
            index = sentence.find(remove_s)
            if index == -1:
                remove_s = remove_stmp + ', '
                index = sentence.find(remove_s)
                if index == -1:
                    remove_s = remove_stmp
        new_s = sentence.replace(remove_s, '')
        return new_s
    else:
        return sentence

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
            senList += break_simple_andbut(s, 'and')
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
            if question != '':
                temp_qList.append(question)
                answer = answer_when(s, question)
                temp_aList.append(answer)
            
            qList.append(temp_qList)
            aList.append(temp_aList)

        for i in range(len(sList)):
            # score(sList[i], qList[i], None, None)
            print('S:', sList[i])
            for j in range(len(qList)):
                print('Q:', qList[i][j])
                print('A:', aList[i][j])
    

if __name__ == "__main__":
    main()
