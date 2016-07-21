import random
import sys

import numpy
from gensim import corpora

from topic_evaluation.wn import WordNetEvaluator
from topic.topic import Topic

# python random_tc.py <dname> <word_count> <sample_times> <output>
# <word_count>: the number of words that need to be randomly generated
# <sample_times>: the repetition times of the topic coherence calculation

if len(sys.argv) <= 1:
    dname = "reuters_LDA"
else:
    dname = sys.argv[1]

if len(sys.argv) <= 2:
    word_count = 10
else:
    word_count = int(sys.argv[2])

if len(sys.argv) <= 3:
    sample_times = 5
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

tc = WordNetEvaluator()

tc_results = []
words_list = []
ofile = open(dname+"/te_mean_rand.txt", "w")

for i in range(sample_times):
    random_words = []
    # generate random numbers
    for n in range(word_count):
        word = random.randint(1, dictlen-1)
        while word in random_words:
            word = random.randint(0, dictlen-1)
        random_words.append(word)

    keylist = []
    for key in random_words:
        keylist.append(dictionary[key])
    words_list.append(keylist)

    randt = Topic()
    for key in keylist:
        randt.words_dist.append((key, 0.1))

    # calculate topic coherence based on randomly generated words
    result = tc.evaluate(randt, word_count)
    tc_results.append(result)

ofile.write("AVG: " + str(numpy.average(tc_results))+"\n")
ofile.write("SD: "+ str(numpy.std(tc_results))+"\n\n")
for item in tc_results:
    ofile.write(str(item)+"\n")

for item in words_list:
    ofile.write(str(item)+"\n")

