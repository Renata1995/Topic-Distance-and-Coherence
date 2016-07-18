from utils.WordCounter import WordCounter
from unittest import TestCase


class TestWrodCounter(TestCase):
    def setUp(self):
        self.corpus = [[(1, 3), (2, 3), (3, 5)], [(1, 2), (3, 4), (6, 2), (7, 1)], [(2, 3), (3, 1), (7, 4)]]
        self.wt = WordCounter()

    def test_total_words(self):
        self.assertEqual(self.wt.totalWords(self.corpus), 28)

    def test_word_frequency(self):
        corpus_dict = []
        for doc in self.corpus:
            corpus_dict.append(dict(doc))
        self.assertEqual(self.wt.countWords3(corpus_dict, 1), 5)
