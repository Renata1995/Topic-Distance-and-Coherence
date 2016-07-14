from math import sqrt, log
from SimABC import SimABC
from utils.DistsDifferException import DistsDiffer


class BCDistance(SimABC):

    def distance(self, topic1, topic2):
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
            raise DistsDiffer("The two topics under calculation do not have the same dictionary")
        bc_coeff = 0.0

        for index, dict in enumerate(topic1.words_dist):

            topic2_dict = topic2.get(index)
            if not dict[0] == topic2_dict[0]:
                raise DistsDiffer("The two topics under calculation do not have the same dictionary")

            prob_product = dict[1] * topic2_dict[1]

            bc_coeff += sqrt(prob_product)

        return bc_coeff

