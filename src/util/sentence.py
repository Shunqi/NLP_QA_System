import os
from nltk.parse import stanford

os.environ['STANFORD_PARSER'] = 'stanford-parser-full-2018-10-17/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'
pcfg_parser = stanford.StanfordParser(model_path='stanford-parser-full-2018-10-17/englishPCFG.ser.gz')
dep_parser = stanford.StanfordDependencyParser(model_path='stanford-parser-full-2018-10-17/englishPCFG.ser.gz')
        
def stanford_parser(self, sentence):
    pcfg = pcfg_parser.raw_parse(sentence).__next__()
    dep = dep_parser.raw_parse(sentence).__next__()
    dep_list = list(dep.triples())
    return dep_list, pcfg