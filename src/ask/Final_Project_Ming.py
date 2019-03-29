{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Parse sentence to get NP, VP and NER analysis\n",
    "# Check if the sentence is grammaly correct\n",
    "# Use Spacy and Standford Parsing to compare results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 241,
   "metadata": {},
   "outputs": [],
   "source": [
    "#input should be a sentence\n",
    "def Spacy_parser(sentence): \n",
    "    from collections import Counter\n",
    "    import spacy\n",
    "    import pandas as pd\n",
    "    #from tabulate import tabulate\n",
    "    \n",
    "    word_Pos = {}\n",
    "    Pos_word = {}\n",
    "    dep_dict = {} # dict for dependency \n",
    "    NER =[]\n",
    "\n",
    "    nlp = spacy.load('en_core_web_lg')\n",
    "    \n",
    "    doc = nlp(sentence)\n",
    "    for ent in doc.ents:\n",
    "        NER.append([ent.text, ent.label_])\n",
    "        \n",
    "    for token in doc:\n",
    "        #print(token.text, token.dep_, token.head.text, token.head.pos_, token.tag_, [child for child in token.children])\n",
    "        #result.append([token.text, token.dep_, token.pos_, token.tag_, [child for child in token.children]])\n",
    "        \n",
    "        # update the dict with the word as key\n",
    "        word_Pos.update({token.text:[token.lemma_, token.pos_, token.tag_, [child for child in token.children]]})\n",
    "        \n",
    "        # update the dependency dict\n",
    "        dep_dict.update({token.dep_:[token.text, token.tag_]})\n",
    "        \n",
    "        # update the dict with the Pos tag as key\n",
    "        if token.tag_ not in Pos_word:\n",
    "            Pos_word.update({token.tag_: token.text})\n",
    "        else: \n",
    "            temp = []\n",
    "            value = Pos_word.get(token.tag_)\n",
    "            if isinstance(value, list): # check if the value is a list\n",
    "                temp.extend(Pos_word.get(token.tag_))\n",
    "            else:\n",
    "                temp.append(Pos_word.get(token.tag_))\n",
    "            temp.append(token.text)\n",
    "            Pos_word.update({token.tag_:temp})\n",
    "        \n",
    "    return word_Pos, Pos_word, NER, dep_dict "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 242,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'Mary': ['mary', 'PROPN', 'NNP', []], 'walks': ['walk', 'VERB', 'VBZ', [Mary, to, today, .]], 'to': ['to', 'ADP', 'IN', [school]], 'school': ['school', 'NOUN', 'NN', []], 'today': ['today', 'NOUN', 'NN', []], '.': ['.', 'PUNCT', '.', []]}\n",
      "{'NNP': 'Mary', 'VBZ': 'walks', 'IN': 'to', 'NN': ['school', 'today'], '.': '.'}\n",
      "[['Mary', 'PERSON'], ['today', 'DATE']]\n",
      "{'nsubj': ['Mary', 'NNP'], 'ROOT': ['walks', 'VBZ'], 'prep': ['to', 'IN'], 'pobj': ['school', 'NN'], 'npadvmod': ['today', 'NN'], 'punct': ['.', '.']}\n"
     ]
    }
   ],
   "source": [
    "result = Spacy_parser(\"Mary walks to school today.\")\n",
    "print(result[0])\n",
    "print(result[1])\n",
    "print(result[2])\n",
    "print(result[3])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# YES/NO question"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 248,
   "metadata": {},
   "outputs": [],
   "source": [
    "# the inputs are the original sentence and its POS tag list\n",
    "def create_YN(sentence, word_Pos, Pos_word, dep_dict):\n",
    "    '''\n",
    "    retract the VERB pos and check if it's be verb (is, are, were, was)\n",
    "    If not, add does/did/do at the beginning\n",
    "    Add question mark at the end\n",
    "    \n",
    "    MD  Modal verb (can, could, may, must)\n",
    "    VB  Base verb (take)\n",
    "    VBC Future tense, conditional\n",
    "    VBD Past tense (took)\n",
    "    VBF Future tense\n",
    "    VBG Gerund, present participle (taking)\n",
    "    VBN Past participle (taken)\n",
    "    VBP Present tense (take)\n",
    "    VBZ Present 3rd person singular (takes)\n",
    "    '''\n",
    "    result = \"\" # the string to return\n",
    "    tense = \"\" # the tense of the sentence\n",
    "    be_words= ['is', 'are', 'were', 'was', 'am', 'can', 'could', 'must', 'may','will','would', 'have', 'had','has']\n",
    "    \n",
    "    for x in be_words:\n",
    "        if x in word_Pos:\n",
    "            sentence = sentence.replace(x+\" \", \"\")\n",
    "            result = x.capitalize() +\" \"+sentence +\"?\"\n",
    "            return result\n",
    "        \n",
    "    # there is no be_words, check what is the tense of the sentence\n",
    "    temp = dep_dict.get(\"ROOT\")\n",
    "    root_word = temp[0] # the root word\n",
    "    verb = temp[1] # the pos tag of the root word\n",
    "    \n",
    "    # find the original word in word_Pos dict\n",
    "    verb_s = word_Pos.get(root_word)[0]\n",
    "    \n",
    "    # check the type of first word, if it's not proper noun, convert to lower case\n",
    "    nlp = spacy.load('en_core_web_lg')\n",
    "    tokens = nlp(sentence)\n",
    "    first_word = tokens[0]\n",
    "    print(first_word)\n",
    "    print(word_Pos.get(first_word)[2])\n",
    "    \n",
    "    if word_Pos.get(first_word)[2] != \"NNP\":\n",
    "        first_word_lower = first_word.lower()\n",
    "        sentence = sentence.replace(first_word, first_word_lower)\n",
    "        \n",
    "    # the verb is present third person singular\n",
    "    if verb == 'VBZ':        \n",
    "        sentence = sentence.replace(verb, verb_s)\n",
    "        result =\"Does \"+sentence +\"?\"\n",
    "    \n",
    "    '''\n",
    "    if verb_s in ['VBP','VBG','VB']:\n",
    "        #tense = \"present\"\n",
    "        \n",
    "            \n",
    "    if verb_s in ['VBF','VBC']:\n",
    "        #tense = \"future\"\n",
    "        \n",
    "    if verb_s in ['VBD','VBN']:\n",
    "        #tense = \"past\" \n",
    "    '''\n",
    "    \n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 249,
   "metadata": {},
   "outputs": [
    {
     "ename": "MemoryError",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mMemoryError\u001b[0m                               Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-249-e2331f8c8b2b>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m()\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[0mprint\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mcreate_YN\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"Mary walks to school today.\"\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mresult\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mresult\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mresult\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m3\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;32m<ipython-input-248-70fedef7ce1e>\u001b[0m in \u001b[0;36mcreate_YN\u001b[1;34m(sentence, word_Pos, Pos_word, dep_dict)\u001b[0m\n\u001b[0;32m     35\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     36\u001b[0m     \u001b[1;31m# check the type of first word, if it's not proper noun, convert to lower case\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 37\u001b[1;33m     \u001b[0mnlp\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mspacy\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'en_core_web_lg'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     38\u001b[0m     \u001b[0mtokens\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mnlp\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0msentence\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     39\u001b[0m     \u001b[0mfirst_word\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mtokens\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\__init__.py\u001b[0m in \u001b[0;36mload\u001b[1;34m(name, **overrides)\u001b[0m\n\u001b[0;32m     13\u001b[0m     \u001b[1;32mif\u001b[0m \u001b[0mdepr_path\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32min\u001b[0m \u001b[1;33m(\u001b[0m\u001b[1;32mTrue\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;32mFalse\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     14\u001b[0m         \u001b[0mdeprecation_warning\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mWarnings\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mW001\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mdepr_path\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 15\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mutil\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload_model\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     16\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     17\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\util.py\u001b[0m in \u001b[0;36mload_model\u001b[1;34m(name, **overrides)\u001b[0m\n\u001b[0;32m    110\u001b[0m     \u001b[1;32mif\u001b[0m \u001b[0misinstance\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mbasestring_\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m  \u001b[1;31m# in data dir / shortcut\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    111\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mname\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mset\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0md\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mname\u001b[0m \u001b[1;32mfor\u001b[0m \u001b[0md\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mdata_path\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0miterdir\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 112\u001b[1;33m             \u001b[1;32mreturn\u001b[0m \u001b[0mload_model_from_link\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    113\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mis_package\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m  \u001b[1;31m# installed as package\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    114\u001b[0m             \u001b[1;32mreturn\u001b[0m \u001b[0mload_model_from_package\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\util.py\u001b[0m in \u001b[0;36mload_model_from_link\u001b[1;34m(name, **overrides)\u001b[0m\n\u001b[0;32m    127\u001b[0m     \u001b[1;32mexcept\u001b[0m \u001b[0mAttributeError\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    128\u001b[0m         \u001b[1;32mraise\u001b[0m \u001b[0mIOError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mErrors\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mE051\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 129\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mcls\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    130\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    131\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\data\\en_core_web_lg\\__init__.py\u001b[0m in \u001b[0;36mload\u001b[1;34m(**overrides)\u001b[0m\n\u001b[0;32m     10\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     11\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 12\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mload_model_from_init_py\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0m__file__\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\util.py\u001b[0m in \u001b[0;36mload_model_from_init_py\u001b[1;34m(init_file, **overrides)\u001b[0m\n\u001b[0;32m    171\u001b[0m     \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[0mmodel_path\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexists\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    172\u001b[0m         \u001b[1;32mraise\u001b[0m \u001b[0mIOError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mErrors\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mE052\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mpath2str\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdata_path\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 173\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mload_model_from_path\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdata_path\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mmeta\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    174\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    175\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\util.py\u001b[0m in \u001b[0;36mload_model_from_path\u001b[1;34m(model_path, meta, **overrides)\u001b[0m\n\u001b[0;32m    154\u001b[0m             \u001b[0mcomponent\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mnlp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mcreate_pipe\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mconfig\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mconfig\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    155\u001b[0m             \u001b[0mnlp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0madd_pipe\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mcomponent\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mname\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 156\u001b[1;33m     \u001b[1;32mreturn\u001b[0m \u001b[0mnlp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfrom_disk\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mmodel_path\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    157\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    158\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\language.py\u001b[0m in \u001b[0;36mfrom_disk\u001b[1;34m(self, path, disable)\u001b[0m\n\u001b[0;32m    651\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m \u001b[1;33m/\u001b[0m \u001b[1;34m'vocab'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexists\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    652\u001b[0m             \u001b[0mexclude\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;34m'vocab'\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;32mTrue\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 653\u001b[1;33m         \u001b[0mutil\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfrom_disk\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mdeserializers\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mexclude\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    654\u001b[0m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_path\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mpath\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    655\u001b[0m         \u001b[1;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\util.py\u001b[0m in \u001b[0;36mfrom_disk\u001b[1;34m(path, readers, exclude)\u001b[0m\n\u001b[0;32m    509\u001b[0m     \u001b[1;32mfor\u001b[0m \u001b[0mkey\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mreader\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mreaders\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mitems\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    510\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mkey\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mexclude\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 511\u001b[1;33m             \u001b[0mreader\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m \u001b[1;33m/\u001b[0m \u001b[0mkey\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    512\u001b[0m     \u001b[1;32mreturn\u001b[0m \u001b[0mpath\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    513\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\spacy\\language.py\u001b[0m in \u001b[0;36m<lambda>\u001b[1;34m(p, proc)\u001b[0m\n\u001b[0;32m    647\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[0mhasattr\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mproc\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m'to_disk'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    648\u001b[0m                 \u001b[1;32mcontinue\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 649\u001b[1;33m             \u001b[0mdeserializers\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;32mlambda\u001b[0m \u001b[0mp\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mproc\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mproc\u001b[0m\u001b[1;33m:\u001b[0m \u001b[0mproc\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfrom_disk\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mp\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mvocab\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;32mFalse\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    650\u001b[0m         \u001b[0mexclude\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;33m{\u001b[0m\u001b[0mp\u001b[0m\u001b[1;33m:\u001b[0m \u001b[1;32mFalse\u001b[0m \u001b[1;32mfor\u001b[0m \u001b[0mp\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mdisable\u001b[0m\u001b[1;33m}\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    651\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;33m(\u001b[0m\u001b[0mpath\u001b[0m \u001b[1;33m/\u001b[0m \u001b[1;34m'vocab'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexists\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mnn_parser.pyx\u001b[0m in \u001b[0;36mspacy.syntax.nn_parser.Parser.from_disk\u001b[1;34m()\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\neural\\_classes\\model.py\u001b[0m in \u001b[0;36mfrom_bytes\u001b[1;34m(self, bytes_data)\u001b[0m\n\u001b[0;32m    349\u001b[0m                     \u001b[1;32mif\u001b[0m \u001b[0misinstance\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mbytes\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    350\u001b[0m                         \u001b[0mname\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mname\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mdecode\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'utf8'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 351\u001b[1;33m                     \u001b[0mdest\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mgetattr\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mlayer\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mname\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    352\u001b[0m                     \u001b[0mcopy_array\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdest\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mparam\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;34mb'value'\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    353\u001b[0m                 \u001b[0mi\u001b[0m \u001b[1;33m+=\u001b[0m \u001b[1;36m1\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\describe.py\u001b[0m in \u001b[0;36m__get__\u001b[1;34m(self, obj, type)\u001b[0m\n\u001b[0;32m     39\u001b[0m         \u001b[1;32melse\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     40\u001b[0m             \u001b[0mshape\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mget_shape\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mobj\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 41\u001b[1;33m             \u001b[0mdata\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mobj\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0madd\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mshape\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     42\u001b[0m             \u001b[1;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0minit\u001b[0m \u001b[1;32mis\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32mNone\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     43\u001b[0m                 \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0minit\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mdata\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mobj\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mops\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\check.py\u001b[0m in \u001b[0;36mchecked_function\u001b[1;34m(wrapped, instance, args, kwargs)\u001b[0m\n\u001b[0;32m    144\u001b[0m                     \u001b[1;32mraise\u001b[0m \u001b[0mExpectedTypeError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mcheck\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m[\u001b[0m\u001b[1;34m'Callable'\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    145\u001b[0m                 \u001b[0mcheck\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0marg_id\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mfix_args\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mkwargs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 146\u001b[1;33m         \u001b[1;32mreturn\u001b[0m \u001b[0mwrapped\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m*\u001b[0m\u001b[0margs\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    147\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    148\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0marg_check_adder\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mfunc\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\neural\\mem.py\u001b[0m in \u001b[0;36madd\u001b[1;34m(self, name, shape)\u001b[0m\n\u001b[0;32m     40\u001b[0m         \u001b[1;32massert\u001b[0m \u001b[0mname\u001b[0m \u001b[1;32mnot\u001b[0m \u001b[1;32min\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_offsets\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;34m\"TODO error\"\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     41\u001b[0m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_offsets\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mname\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;36m0\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mshape\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 42\u001b[1;33m         \u001b[0mblob\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_get_blob\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mprod\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     43\u001b[0m         \u001b[1;32mreturn\u001b[0m \u001b[0mblob\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mreshape\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     44\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\neural\\mem.py\u001b[0m in \u001b[0;36m_get_blob\u001b[1;34m(self, nr_req)\u001b[0m\n\u001b[0;32m     52\u001b[0m         \u001b[0mnr_avail\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m-\u001b[0m \u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m\u001b[1;33m+\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     53\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mnr_avail\u001b[0m \u001b[1;33m<\u001b[0m \u001b[0mnr_req\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 54\u001b[1;33m             \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_realloc\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mmax\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mnr_req\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;33m*\u001b[0m \u001b[1;36m2\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     55\u001b[0m         \u001b[0mblob\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m \u001b[1;33m:\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m \u001b[1;33m+\u001b[0m \u001b[0mnr_req\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     56\u001b[0m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m \u001b[1;33m+=\u001b[0m \u001b[0mnr_req\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\thinc\\neural\\mem.py\u001b[0m in \u001b[0;36m_realloc\u001b[1;34m(self, new_size)\u001b[0m\n\u001b[0;32m     58\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     59\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0m_realloc\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mnew_size\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 60\u001b[1;33m         \u001b[0mnew_mem\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mops\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mallocate\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mnew_size\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     61\u001b[0m         \u001b[0mnew_mem\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m:\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m\u001b[1;33m+\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m]\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m\u001b[1;33m[\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m,\u001b[0m \u001b[1;33m:\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_i\u001b[0m\u001b[1;33m+\u001b[0m\u001b[1;36m1\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     62\u001b[0m         \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_mem\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mnew_mem\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32mops.pyx\u001b[0m in \u001b[0;36mthinc.neural.ops.Ops.allocate\u001b[1;34m()\u001b[0m\n",
      "\u001b[1;31mMemoryError\u001b[0m: "
     ]
    }
   ],
   "source": [
    "print(create_YN(\"Mary walks to school today.\", result[0], result[1], result[3]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Spacy is much easier to use than NLTK and has better performance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 132,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\rafae\\Anaconda3\\lib\\site-packages\\ipykernel_launcher.py:12: DeprecationWarning: The StanfordDependencyParser will be deprecated\n",
      "Please use nltk.parse.corenlp.StanforCoreNLPDependencyParser instead.\n",
      "  if sys.path[0] == '':\n"
     ]
    }
   ],
   "source": [
    "from nltk.parse.stanford import StanfordDependencyParser\n",
    "from __future__ import division, unicode_literals\n",
    "import nltk\n",
    "\n",
    "path_to_jar = '/Users/rafae/Desktop/NLP Final project/stanford-parser.jar'\n",
    "path_to_models_jar = '/Users/rafae/Desktop/NLP Final project/stanford-english-corenlp-2018-10-05-models.jar'\n",
    "#path_to_models_jar = '/Users/rafae/Desktop/NLP Final project/stanford-parser-3.9.2-models.jar'\n",
    "\n",
    "#path_to_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser.jar'\n",
    "#path_to_models_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser-3.4.1-models.jar'\n",
    "\n",
    "dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 133,
   "metadata": {},
   "outputs": [],
   "source": [
    "from __future__ import print_function, unicode_literals\n",
    "\n",
    "from collections import defaultdict\n",
    "from itertools import chain\n",
    "from pprint import pformat\n",
    "import subprocess\n",
    "import warnings\n",
    "\n",
    "from six import string_types\n",
    "\n",
    "from nltk.tree import Tree\n",
    "from nltk.compat import python_2_unicode_compatible"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 143,
   "metadata": {},
   "outputs": [],
   "source": [
    "result = dependency_parser.raw_parse(\"Apple is looking at buying U.K. startup for $1 billion\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 138,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "defaultdict(<function DependencyGraph.__init__.<locals>.<lambda> at 0x000001E72DEEE048>,\n",
      "            {0: {'address': 0,\n",
      "                 'ctag': 'TOP',\n",
      "                 'deps': defaultdict(<class 'list'>, {'root': [3]}),\n",
      "                 'feats': None,\n",
      "                 'head': None,\n",
      "                 'lemma': None,\n",
      "                 'rel': None,\n",
      "                 'tag': 'TOP',\n",
      "                 'word': None},\n",
      "             1: {'address': 1,\n",
      "                 'ctag': 'NNP',\n",
      "                 'deps': defaultdict(<class 'list'>, {}),\n",
      "                 'feats': '_',\n",
      "                 'head': 3,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'nsubj',\n",
      "                 'tag': 'NNP',\n",
      "                 'word': 'Apple'},\n",
      "             2: {'address': 2,\n",
      "                 'ctag': 'VBZ',\n",
      "                 'deps': defaultdict(<class 'list'>, {}),\n",
      "                 'feats': '_',\n",
      "                 'head': 3,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'aux',\n",
      "                 'tag': 'VBZ',\n",
      "                 'word': 'is'},\n",
      "             3: {'address': 3,\n",
      "                 'ctag': 'VBG',\n",
      "                 'deps': defaultdict(<class 'list'>,\n",
      "                                     {'advcl': [5],\n",
      "                                      'aux': [2],\n",
      "                                      'nsubj': [1]}),\n",
      "                 'feats': '_',\n",
      "                 'head': 0,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'root',\n",
      "                 'tag': 'VBG',\n",
      "                 'word': 'looking'},\n",
      "             4: {'address': 4,\n",
      "                 'ctag': 'IN',\n",
      "                 'deps': defaultdict(<class 'list'>, {}),\n",
      "                 'feats': '_',\n",
      "                 'head': 5,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'mark',\n",
      "                 'tag': 'IN',\n",
      "                 'word': 'at'},\n",
      "             5: {'address': 5,\n",
      "                 'ctag': 'VBG',\n",
      "                 'deps': defaultdict(<class 'list'>,\n",
      "                                     {'dobj': [7],\n",
      "                                      'mark': [4]}),\n",
      "                 'feats': '_',\n",
      "                 'head': 3,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'advcl',\n",
      "                 'tag': 'VBG',\n",
      "                 'word': 'buying'},\n",
      "             6: {'address': 6,\n",
      "                 'ctag': 'NNP',\n",
      "                 'deps': defaultdict(<class 'list'>, {}),\n",
      "                 'feats': '_',\n",
      "                 'head': 7,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'compound',\n",
      "                 'tag': 'NNP',\n",
      "                 'word': 'U.K.'},\n",
      "             7: {'address': 7,\n",
      "                 'ctag': 'NNP',\n",
      "                 'deps': defaultdict(<class 'list'>,\n",
      "                                     {'compound': [6],\n",
      "                                      'nmod': [9]}),\n",
      "                 'feats': '_',\n",
      "                 'head': 5,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'dobj',\n",
      "                 'tag': 'NNP',\n",
      "                 'word': 'startup'},\n",
      "             8: {'address': 8,\n",
      "                 'ctag': 'IN',\n",
      "                 'deps': defaultdict(<class 'list'>, {}),\n",
      "                 'feats': '_',\n",
      "                 'head': 9,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'case',\n",
      "                 'tag': 'IN',\n",
      "                 'word': 'for'},\n",
      "             9: {'address': 9,\n",
      "                 'ctag': '$',\n",
      "                 'deps': defaultdict(<class 'list'>,\n",
      "                                     {'case': [8],\n",
      "                                      'nummod': [11]}),\n",
      "                 'feats': '_',\n",
      "                 'head': 7,\n",
      "                 'lemma': '_',\n",
      "                 'rel': 'nmod',\n",
      "                 'tag': '$',\n",
      "                 'word': '$'},\n",
      "             10: {'address': 10,\n",
      "                  'ctag': 'CD',\n",
      "                  'deps': defaultdict(<class 'list'>, {}),\n",
      "                  'feats': '_',\n",
      "                  'head': 11,\n",
      "                  'lemma': '_',\n",
      "                  'rel': 'compound',\n",
      "                  'tag': 'CD',\n",
      "                  'word': '1'},\n",
      "             11: {'address': 11,\n",
      "                  'ctag': 'CD',\n",
      "                  'deps': defaultdict(<class 'list'>, {'compound': [10]}),\n",
      "                  'feats': '_',\n",
      "                  'head': 9,\n",
      "                  'lemma': '_',\n",
      "                  'rel': 'nummod',\n",
      "                  'tag': 'CD',\n",
      "                  'word': 'billion'}})\n"
     ]
    }
   ],
   "source": [
    "dep = next(result)\n",
    "print(dep)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 142,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "digraph G{\n",
      "edge [dir=forward]\n",
      "node [shape=plaintext]\n",
      "\n",
      "0 [label=\"0 (None)\"]\n",
      "0 -> 3 [label=\"root\"]\n",
      "1 [label=\"1 (Apple)\"]\n",
      "2 [label=\"2 (is)\"]\n",
      "3 [label=\"3 (looking)\"]\n",
      "3 -> 1 [label=\"nsubj\"]\n",
      "3 -> 2 [label=\"aux\"]\n",
      "3 -> 5 [label=\"advcl\"]\n",
      "4 [label=\"4 (at)\"]\n",
      "5 [label=\"5 (buying)\"]\n",
      "5 -> 4 [label=\"mark\"]\n",
      "5 -> 7 [label=\"dobj\"]\n",
      "6 [label=\"6 (U.K.)\"]\n",
      "7 [label=\"7 (startup)\"]\n",
      "7 -> 6 [label=\"compound\"]\n",
      "7 -> 9 [label=\"nmod\"]\n",
      "8 [label=\"8 (for)\"]\n",
      "9 [label=\"9 ($)\"]\n",
      "9 -> 8 [label=\"case\"]\n",
      "9 -> 11 [label=\"nummod\"]\n",
      "10 [label=\"10 (1)\"]\n",
      "11 [label=\"11 (billion)\"]\n",
      "11 -> 10 [label=\"compound\"]\n",
      "}\n"
     ]
    }
   ],
   "source": [
    "dep = next(result)\n",
    "print(dep.to_dot())\n",
    "#print(type(dep))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 144,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1\tApple\t_\tNNP\tNNP\t_\t3\tnsubj\t_\t_\n",
      "2\tis\t_\tVBZ\tVBZ\t_\t3\taux\t_\t_\n",
      "3\tlooking\t_\tVBG\tVBG\t_\t0\troot\t_\t_\n",
      "4\tat\t_\tIN\tIN\t_\t5\tmark\t_\t_\n",
      "5\tbuying\t_\tVBG\tVBG\t_\t3\tadvcl\t_\t_\n",
      "6\tU.K.\t_\tNNP\tNNP\t_\t7\tcompound\t_\t_\n",
      "7\tstartup\t_\tNNP\tNNP\t_\t5\tdobj\t_\t_\n",
      "8\tfor\t_\tIN\tIN\t_\t9\tcase\t_\t_\n",
      "9\t$\t_\t$\t$\t_\t7\tnmod\t_\t_\n",
      "10\t1\t_\tCD\tCD\t_\t11\tcompound\t_\t_\n",
      "11\tbillion\t_\tCD\tCD\t_\t9\tnummod\t_\t_\n",
      "\n"
     ]
    }
   ],
   "source": [
    "dep = next(result)\n",
    "print(dep.to_conll(10))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
