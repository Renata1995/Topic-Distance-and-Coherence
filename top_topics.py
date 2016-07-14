from similarity.SimTopicLists import SimTopicLists
from utils.TopicIO import TopicIO
import sys
from gensim import corpora, models
#
# syntax: python  GenSimTweetTest1.py <input directory> <# of topics> <corpus type> <src> <src type> <alpha> <eta> <output dir>
#  <input directory> Directory that saves LDA, dictionary and corpora
#  <# of topics> default to 8
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <src> the original corpus src name
#  <src type> 0: a file in which each line is a document.
#              Anything else or missing: a directory in which each file is a document
#  <output dir> results output directory

#
# Read command line parameters
#
if len(sys.argv) <= 1:
    dname = "pp_test_LDA"
else:
    dname = sys.argv[1]

if len(sys.argv) <= 2:
    topics_count = 8;
else:
    topics_count = int(sys.argv[2]);

if len(sys.argv) <= 3:
    corpus_type = "bow"
else:
    if sys.argv[3] == "t":
        corpus_type = "tfidf"
    elif sys.argv[3] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 4:
    src = "data"
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
    output = sys.argv[8];

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

# Load LDA
if alpha_set:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_alpha" + str(alpha) + ".lda"
elif eta_set:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + "_eta" + str(eta) + ".lda"
else:
    lda_fname = dname + "/" + corpus_type + "_t" + str(topics_count) + ".lda"
print "Load LDA file : " + lda_fname
lda = models.LdaModel.load(lda_fname, mmap="r")

# Load required corpus according to the argument corpus_type
if corpus_type == 'tfidf':
    corpus_fname = dname + '/tfidf_corpus.mm'
elif corpus_type == 'binary':
    corpus_fname = dname + '/binary_corpus.mm'
else:
    corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)
print(lda.show_topics(8))

# topic coherence
ofname = output+"/top_topics.txt"
ofname = open(ofname, "w")
tlist = lda.top_topics(corpus, num_words=20)
for item in tlist:
    ofname.write("Topic "+ str(item[2])+ "  " +str(item[1])+"\n")
    for wtuple in item[0]:
        ofname.write("\n"+wtuple[1]+" : "+str(wtuple[0]))
    ofname.write("\n\n\n")


# write ranking files
# stl = SimTopicLists()
# topics_io = TopicIO()
#
# t_1 = output + "/topics"
# t_list1 = topics_io.read_topics(t_1)
#
# ofname = output+"/self-comp_rank_kl.html"
# dist_output = open(ofname, "w")
# stl.show_results_rank_bw(stl.kl_divergence(t_list1, t_list1), dist_output)
#
# ofname = output+"/self-comp_rank_cos.html"
# dist2 = open(ofname, "w")
# stl.show_results_rank_bw(stl.cos_distance(t_list1, t_list1), dist2)
