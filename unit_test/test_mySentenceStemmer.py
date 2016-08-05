from preprocess.MySentenceStemmer import MySentenceStemmer
from unittest import TestCase

class TestSentenceStemmer(TestCase):
    def setUp(self):
        self.st = {}
        self.stemmer = MySentenceStemmer(self.st)
    def test_stem(self):
        str = " Hello, how are you?"
        result = ['Hello', ',', 'how', 'be', 'you', '?']
        self.assertEqual(result, self.stemmer.stem(str))