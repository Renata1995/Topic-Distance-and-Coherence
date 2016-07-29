import os
import sys
from gensim import corpora, models
from utils.WordCounter import WordCounter
from topic.topicio import TopicIO

if len(sys.argv) <= 1:
    dname = "reuters_LDA"
else:
    dname = sys.argv[1]

if len(sys.argv) <= 2:
    corpus_type = "bow"
else:
    if sys.argv[2] == "t":
        corpus_type = "tfidf"
    elif sys.argv[2] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 3:
    topics_count = 8;
else:
    topics_count = int(sys.argv[3]);

if len(sys.argv) <= 4:
    src = "pp_reuters"
else:
    src = sys.argv[4];

if len(sys.argv) <= 5:
    input_type = True
else:
    if int(sys.argv[5]) == 0:
        input_type = False
    else:
        input_type = True

if len(sys.argv) <= 6 or sys.argv[6] == "d":
    alpha_set = False
else:
    alpha_set = True
    alpha = sys.argv[6]

if len(sys.argv) <= 7:
    eta_set = False
else:
    eta_set = True
    eta = sys.argv[7]

if len(sys.argv) <= 8:
    if alpha_set:
        output = "LDA_" + src + "_" + corpus_type + "_t" + str(topics_count)+"_alpha"+str(alpha)
    elif eta_set:
        output = "LDA_" + src + "_" + corpus_type + "_t" + str(topics_count) + "_eta" + str(eta)
    else:
        output = "LDA_" + src + "_" + corpus_type + "_t" + str(topics_count)
else:
    output = sys.argv[8]


print "input directory : " + dname
print "# of topics : " + str(topics_count)
print "corpus type :" + corpus_type
print "source : " + src
print "input type :",
if input_type:
    print "Input is a directory"
else:
    print "Input is a file"
print "output directory : " + output
if alpha_set:
    print "alpha : "+ alpha
if eta_set:
    print "eta : " + eta
print "\n"

# Load required corpus according to the argument corpus_type

corpus_fname = dname + '/tfidf_corpus.mm'
corpus = corpora.MmCorpus(corpus_fname)

# Load LDA
if alpha_set:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_alpha" + str(alpha) + ".lda"
elif eta_set:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_eta" + str(eta) + ".lda"
else:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + ".lda"
print "Load LDA file : " + lda_fname
lda = models.LdaModel.load(lda_fname, mmap="r")
corpus_lda = lda[corpus]
corpus_dict = [dict(doc) for doc in corpus]

# load dictionary
dictionary = lda.id2word

# a list that include top documents for each topic
tdoc_list = []
for n in range(topics_count):
    tdoc_list.append([])
    
for index, doc in enumerate(corpus_lda)
    for t in doc:  # t: (tid, pt/d)
        if t[1]>0.1: # if pt/d is larger than 0.1, add this doc to the topic doc list
            tdoc_list[t[0]].append(index)
            
tio = TopicIO()
tlist = tio.read_topics(pctotal, output + "/topics")

top = 300

newtlist = []
for topic in tlist:
    dist = topic.list(300)
    

#tio.write_topics_from_tlist(tlist, output+"/topics_ptipc")



