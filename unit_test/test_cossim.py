from unittest import TestCase

from topic.topicio import Topic
from similarity.CosDistance import CosDistance
from utils.DistsDifferException import DistsDiffer


class TestCosSim(TestCase):
    def setUp(self):
        self.cs = CosDistance()
        self.topic1 = Topic()
        self.topic2 = Topic()

        self.topic1.words_dist = [(1, 0.1), (2, 0.2), (3, 0.3), (4, 0.4)]
        self.topic2.words_dist = [(1, 0.15), (2, 0.25), (3, 0.03), (4, 0.57)]

    def test_similarity(self):
        result = self.cs.distance(self.topic1, self.topic2)
        self.assertEqual(round(result, 5), 0.13974)

        # if the two topics do not have the same directory, assertionError will be thrown
        self.topic1.words_dist = [(1, 0.33), (2, 0.33), (3, 0.34)]
        self.assertRaises(DistsDiffer, self.cs.distance, self.topic1, self.topic2)

        self.topic1.words_dist = [(1, 0.1), (2, 0.2), (5, 0.3), (4, 0.4)]
        self.assertRaises(DistsDiffer, self.cs.distance, self.topic1, self.topic2)