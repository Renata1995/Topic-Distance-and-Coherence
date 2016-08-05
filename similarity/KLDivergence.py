from math import sqrt, log
from SimABC import SimABC
from utils.DistsDifferException import DistsDiffer
from scipy.stats import entropy


class KLDivergence(SimABC):

    def distance(self, topic1, topic2):
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
        KLavg = (KL12+KL21)/2

        return KLavg



