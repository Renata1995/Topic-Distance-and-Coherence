import MyTextPreProcess
from MyConvertUnicode import MyConvertUnicode
from nltk import word_tokenize, sent_tokenize
import os
import re

class DirDocTokenizer:
    """
    Transfer a corpus into word tokens with or without preprocessing.
    Preprocessing removes stop words and turn all words into stems
    """

    def orig(self, dname):
        """
        Transfer a corpus into a list of documents string and a 2D list of word tokens
        :param dname:the name of the input directory
        :return:a list of document names and a 2D list of word tokens
        """
        doc_list = [fname for fname in sorted(os.listdir(dname))]
        token_list = self.orig_corpus_tokenize(dname)
        return doc_list, token_list

    def preprocess(self, dname):
        """
        preprocess a new corpus directory and write results to files
        :param dname: the name of the corpus directory
        :param pp_dname: the name of the previously preprocced corpus directory
        :return: a list of document names and a 2D list of word tokens
        """
        doc_list = [fname for fname in sorted(os.listdir(dname))]
        token_list = self.pp_corpus_tokenize(dname)
        return doc_list, token_list

    def orig_corpus_tokenize(self, dname):
        """
        Transfer a corpus into a 2D list of word tokens arranged by documents without preprocessing
        :param dname: corpus directory name
        :return: a 2D list of word tokens
        """
        orig_tokens = []
        for i_file in os.listdir(dname):
            ifile = dname + "/" + i_file
            orig_tokens.append(self.orig_doc_tokenize(ifile))
        return orig_tokens

    def orig_doc_tokenize(self, filename):
        """
        Transfer a document into a list of word tokens without preprocessing
        :param filename: document name
        :return: a list of word tokens
        """
        # prepare the document string
        converter = MyConvertUnicode()
        input_file = open(filename, "r")
        file_str = input_file.read().decode("utf-8", "ignore")
        #file_str = converter.convert(file_str)

        # transfer the document string into a list of tokens
        pattern = r"(^[a-z]+(-?[a-z0-9]+)*$)|(^([a-z]\.)+$)"

        orig_tokens = []
        file_tokens = word_tokenize(file_str.lower())
        for w in file_tokens:
            if len(w) < 30 and re.search(pattern, w):
                orig_tokens.append(w)

        return orig_tokens

    def pp_corpus_tokenize(self, dname):
        """
        a. Transfer a corpus into a 2D list of word tokens arranged by documents with preprocessing
        b. Write the corpus into an output directory in which each file contains preprocessed
        word tokens in an input document

        :param dname: input directory name
        :return: a 2D list of word tokens representing the corpus
        """
        # create the output directory
        pp_dname = "pp_" + dname
        if not os.path.exists(pp_dname):
            os.makedirs(pp_dname)

        pp_tokens = []  # all tokens in a corpus arranged by documents

        # Process each document in the input directory
        for ifile in sorted(os.listdir(dname)):
            ifile = dname + "/" + ifile
            # Transfer a document into a list of tokens and add to the corpus list
            doc_tokens = self.pp_doc_tokenize(ifile)
            pp_tokens.append(doc_tokens)
            # Write the list of tokens into an output file
            pp_file = "pp_" + ifile
            self.output_tokens(pp_file, doc_tokens)

        return pp_tokens

    def pp_doc_tokenize(self, filename):
        """
        Transfer a document into a list of word tokens with preprocessing
        :param filename: a document
        :return:
        """
        # open input file and prepare PreProcessor
        input_file = open(filename, "r")
        mtpp = MyTextPreProcess.MyTextPreProcess()

        # Get the document string and transfer it into a list of preprocessed word tokens
        file_str = input_file.read().decode("utf-8", "ignore")
        # pp_tokens = []
        # for sent in sent_tokenize(file_str):
        #     pp_tokens.extend(mtpp.PreProcess(sent))
        pp_tokens = mtpp.PreProcess(file_str)

        return pp_tokens

    def output_tokens(self, output_name, tokens):
        """
        Write a list of tokens into an output files
        :param output_name: the filename of the output file
        :param tokens: a list of tokens
        """
        # write pp_tokens to a file <pp_filename>
        output_file = open(output_name, "w")
        for token in tokens:
            output_file.write(token +" ")


class FileDocTokenizer:

    def orig(self, filename):
        # Generate self.orig_tokens and self.orig_docs_list according to the input file
        converter = MyConvertUnicode()
        input_file = open(filename, "r")
        orig_tokens = []
        orig_docs_list = []

        for line in input_file:
            if len(line) >= 2:
                line = converter.convert(line)
                orig_docs_list.append(line)
                orig_tokens.append([token.lower() for token in word_tokenize(line) if token.isalpha()])
        return orig_docs_list, orig_tokens

    def preprocess(self, filename):
        # Generate self.pp_tokens and self.pp_docs_list according to the input file
        # Write self.pp_tokens into file <pp_filename>
        # Write self.pp_docs_list into file <docs_pp_filename>

        # open input file and prepare PreProcessor
        input_file = open(filename, "r")
        mtpp = MyTextPreProcess.MyTextPreProcess()

        # modify self.pp_docs_list & self.pp_tokens
        pp_docs_list = []
        pp_tokens = []

        for line in input_file:
            l2 = mtpp.PreProcess(line)
            if len(l2) >= 2:
                pp_docs_list.append(line)
                pp_tokens.append(l2)

        # write files
        self.output_pp(filename, pp_tokens)
        self.output_pp_docs_list(filename, pp_docs_list)

        return pp_docs_list, pp_tokens

    def output_pp(self, filename, pp_tokens):
        # write pp_tokens to a file <pp_filename>
        output_name = "pp_" + filename
        output_file = open(output_name, "w")
        for doc in pp_tokens:
            for token in doc:
                output_file.write(token + " ")
            output_file.write("\n")

    def output_pp_docs_list(self, filename, pp_docs_list):
        # write pp_docs_list to a file <docs_pp_filename>
        output_name = "docs_pp_" + filename
        output_file = open(output_name, "w")
        for line in pp_docs_list:
            output_file.write(line)

    def read_pp_docs_list(self, filename):
        # generate pp_docs_list from a previously output file after preprocessing
        pp_docs_list = []
        filename = "docs_" + filename
        input_file = open(filename, "r")
        for line in input_file:
            pp_docs_list.append(line)
        return pp_docs_list
