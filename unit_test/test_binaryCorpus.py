from utils.BinaryCorpus import BinaryCorpus
from unittest import TestCase


class TestBinaryCorpus(TestCase):
    def test_binaryCorpus(self):
        corpus = [[(1, 3), (2, 3), (3, 5)], [(1, 2), (3, 4), (6, 2), (7, 1)], [(2, 3), (3, 1), (7, 4)]]
        binary = [[(1, 1), (2, 1), (3, 1)], [(1, 1), (3, 1), (6, 1), (7, 1)], [(2, 1), (3, 1), (7, 1)]]

        self.assertEqual(BinaryCorpus(corpus), binary)
