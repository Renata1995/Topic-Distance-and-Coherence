import sys

from gensim import corpora

from topic.topicio import TopicIO
from topic_evaluation.topic_coherence import TopicCoherence
from topic_evaluation.tc_tfidf import TfidfTC

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

if len(sys.argv) <= 6:
    startw = 0
else:
    startw = int(sys.argv[6])
    
if len(sys.argv) <= 7:
    tfidf = False
else:
    if sys.argv[7] == "t":
        tfidf = True
    else:
        tfidf = False

output = "LDA_"+src+"_"+corpus_type+"_t"+str(topics_count)

print "input directory : " + dname
print "corpus type :" + corpus_type
print "# of topics : " + str(topics_count)
print "src : " + src
print "# of words used for topic coherence: " + str(max_wc)
print "output : " + output
print "\n"

# Load directory
dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print(dictionary)

# Load corpus
if tfidf:
    corpus_fname =  dname + '/tfidf_corpus.mm'
else:
    corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

# Transfer each doc(list) in the corpus into a dic
corpus_dict = []
for doc in corpus:
    corpus_dict.append(dict(doc))

# Init all helpers
topics_io = TopicIO()
tc = TopicCoherence()
tct = TfidfTC()

# get all topics
tlist = topics_io.read_topics(output+"/topics")

# sort all words by decreasing frequency
tlist2 = []
for topic in tlist:
    topic.sort()
    tlist2.append(topic.list_words(max_wc, start=startw))

# construct a dictionary that contains top startw - max_wc words and their ids in each topic
wdict = {}
for topic in tlist2:
    for word in topic:
        if word not in wdict.keys(): # check whether the key already exists
            wordkey = -1
            for key, value in dictionary.iteritems():  # key-id value-word
                if dictionary.get(key) == word:
                    wordkey = key
                    break
            if wordkey > -1:
                wdict[word] = wordkey

# id list
keylist = [value for key, value in wdict.iteritems()]

if tfidf:
    tct.write_freqlist(tct.word_list_doc_freq(keylist, corpus_dict, dictionary),
                      dname + "/wdoc_freq_tfidf_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt")
    colist = tct.words_cooccur(keylist, corpus_dict, dictionary)
    tct.write_freqlist(colist, dname + "/cofreq_tfidf_" + corpus_type + "_t" + str(topics_count) + "_start" + str(startw) + ".txt")
else:
    tc.write_freqlist(tc.word_list_doc_freq(keylist, corpus_dict, dictionary), dname+"/wdoc_freq_"+corpus_type+"_t"+str(topics_count)+"_start"+str(startw)+".txt")
    colist = tc.words_cooccur(keylist, corpus_dict, dictionary)
    tc.write_freqlist(colist, dname+"/cofreq_"+corpus_type+"_t"+str(topics_count)+"_start"+str(startw)+".txt")
