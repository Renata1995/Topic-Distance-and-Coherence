from topic_evaluation.wn import WordNetEvaluator
from unittest import TestCase
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
from topic.topic import Topic


class TestTopicEvaluator(TestCase):
    def setUp(self):
        self.te = WordNetEvaluator()

    def test_sim_words(self):
        self.assertEqual(self.te.sim_words("dog", "dog", self.te.path), 1.0)
        topic = Topic()
        topic.words_dist = [("cat", "0.1")] * 2
        topic.words_dist.extend([("dog", "0.2")]*3)

        self.assertEqual(self.te.evaluate(topic, 3, "wup"), (3.0, 1.0, 1.0, [1.0, 1.0, 1.0]))

    def test_sim_words_ic(self):
        reuters_ic = wn.ic(reuters, False, 0.0)
        self.assertTrue(isinstance(self.te.sim_words_ic("dog", "cat", reuters_ic, self.te.res), float))
        topic = Topic()
        topic.words_dist =  [("dog", 0.3), ("cat",0.2), ("rabbit", 0.15), ("table", 0.35)]
        rsum, rmean, rmedian, rlist = self.te.evaluate_ic(topic, 3, reuters_ic, "lin")
        self.assertTrue(isinstance(rsum, float))
        self.assertTrue(isinstance(rmean, float))
        self.assertTrue(isinstance(rmedian, float))
        self.assertTrue(isinstance(rlist, list))
        self.assertTrue(len(rlist) == 3)
