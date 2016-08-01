from topic_evaluation.wn import WordNetEvaluator
import sys
import utils.name_convention as name
from topic.topicio import TopicIO
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
import os

if len(sys.argv) <= 1:
    corpus_type = "bow"
else:
    if sys.argv[1] == "t":
        corpus_type = "tfidf"
    elif sys.argv[1] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 2:
    topics_count = 3
else:
    topics_count = int(sys.argv[2])
src= "pp_reuters"



dname = name.get_output_dir(corpus_type, topics_count, src)

# read topics
tio = TopicIO()
tlist = tio.read_topics(dname + name.topics_dir())

ifile = open(dname+"/tc_freq_10.txt")

tdict = []
for num in range(topics_count):
    tdict.append({})

tid = 0
for line in ifile:
    if "Topic" in line and "coherence" not in line:
        tid = int(line.split()[1])
    if "/" in line:
        linelist = line.split()
        wordPair = linelist[0]+" "+ linelist[1]
        value = linelist[3].split("/")[0]
        tdict[tid][wordPair] = value

ofile = open("tc_test_2.txt","w")
for tindex, topic in enumerate(tlist):
    topic.sort()
    dist = topic.list_words(10)

    ofile.write("Topic "+str(tindex)+"\n")
    for i, m in enumerate(dist):
        for l in dist:
            if m != l:
                mllist = list(sorted([m,l]))
                key = " ".join(mllist)
                value = tdict[tindex][key]
                ofile.write(m +"  "+ l+ str(value)+"\n")
            
            
    

