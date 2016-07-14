from similarity.BCDistance import BCDistance
from utils.TopicIO import Topic
from utils.DistsDifferException import DistsDiffer
import unittest


class TestBCDistance(unittest.TestCase):
    def setUp(self):
        self.bc = BCDistance()
        self.topic1 = Topic()
        self.topic2 = Topic()

        self.topic1.words_dist = [(1, 0.1), (2, 0.2), (3, 0.3), (4, 0.4)]
        self.topic2.words_dist = [(1, 0.15), (2, 0.25), (3, 0.03), (4, 0.57)]

    def test_bc_coeff(self):
        bc_coeff = self.bc.bc_coeff(self.topic1,self.topic2)
        self.assertEqual(round(bc_coeff, 3), 0.918)

        # if the two topics do not have the same directory, assertionError will be thrown
        self.topic1.words_dist = [(1, 0.33), (2, 0.33), (3, 0.34)]
        self.assertRaises(DistsDiffer, self.bc.bc_coeff, self.topic1, self.topic2)

        self.topic1.words_dist = [(1, 0.1), (2, 0.2), (5, 0.3), (4, 0.4)]
        self.assertRaises(DistsDiffer, self.bc.bc_coeff, self.topic1, self.topic2)

    def test_similarity(self):
        similarity = self.bc.distance(self.topic1, self.topic2)
        self.assertEqual(round(similarity, 3), 0.085)

