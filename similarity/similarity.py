from scipy import stats
import numpy as np


class Similarity:

    def jaccard_coeff(self, topic1, topic2, threshold=0):
        """
        Calculate the Bhattacharyya Coefficient between two topics
        """
        topic1.sort()
        topic2.sort()

        wset1 = set(topic1.list_words(threshold))
        wset2 = set(topic2.list_words(threshold))

        intersection = wset1.intersection(wset2)
        union = wset1.union(wset2)
        return float(len(intersection))/float(len(union))

    def kendall_tau(self, t1words, t2words):
        return stats.kendalltau(t1words,t2words)[0]

    def dcg(self, topic, word_limit = 0):
        topic.sort()
        wlist2 = [v[1] for v in topic.list(word_limit)]

        dcg = float(wlist2[0])
        for index, value in enumerate(wlist2[1:]):
            i = index+2
            add = value/np.log2(i)
            dcg += add
        return dcg

    def dcg_similarity(self, topic1, topic2, word_limit):
        dcg_diff = np.absolute(self.dcg(topic1, word_limit) - self.dcg(topic2,word_limit))
        return dcg_diff




