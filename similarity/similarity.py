from scipy import stats
from math import sqrt, log
import numpy as np
from utils.DistsDifferException import DistsDiffer
from scipy.stats import entropy
from scipy.spatial.distance import cosine


class Similarity:
    def cosine_distance(self, topic1, topic2):
        """
        Calculate the cosine similarity between two topics
        """
        # Check whether the two topics have the same dictionary
        if not topic1.size() == topic2.size():
            raise DistsDiffer("The two topics under calculation do not have the same dictionary")
        for index in range(topic1.size()):
            if not topic1.get(index)[0] == topic2.get(index)[0]:
                raise DistsDiffer("The two topics under calculation do not have the same dictionary")

        # Calculate cosine similarity
        t1 = [dtuple[1] for dtuple in topic1.words_dist]
        t2 = [dtuple[1] for dtuple in topic2.words_dist]
        return cosine(t1, t2)

    def bha_distance(self, topic1, topic2):
        """
        Calculate the Bhattacharyya Distance between two topics
        """
        bha_distance = -log(self.bc_coeff(topic1, topic2))
        return bha_distance

    def bc_coeff(self, topic1, topic2):
        """
        Calculate the Bhattacharyya Coefficient between two topics
        """
        if not topic1.size() == topic2.size():
            print "length"
            raise DistsDiffer("The two topics under calculation do not have the same dictionary")
        bc_coeff = 0.0

        for index, dict in enumerate(topic1.words_dist):

            topic2_dict = topic2.get(index)
            if not dict[0] == topic2_dict[0]:
                print dict[0] + "  " + topic2_dict[0]
                raise DistsDiffer("The two topics under calculation do not have the same dictionary")

            prob_product = dict[1] * topic2_dict[1]

            bc_coeff += sqrt(prob_product)

        return bc_coeff

    def kl_divergence(self, topic1, topic2):
        """
        Calculate the KL Divergence between two topics
        """
        # Check whether the two topics have the same dictionary
        if not topic1.size() == topic2.size():
            raise DistsDiffer("The two topics under calculation do not have the same dictionary")
        for index in range(topic1.size()):
            if not topic1.get(index)[0] == topic2.get(index)[0]:
                raise DistsDiffer("The two topics under calculation do not have the same dictionary")

        # Calculate a symmetric form of KL Divergence
        t1 = [dtuple[1] for dtuple in topic1.words_dist]
        t2 = [dtuple[1] for dtuple in topic2.words_dist]

        KL12 = entropy(t1, t2)
        KL21 = entropy(t2, t1)
        KLavg = (KL12 + KL21) / 2

        return KLavg

    def jaccard_distance(self, topic1, topic2, num_words=0):
        """
        Calculate the Jaccard Coefficient between two topics
        """
        topic1.sort()
        topic2.sort()

        wset1 = set(topic1.list_words(num_words))
        wset2 = set(topic2.list_words(num_words))

        intersection = wset1.intersection(wset2)
        union = wset1.union(wset2)
        return 1-float(len(intersection))/float(len(union))

    def kendall_tau(self, t1words, t2words):
        """
        :param t1words: a ranked list of words
        :param t2words: a ranked list of words
        :return: correlation between these two ranked lists
        """
        return stats.kendalltau(t1words,t2words)[0]

    def dcg(self, topic, word_limit=0):
        """
        Calculate discounted cumulative gain of a specific topic
        :param topic:
        :param word_limit:
        :return: DCG value of a specific topic
        """
        topic.sort()
        wlist2 = [v[1] for v in topic.list(word_limit)]

        dcg = float(wlist2[0])
        for index, value in enumerate(wlist2[1:]):
            i = index+2
            add = value/np.log2(i)
            dcg += add
        return dcg

    def dcg_difference(self, topic1, topic2, word_limit=0):
        """
        Calculate the difference between DCG of two topics
        :param topic1: a topic
        :param topic2: a topic
        :param word_limit: the number of top words
        :return:the difference between DCG of two topics
        """
        dcg_diff = np.absolute(self.dcg(topic1, word_limit) - self.dcg(topic2,word_limit))
        return dcg_diff




