from preprocess.DocTokenizer import DirDocTokenizer, FileDocTokenizer
from gensim import corpora, models
import sys
import os
import shutil
from utils.BinaryCorpus import BinaryCorpus

#
# Generate and save dictionary and three types of corpus (tfidf, bow, and binary) to prepare for LDA
#


# syntax: python  LDAPreparator.py <input type> <directory name> <preprocess or not> <output directory name>
#  <input type> 0: a file in which each line is a document.
#              Anything else or missing: a directory in which each file is a document
#  <directory/file name> input directory/file name
#  <preprocess or not>:0 = no preprocessing. Anything else or missing: preprocessing
#  <output directory name> output directory name


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
    src = "pp_test"
else:
    src = sys.argv[2];

if len(sys.argv) <= 3:
    preprocess = True
else:
    if int(sys.argv[3]) == 0:
        preprocess = False
    else:
        preprocess = True

if len(sys.argv) <= 4:
    output_dir = src+"_LDA"
else:
    output_dir = sys.argv[4]


print "input type :",
if input_type:
    print "Input is a directory"
else:
    print "Input is a file"
print "source : " + src
print "preprocess : " + str(preprocess)
print "output directory name : " + output_dir
print "\n"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Check whether the src file/directory exists or not
if not os.path.exists(src):
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

        if not os.path.exists(pp_dir):
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

            for fname in os.listdir(src):
                orig_file_name = src + "/" + fname
                pp_file_name = pp_dir + "/" + fname
                if not os.path.isfile(pp_file_name) or os.path.getmtime(orig_file_name) > os.path.getmtime(pp_file_name):
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
        mtime_input = os.path.getmtime(src)
        output_tokens = "pp_" + src
        output_docs = "docs_pp_" + src
        if os.path.isfile(output_tokens) and os.path.isfile(output_docs) and os.path.getmtime(output_tokens) > mtime_input and os.path.getmtime(
                output_docs) > mtime_input:
            print ("PreProcessed Files exist.\n")
            token_list = mdt.orig(src)[1]
            doc_list = mdt.read_pp_doc_list(src)
        else:
            doc_list, token_list = mdt.preprocess(src)

# Prepare and save the dictionary
dictionary = corpora.Dictionary(token_list)
dictionary.save(output_dir+"/dict.dict")

print(dictionary)

# Generate and save three types of corpus
corpus_bow = [dictionary.doc2bow(text) for text in token_list]
corpora.MmCorpus.serialize(output_dir+"/bow_corpus.mm", corpus_bow)

tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]
corpora.MmCorpus.serialize(output_dir+"/tfidf_corpus.mm", corpus_tfidf)

corpus_binary = BinaryCorpus(corpus_bow)
corpora.MmCorpus.serialize(output_dir+"/binary_corpus.mm", corpus_binary)

