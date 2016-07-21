import random
import sys

import numpy
from gensim import corpora

from topic_evaluation.wn import WordNetEvaluator
from topic.topic import Topic
from nltk.corpus import wordnet
from nltk.corpus import reuters
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

if len(sys.argv) <= 4:
    tcmethod = "path"
else:
    tcmethod = sys.argv[4]
    print tcmethod

if len(sys.argv) <= 5:
    ic = False
else:
    if sys.argv[5] == "ic":
        ic = True
    else:
        ic = False


dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print "Load dictionary",
print dictionary
corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

# transfer each doc in the corpus into a dictionary
corpus_dict = []
for doc in corpus:
    corpus_dict.append(dict(doc))
dictlen = len(dictionary)

tc = WordNetEvaluator()

tc_means = []
tc_medians = []
words_list = []

ofilemean = open(dname + "/te_mean_rand.txt", "w")
ofilemedian = open(dname + "/te_median_rand.txt", "w")

if ic:
    reuters_ic = reuters_ic = wordnet.ic(reuters, False, 0.0)


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
    if ic:
        result = tc.evaluate_ic(randt, word_count, reuters_ic, tcmethod)
    else:
        result = tc.evaluate(randt, word_count, tc)

    tc_means.append(result[1])
    tc_medians.append(result[2])

ofilemean.write("AVG: " + str(numpy.average(tc_means)) + "\n")
ofilemean.write("SD: " + str(numpy.std(tc_means)) + "\n\n")
for item in tc_means:
    ofilemean.write(str(item) + "\n")

for item in words_list:
    ofilemean.write(str(item) + "\n")

ofilemedian.write("AVG: " + str(numpy.average(tc_medians)) + "\n")
ofilemedian.write("SD: " + str(numpy.std(tc_medians)) + "\n\n")
for item in tc_medians:
    ofilemedian.write(str(item) + "\n")

for item in words_list:
    ofilemedian.write(str(item) + "\n")

