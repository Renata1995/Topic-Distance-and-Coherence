# input a directory, each file is a document

from utils.TopicIO import TopicIO
from utils.BinaryCorpus import BinaryCorpus
from preprocess.DocTokenizer import DirDocTokenizer, FileDocTokenizer
from gensim import corpora, models, similarities, matutils
import numpy as np
import sys
from os.path import isfile, getmtime, exists
from os import listdir
from time import time
from utils.WordCounter import WordCounter
import os

#
# syntax: python  GenSimTweetTest1.py <input type> <directory name> <# of topics> <corpus type> <preprocess or not> <topics output>
#  <input type> 0: a file in which each line is a document.
#              Anything else or missing: a directory in which each file is a document
#  <directory/file name> input directory/file name
#  <# of topics> default to 8
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <preprocess or not>:0 = no preprocessing. Anything else or missing: preprocessing
#  <topics output> topic output directory name. default to topics_output
#
#  each file in the directory is a document
#
#

#
# Read command line parameters
#
if len(sys.argv) <= 1:
    input_type = True
else:
    if int(sys.argv[1]) == 0:
        input_type = False
    else:
        input_type = True

if len(sys.argv) <= 2:
    src = "pp_data"
else:
    src = sys.argv[2];

if len(sys.argv) <= 3:
    topics_count = 4;
else:
    topics_count = int(sys.argv[3]);

if len(sys.argv) <= 4:
    corpus_type = "c"
else:
    corpus_type = sys.argv[4]

if len(sys.argv) <= 5:
    preprocess = False
else:
    if int(sys.argv[5]) == 0:
        preprocess = False
    else:
        preprocess = True

if len(sys.argv) <= 6:
    t_output = "t_topics_output"
else:
    t_output = sys.argv[6]

print "input type :",
if input_type:
    print "Input is a directory"
else:
    print "Input is a file"
print "source : " + src
print "tcount : " + str(topics_count)
print "corpus type :",
if corpus_type == "t":
    print "tfidf"
elif corpus_type == "b":
    print "binary"
else:
    print "bow"
print "preprocess : " + str(preprocess)
print "topics output directory name : " + t_output

# Check whether the directory exists or not
if not exists(src):
    print ("Input source does not exist")
    exit()

if input_type:
    # if input is a directory
    mdt = DirDocTokenizer()
    # According to the <preprocess> param, determine whether the input corpus should be preprocessed or not

    if not preprocess:
        doc_list, token_list = mdt.orig(src)

    else:
        # Execution in the past resulted in existing preprocessed directory.
        # Determine whether
        # a) an up-to-date preprocessed directory is available to use
        # or b) the original input directory should be used.

        pp_dir_use = True  # indicate whether the preprocessed directory or the input directory should be used
        pp_dir = "pp_" + src  # the name of a possibly existing preprocessed directory

        if not exists(pp_dir):
            # if the preprocessed directory does not exist, use the input directory
            pp_dir_use = False

        else:
            # When the preprocessed directory exists,
            # go through each file in the input directory and the found preprocessed directoary.

            # If the preprocessed directory satisfies these two requirements:
            # 1. Every original file has a corresponding preprocessed file
            # 2. Every preprocessed file 's last-modification time is later that that of the original file
            # Then ,the existing preprocessed directory will be used.

            # Else, the input directory will be used.

            for fname in listdir(src):
                orig_file_name = src + "/" + fname
                pp_file_name = pp_dir + "/" + fname
                if not isfile(pp_file_name) or getmtime(orig_file_name) > getmtime(pp_file_name):
                    pp_dir_use = False
                    break

        # Choose the appropriate directory to use
        if pp_dir_use:
            print ("PreProcessed Files exist and are up-to-date.\n")
            doc_list, token_list = mdt.orig(pp_dir)
        else:
            doc_list, token_list = mdt.preprocess(src)
else:
    # if input is a file
    mdt = FileDocTokenizer()
    if not preprocess:
        doc_list, token_list = mdt.orig(src)
    else:
        mtime_input = getmtime(src)
        output_tokens = "pp_" + src
        output_docs = "docs_pp_" + src
        if isfile(output_tokens) and isfile(output_docs) and getmtime(output_tokens) > mtime_input and getmtime(
                output_docs) > mtime_input:
            print ("PreProcessed Files exist.\n")
            token_list = mdt.orig(src)[1]
            doc_list = mdt.read_pp_doc_list(src)
        else:
            doc_list, token_list = mdt.preprocess(src)

# Prepare the directory
dictionary = corpora.Dictionary(token_list)
print(dictionary)

# Generate the bow corpus
corpus_bow = [dictionary.doc2bow(text) for text in token_list]

# According to the argument corpus_type, select the suitable corpus to use in the following processing
if corpus_type == 't':
    corpus_type = "tfidf"
    tfidf = models.TfidfModel(corpus_bow)
    corpus = tfidf[corpus_bow]

elif corpus_type == 'b':
    corpus_type = "binary"
    corpus = BinaryCorpus(corpus_bow)

else:
    corpus_type = "bow"
    corpus = corpus_bow

#
#  Latent Semantic Indexing Model
#  (Notice we build the model based on TFIDF
#



print "=========== start LSI"

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topics_count)

#
#  print LSI document vector for each document
#

#
# print lsi
#
corpus_lsi = lsi[corpus]
print corpus_lsi
for doc in corpus_lsi:
    print doc

#
#  print the topics for LSI
#


print "=========== topics"

topic = lsi.print_topics(topics_count, 50)

for x in topic:
    print x

#
#  LDA
#  Pick the corpus to use
#

topics_io = TopicIO()

print "=========== start LDA"
start_time = time()
lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topics_count, minimum_probability=-1)
corpus_lda = lda[corpus]

print "======"
# topic = lda.print_topics(topics_count, 10)
# for x in topic:
#    print x
topics_io.write_topics(model=lda, orig_dir=src, num_topics=topics_count, num_words=len(dictionary.keys()),
                       output_dir=t_output)

#
#  For each topic: print the top 20 words and  all the tweets that has non-trivial probability associated with it (which is defined as (1.01/# of topics)
#

#  convert LDA corpus back to dense matrix represnetation (to enable the argsort statement to work properly
# now each row is a  topic, so can use the argsort

c1 = matutils.corpus2dense(corpus_lda, topics_count)
i = 0
for q in c1:
    print "======="
    x1 = [w for w in np.argsort(q) if q[w] > 1.01 / topics_count]
    print "LDATopic " + str(i) + " " + lda.print_topic(i, 20)
    print x1
    for x2 in x1[::-1]:
        print str(x2) + " ",
        print doc_list[x2] + " ",
        #   print token_list[x2],
        #   print " ",
        print q[x2]
    i = i + 1

# Print the topics again (but with 50 words)
#
#
print "======"
topic = lda.print_topics(topics_count, 50)
for x in topic:
    print x

for i in range(1, 100):
    x2 = [(i, 1)]
    x3 = lda[x2]
    print repr(x3)


#
#  HDPA (ignore for now)
#


# print "=========== start HDPA"
# hdp = models.HdpModel(corpus_tfidf, id2word=dictionary)
# hdp = models.HdpModel(corpus, id2word=dictionary)
# hdp = models.HdpModel(corpus_binary, id2word=dictionary)
# for l in hdp.show_topics(-1, 40):
#   print l
