import sys

from gensim import corpora

from topic.topicio import TopicIO
from topic_evaluation.topic_coherence import TopicCoherence

#
# syntax: python  GenSimTweetTest1.py <input directory name> <corpus type> <# of topics> <src>
#  <dictionary name> the name of the input dictionary
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <# of topics> number of topics. default to 8
#  <alpha> default ot 1/# of topics
#  <eta> default to 1/# of topics
#

#
# Read command line parameters
#
if len(sys.argv) <= 1:
    dname = 'pp_test_LDA'
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
    src = "pp_test"
else:
    src = sys.argv[4]

print "input directory : " + dname
print "corpus type :" + corpus_type
print "# of topics : " + str(topics_count)
print "src : " + src
print "\n"

# Load directory
dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print(dictionary)

# Load corpus
corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

corpus_dict = []
for doc in corpus:
    corpus_dict.append(dict(doc))

topics_io = TopicIO()
output = "LDA_"+src+"_"+corpus_type+"_t"+str(topics_count)
tc = TopicCoherence()

# get all topics
tlist = topics_io.read_topics_wp(output+"/topics_wp")

tlist2 = []
for topic in tlist:
    tlist2.append(topic.words_dist)


ctlist = []
for index, t in enumerate(tlist2):
    t = t[:20]
    subt = [wt[0] for wt in t]
    subt2 = []
    for w in subt:
        for key, value in dictionary.iteritems():
            if value == w:
                subt2.append(key)
    ctlist.append((index, tc.coherence(subt2, corpus_dict), t))

ctlist = list(reversed(sorted(ctlist, key=lambda x:x[1])))
ofile = open(output + "/wp_ct.txt", "w")
for tctuple in ctlist:
    ofile.write("topic  "+ str(tctuple[0])+"   "+str(tctuple[1]) + "\n\n")
    for item in tctuple[2]:
        ofile.write(item[0]+" : "+ str(item[1])+"\n")
    ofile.write("\n\n")