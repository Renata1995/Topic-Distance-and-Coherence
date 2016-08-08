# input a directory, each file is a document

import os
import sys

from gensim import corpora, models

from topic.topicio import TopicIO
from preprocess.DocTokenizer import DirDocTokenizer, FileDocTokenizer
from utils.WordCounter import WordCounter

#
#  Analyze a specific LDA file and output results
#  Assume the existence of the LDA file, the corpus, src for the corpus, and the dictionary
#

#  python lda_analyze.py <input directory> <corpus type> <# of topics> <src> <src type> <alpha> <eta> <output dir>
#  <input directory> Directory that saves LDA, dictionary and corpora
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <# of topics> default to 8
#  <src> the original corpus src name. used for name conventions
#  <src type> 0: a file in which each line is a document.
#              Anything else or missing: a directory in which each file is a document
#  <output dir> results output directory
#  <alpha> default ot 1/# of topics
#  <eta> default to 1/# of topics

#
# Read command line parameters
#
if len(sys.argv) <= 1:
    dname = "output"
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


# Check the output directory
if not os.path.exists(output):
    os.makedirs(output)

if input_type:
    # if input is a directory
    mdt = DirDocTokenizer()
    doc_list, token_list = mdt.orig(src)
else:
    fdt = FileDocTokenizer()
    doc_list, token_list = fdt.save_pp(src)

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
corpus_lda = lda[corpus]
corpus_dict = [dict(doc) for doc in corpus]

dictionary = lda.id2word
print dictionary

# Write topics
topics_io = TopicIO()
topics_output = output + "/topics"
topics_io.write_topics(model=lda, orig_dir=src, num_topics=topics_count, num_words=len(dictionary.keys()),
                       output_dir=topics_output)


# For each document, print the probability that the document being to each topic
# (Here we just print the original document file name)

length = len(max([fname for fname in doc_list]))

# Generate document-topic matrix
dunsorted = open(output + "/" + "unsorted_doc_topics.txt", "w")
dunsorted.write("Corpus Type: " + corpus_type)
dunsorted.write("\nTopic Count: " + str(topics_count))

dsorted = open(output + "/" + "sorted_doc_topics.txt", "w")
dsorted.write("Corpus Type: " + corpus_type)
dsorted.write("\nTopic Count: " + str(topics_count))

doctlist = []
for num in range(topics_count):
    doctlist.append([])

for i, doc in enumerate(corpus_lda):
    dunsorted.write("\n\n" + '{:{l}}'.format(doc_list[i], l=length + 3))
    dsorted.write("\n\n" + '{:{l}}'.format(doc_list[i], l=length + 3))

    #write the topic list for each doc by the topic number order
    for value in doc:
        dunsorted.write('{:22}'.format(" " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))

    #write the topic list for each doc by a decreasing probability order
    doc = list(reversed(sorted(doc, key=lambda x: x[1])))
    doctlist[doc[0][0]].append(doc_list[i])

    for value in doc:
        dsorted.write('{:22}'.format("  " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))


# topic-document matrix
# For each topic, output documents illustrate the highest probability on it

tdoc = open(output + "/" + "td_cluster.txt", "w")
for index, sublist in enumerate(doctlist):
    tdoc.write("topic " + str(index) + ":  ")
    tdoc.write(str(len(sublist)))
    for value in sublist:
        tdoc.write("  "+value)
    tdoc.write("\n")


# topic-words matrix
# For each topic, output top 300 words in the topic
tw = open(output + "/" + "words_in_topics.txt", "w")
tw.write("Corpus Type: " + corpus_type)
tw.write("\nTopic Count: " + str(topics_count))
for i in range(topics_count):
    tw.write("\n\nTopic " + str(i) + "\n")
    for w_tuple in lda.show_topic(i, 300):
        tw.write(str(w_tuple[0]) + ": " + str('{:.10f}'.format(w_tuple[1])) + "\n")


# Represent topic be decreasing probability difference
# probability difference = word probability in the topic - word probability in the corpus
wt = WordCounter()
total_words = wt.totalWords(corpus)
#
# Build a dictionary with word frequency in the corpus and write it to a file
freqlist = {}
for word in dictionary:
    word_freq = float(wt.countWords3(corpus_dict, word))/total_words
    freqlist[dictionary.get(word)] = word_freq

# Sort words in topics by word frequency difference from the baseline frequency
if not os.path.exists(output+"/topics_wp"):
    os.makedirs(output+"/topics_wp")

for i in range(topics_count):
    ofile = open(output+"/topics_wp/topic"+str(i)+".txt", "w")

    wtlist = []
    for wtuple in lda.show_topic(i, len(dictionary.keys())):
        freq_diff = wtuple[1] - freqlist[wtuple[0]]
        wtlist.append((wtuple[0], freq_diff, wtuple[1], freqlist[wtuple[0]]))
    wtlist = list(reversed(sorted(wtlist, key=lambda x: x[1])))

    for ftuple in wtlist:
        ofile.write(str(ftuple[0])+" "+str(ftuple[1])+" "+str(ftuple[2])+" "+str(ftuple[3])+"\n")



