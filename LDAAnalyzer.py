# input a directory, each file is a document

from utils.TopicIO import TopicIO
from preprocess.DocTokenizer import DirDocTokenizer, FileDocTokenizer
from gensim import corpora, models
import sys
from os.path import exists
from utils.WordCounter import WordCounter
from time import time
import os
import shutil
from similarity.SimTopicLists import SimTopicLists
from utils.topic_coherenc import TopicCoherence

#
# syntax: python  GenSimTweetTest1.py <input directory> <corpus type> <# of topics>  <src> <src type> <alpha> <eta> <output dir>
#  <input directory> Directory that saves LDA, dictionary and corpora
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <# of topics> default to 8
#  <src> the original corpus src name
#  <src type> 0: a file in which each line is a document.
#              Anything else or missing: a directory in which each file is a document
#  <output dir> results output directory

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

if not os.path.exists(output):
    os.makedirs(output)

# Check whether the directory exists or not
if not exists(src):
    print ("Input source does not exist")
    exit()

if input_type:
    # if input is a directory
    mdt = DirDocTokenizer()
    doc_list, token_list = mdt.orig(src)
else:
    print "file"

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

topics_io = TopicIO()
#
# print "======"
# topic = lda.print_topics(topics_count, 10)
# for x in topic:
#     print x
topics_output = output + "/topics"
# topics_io.write_topics(model=lda, orig_dir=src, num_topics=topics_count, num_words=len(dictionary.keys()),
#                        output_dir=topics_output)

# For each document, print the probability that the document being to each topic
# (Here we just print the original document file name)

length = len(max([fname for fname in doc_list]))

#dunsorted = open(output + "/" + "unsorted_doc_topics.txt", "w")
#dunsorted.write("Corpus Type: " + corpus_type)
#dunsorted.write("\nTopic Count: " + str(topics_count))

#dsorted = open(output + "/" + "sorted_doc_topics.txt", "w")
#dsorted.write("Corpus Type: " + corpus_type)
#dsorted.write("\nTopic Count: " + str(topics_count))

# doctlist = []
# for num in range(topics_count):
#     doctlist.append([])
#
# for i, doc in enumerate(corpus_lda):
    #dunsorted.write("\n\n" + '{:{l}}'.format(doc_list[i], l=length + 3))
    #dsorted.write("\n\n" + '{:{l}}'.format(doc_list[i], l=length + 3))

    # write the topic list for each doc by the topic number order
    #for value in doc:
        #dunsorted.write('{:22}'.format(" " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))

    # write the topic list for each doc by a decreasing probability order
    # doc = list(reversed(sorted(doc, key=lambda x: x[1])))
    # doctlist[doc[0][0]].append(doc_list[i])

    #for value in doc:
        #dsorted.write('{:22}'.format("  " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))

# For each topic, output documents illustrate the highest probability on it
# tdoc = open(output + "/" + "td_cluster.txt", "w")
# for index, sublist in enumerate(doctlist):
#     tdoc.write("Topic " + str(index) + ":  ")
#     tdoc.write(str(len(sublist)))
#     for value in sublist:
#         tdoc.write("  "+value)
#     tdoc.write("\n")

# tw = open(output + "/" + "words_in_topics.txt", "w")
# tw.write("Corpus Type: " + corpus_type)
# tw.write("\nTopic Count: " + str(topics_count))
# for i in range(topics_count):
#     tw.write("\n\nTopic " + str(i) + "\n")
#     for w_tuple in lda.show_topic(i, 300):
#         tw.write(str(w_tuple[0]) + ": " + str('{:.10f}'.format(w_tuple[1])) + "\n")

# self comparison difference

# stl = SimTopicLists()
# ofname = output + "/self-comp_max.txt"
# dist_output = open(ofname, "w")
# t_1 = output + "/topics"
# t_list1 = topics_io.read_topics(t_1)
# stl.show_results_2max_self(stl.bc_distance(t_list1, t_list1), dist_output)
#
# ofname = output + "/self-comp_min.txt"
# dist_output = open(ofname, "w")
# t_1 = output + "/topics"
# t_list1 = topics_io.read_topics(t_1)
# stl.show_results_2min_self(stl.bc_distance(t_list1, t_list1), dist_output)

# all_tokens = []
# for sublist in token_list:
#     all_tokens.extend(sublist)

# # word-topics
# wtfile = open(output + "/"+ "unsorted_wt.txt", "w")
# wtfile.write("Corpus Type: " + corpus_type)
# wtfile.write("\nTopic Count: " + str(topics_count))
# swt = open(output + "/"+ "sorted_wt.txt", "w")
# swt.write("Corpus Type: " + corpus_type)
# swt.write("\nTopic Count: " + str(topics_count))

#length = 30
wt = WordCounter()
total_words = wt.totalWords(corpus)

# Build a dictionary with word frequency in the corpus and write it to a file
freqlist = {}
time1 = time()
for word in dictionary:
    word_freq = float(wt.countWords3(corpus_dict, word))/total_words
    freqlist[dictionary.get(word)] = word_freq

# ofile = open(output + "/words_freq_"+corpus_type+".txt","w")
# for key, value in freqlist.iteritems():
#     ofile.write(str(key) + ": " + str(value)+"\n")


# Sort words in topics by word frequency difference from the baseline frequency
# os.makedirs(output+"/topics_wp")
for i in range(topics_count):
    ofile = open(output+"/topics_wp/Topic"+str(i)+".txt", "w")

    wtlist = []
    for wtuple in lda.show_topic(i, len(dictionary.keys())):
        freq_diff = wtuple[1] - freqlist[wtuple[0]]
        wtlist.append((wtuple[0], freq_diff, wtuple[1], freqlist[wtuple[0]]))
    wtlist = list(reversed(sorted(wtlist, key=lambda x: x[1])))

    for ftuple in wtlist:
        ofile.write(str(ftuple[0])+" "+str(ftuple[1])+" "+str(ftuple[2])+" "+str(ftuple[3])+"\n")



#for word in dictionary:
    # wtfile.write('{:{l}}'.format("\n"+dictionary.get(word)+": ", l=length))
    # swt.write('{:{l}}'.format("\n" + dictionary.get(word) + ": ", l=length))
    #
    # tlist = lda.get_term_topics(word)
    # for value in tlist:
    #     wtfile.write('{:22}'.format("  " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))
    #
    # # write the topic list for each doc by a decreasing probability order
    # tlist = list(reversed(sorted(tlist, key=lambda x: x[1])))
    #
    # for value in tlist:
    #     swt.write('{:22}'.format("  " + str(value[0]) + ": " + str('{:.15f}'.format(value[1])) + " "))
    #
    # word_frequency = wt.countWords3(corpus_dict, word)
    # #word_frequency = wt.countWords2(all_tokens, dictionary.get(word))
    # freqlist.append(int(word_frequency))
    #
    #
    # wtfile.write('{:10}'.format("  " + str(word_frequency) + "  ") + str('{:.15f}'.format(float(word_frequency)/total_words)))
    # swt.write('{:10}'.format("  " + str(word_frequency) + "  ") + str('{:.15f}'.format(float(word_frequency)/total_words)))

# time2 =time()
# print time2-time1
# print total_words
# print sum(freqlist.values())
