# input a directory, each file is a document

from utils.TopicIO import TopicIO
from gensim import corpora, models
import sys

#
# syntax: python  GenSimTweetTest1.py <input directory name> <corpus type> <# of topics> <alpha> <eta>
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

if len(sys.argv) <= 4 or sys.argv[4] == "d":
    alpha_set = False
    alpha = [1.0 / topics_count] * topics_count
else:
    alpha_set = True
    alpha = [float(sys.argv[4])] * topics_count

if len(sys.argv) <= 5:
    eta_set = False
    eta = [1.0 / topics_count] * topics_count
else:
    eta_set = True
    eta = [float(sys.argv[5])] * topics_count

print "input directory : " + dname
print "corpus type :" + corpus_type
print "# of topics : " + str(topics_count)
print "alpha : " + str(alpha)
print "eta: " + str(eta)
print "\n"

# Load directory
dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print(dictionary)

# Load required corpus according to the argument corpus_type
if corpus_type == 'tfidf':
    corpus_fname = dname + '/tfidf_corpus.mm'
elif corpus_type == 'binary':
    corpus_fname = dname + '/binary_corpus.mm'
else:
    corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

topics_io = TopicIO()

print "=========== start LDA"
if alpha_set:
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topics_count, minimum_probability=-1, alpha=alpha)
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_alpha" + str(sys.argv[4]) + ".lda"
elif eta_set:
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topics_count, minimum_probability=-1, eta=eta)
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_eta" + str(sys.argv[5]) + ".lda"
else:
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topics_count, minimum_probability=-1)
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + ".lda"


print "LDA file name : " + lda_fname
lda.save(lda_fname)
corpus_lda = lda[corpus]
