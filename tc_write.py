import sys
from utils.topic_coherence import TopicCoherence
from utils.TopicIO import TopicIO
from gensim import corpora, models
import os
#
# syntax: python  tcReader.py <input directory name> <corpus type> <# of topics> <src> <word count>
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

if len(sys.argv) <= 5:
    max_wc =10
else:
    max_wc = int(sys.argv[5])


print "input directory : " + dname
print "corpus type :" + corpus_type
print "# of topics : " + str(topics_count)
print "src : " + src
print "# of words used for topic coherence: " + str(max_wc)
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
tlist = topics_io.read_topics(output+"/topics")

# sort all words by decreasing frequency
tlist2 = []
for topic in tlist:
    tlist2.append(list(reversed(sorted(topic.words_dist, key=lambda x:x[1]))))

# construct a dictionary that contains top max_wc words in each topic
wdict = {}
for topic in tlist2:
    for num in range(max_wc):
        if topic[num][0] not in wdict.keys():
            wordkey = -1
            for key, value in dictionary.iteritems():
                if dictionary.get(key) == topic[num][0]:
                    wordkey = key
                    break
            if wordkey > -1:
                wdict[topic[num][0]] = wordkey


keylist = [value for key, value in wdict.iteritems()]

tc.write_freqlist(tc.word_list_doc_freq(keylist, corpus_dict, dictionary), dname+"/wdoc_freq_"+corpus_type+"_t"+str(topics_count)+".txt")
colist = tc.words_cooccur(keylist, corpus_dict, dictionary)
tc.write_freqlist(colist, dname+"/cofreq_"+corpus_type+"_t"+str(topics_count)+".txt")
