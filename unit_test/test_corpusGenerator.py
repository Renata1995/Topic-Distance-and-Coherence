from utils.CorpusGenerator import CorpusGenerator
from unittest import TestCase
from preprocess import DocTokenizer
from shutil import rmtree
import os

raw_corpus = ['1 3 5 2'.split(), '1 2 4 6 1'.split(), '1 5 6'.split(), '2 3 3'.split()]


def mock_tokenize(self, dname):
    return raw_corpus

DocTokenizer.DirDocTokenizer.orig_corpus_tokenize = mock_tokenize


class TestCorpusGenerator(TestCase):

    def setUp(self):
        self.cgen = CorpusGenerator()

    def test_corpus_to_tokens(self):
        result = '1 3 5 2 1 2 4 6 1 1 5 6 2 3 3'.split()
        self.assertEqual(self.cgen.corpus_to_tokens(raw_corpus), result)

    def test_generate_corpus(self):
        output_str = ""
        rmtree("rand_gen_corpus")

        self.cgen.generate_corpus("gen_corpus")
        self.assertTrue(os.path.exists("rand_gen_corpus"))

        for fname in os.listdir("rand_gen_corpus"):
            fname = "rand_gen_corpus/" + fname
            f = open(fname, "r")
            output_str += f.read()

        output_str.strip()
        output = output_str.split()
        orig = '1 3 5 2 1 2 4 6 1 1 5 6 2 3 3'.split()

        self.assertEqual(list(sorted(output)), list(sorted(orig)))
        self.assertNotEqual(orig, output)







