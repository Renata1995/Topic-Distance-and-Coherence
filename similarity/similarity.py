from scipy import stats
import numpy as np


class Similarity:

    def jaccard_coeff(self, topic1, topic2, threshold=0):
        """
        Calculate the Bhattacharyya Coefficient between two topics
        """
        wset1 = set([w[0] for w in topic1.words_dist if w[1] > threshold])
        wset2 = set([w[0] for w in topic2.words_dist if w[1] > threshold])

        intersection =  wset1.intersection(wset2)
        union = wset1.intersection(wset2)
        return float(intersection)/float(union)

    def kendall_tau(self, topic1, topic2):
        return stats.kendalltau(topic1.list(), topic2.list())

    def dcg(self, topic1, topic2):
        topic1.sort()
        topic2.sort()

        wlist1 = topic1.list()
        wlist2 = topic2.list()


