import os
from unittest import TestCase

from gensim import models

from topic.topicio import TopicIO, Topic


class TestTopic(TestCase):
    def setUp(self):
        self.topic = Topic()
        self.topic.add((1, 0.3))
        self.topic.add((2, 0.5))

    def test_add(self):
        self.assertEqual(self.topic.words_dist, [(1, 0.3), (2, 0.5)])

    def test_size(self):
        self.assertEqual(self.topic.size(), 2)

    def test_get(self):
        self.assertEqual(self.topic.get(0), (1, 0.3))

    def test_sort(self):
        self.topic.sort()
        self.assertEqual(self.topic.words_dist, [(2,0.5), (1, 0.3)])

    def test_list_words(self):
        self.topic.add((3, 0.1))
        self.topic.add((4, 0.5))
        self.topic.add((5, 0.25))
        self.topic.add((5, 0.25))
        self.assertTrue(self.topic.list_words(3),[1,2,3])
        self.assertTrue(self.topic.list_words(3,1), [2, 3,4])
        self.assertTrue(self.topic.list_words(3,2), [3,4,5])


mock_t0 = Topic()
mock_t1 = Topic()
mock_t0.words_dist = [("a", 0.1), ("c", 0.2), ("b", 0.3), ("d", 0.4)]
mock_t1.words_dist = [("b", 0.15), ("c", 0.25), ("a", 0.03), ("d", 0.57)]

class mock_lda:
    def show_topics(corpus=0, num_topics=2, num_words=4, formatted=False):
        return [(0, mock_t0.words_dist), (1, mock_t1.words_dist)]

models.LdaModel = mock_lda


class TestTopicIO(TestCase):
    def setUp(self):
        self.topic_io = TopicIO()

    def test_write_and_read_topics(self):
        lda = models.LdaModel()
        dname = "topic_io"
        self.topic_io.write_topics(lda, "orig", 2, 4, dname)

        self.assertTrue(os.path.exists(dname))
        t_list = self.topic_io.read_topics(dname)

#        self.assertEqual(list(sorted(mock_t0.words_dist)), t_list[0][1].words_dist)






