from gensim import corpora
import random
from utils.topic_coherenc import TopicCoherence

dname = "brown_LDA"
dictionary = corpora.Dictionary.load(dname + "/dict.dict")
corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

corpus_dict =[]
for doc in corpus:
    corpus_dict.append(dict(doc))
dictlen = len(dictionary)
print dictlen

tc = TopicCoherence()



tsum = 0.0
for i in range(30):
    random_words = []
    for n in range(20):
        word = random.randint(1, dictlen)
        while word in random_words:
            word = random.randint(1, dictlen)
        random_words.append(word)

    result = tc.topic_coherence(random_words, corpus_dict)
    print result
    tsum += result
print tsum/30

