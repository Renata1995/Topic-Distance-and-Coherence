from preprocess.DocTokenizer import DirDocTokenizer
import os
import random
from shutil import rmtree

class CorpusGenerator:
    """
    Generate a random corpus according to a given corpus.

    Notice:
    a. The given corpus should be already preprocessed.
    b. If a is satisfied, the random corpus does not need to be preprocessed any more.

    Preprocessing the random corpus and the original corpus will result in different vocabularies due to
    tagging and stemming. Therefore, it's better to preprocess the original corpus first and input a
    preprocessed corpus to generate a random corpus

    """
    def __init__(self):
        self.dt = DirDocTokenizer()

    def generate_corpus(self, dname):
        """
        Input a corpus and generate a random corpus that satisfies the following requirements:
        1. Has the same token set
        2. Has the same number of docs
        3. Each doc has the same length as that of the original doc
        :param dname: the directory name of the input corpus
        """
        # Get the num of docs and the length of each doc
        corpus = self.dt.orig_corpus_tokenize(dname)
        num_docs = len(corpus)
        doc_len_list = [len(doc) for doc in corpus]

        # Transfer the corpus into a list of word tokens
        all_tokens = self.corpus_to_tokens(corpus)

        # create the output directory
        output_dir = "rand_" + dname
        if os.path.exists(output_dir):
            rmtree(output_dir)
        os.makedirs(output_dir)

        # write each file
        for i in range(num_docs):
            fname = output_dir +"/rand_corpus_" + str(i) + ".txt"
            ofile = open(fname, "w")

            for j in range(doc_len_list[i]):
                index = random.randrange(len(all_tokens))
                ofile.write(all_tokens[index]+' ')
                del all_tokens[index]

    def corpus_to_tokens(self, corpus):
        """
        Transfer a 2D list corpus into a large list of word tokens
        :param corpus: a 2 2D list of word tokens
        :return: a 1D list of word tokens
        """
        all_tokens = []
        for doc in corpus:
            all_tokens.extend(doc)
        return all_tokens





