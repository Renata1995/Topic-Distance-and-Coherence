from gensim import corpora
import random
from utils.topic_coherenc import TopicCoherence
import sys
import numpy

# python random_tc.py <dname> <word_count> <sample_times> <output>
# <word_count>: the number of words that need to be randomly generated
# <sample_times>: the repetition times of the topic coherence calculation

if len(sys.argv) <= 1:
    dname = "brown_LDA"
else:
    dname = sys.argv[1]

if len(sys.argv) <= 2:
    word_count = 10
else:
    word_count = int(sys.argv[2])

if len(sys.argv) <= 3:
    sample_times = 20
else:
    sample_times = int(sys.argv[3])

dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print "Load dictionary",
print dictionary
corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

# transfer each doc in the corpus into a dictionary
corpus_dict =[]
for doc in corpus:
    corpus_dict.append(dict(doc))
dictlen = len(dictionary)

tc = TopicCoherence()

tc_results = []
ofile = open(dname+"/tc_rand_"+str(word_count)+".txt", "w")

for i in range(sample_times):
    random_words = []
    # generate random numbers
    for n in range(word_count):
        word = random.randint(1, dictlen)
        while word in random_words:
            word = random.randint(1, dictlen)
        random_words.append(word)

    # calculate topic coherence based on randomly generated words
    result = tc.topic_coherence(random_words, corpus_dict)
    tc_results.append(result)

ofile.write("AVG: " + str(numpy.average(tc_results))+"\n")
ofile.write("SD: "+ str(numpy.std(tc_results))+"\n\n")
for item in tc_results:
    ofile.write(str(item)+"\n")

