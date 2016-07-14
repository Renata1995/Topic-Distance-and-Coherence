import numpy
from utils import TopicIO
from BCDistance import BCDistance


class BCInterpreter:
    """
    A helper class used in the interpretation of BC Distance
    """
    def __init__(self):
        self.bc = BCDistance()

    def bc_similarity(self, seq_size, sample_size=30, sample_times=20, degree=0.1, bc_times=20):
        """
        Calculate the average bc_distance between two similar distributions with certain parameters
        :param seq_size: the size of the sequence (population)
        :param sample_size: the size of the sample
        :param sample_times: times of sampling
        :param degree: degree of randomness.
        The smaller the number, the more sparse the distribution is.
        The larger the number, the  more uniform the distribution is.
        :param bc_times: times to calculate bc_distance
        :return: an averaged bc_distance value
        """
        bsum = 0
        for num in range(bc_times):
            dist1 = list(numpy.random.dirichlet([degree] * seq_size))
            dist2 = self.mean_rand_dist(dist1, seq_size,sample_size, sample_times)
            bsum += self.bc.distance(self.dist_to_topic(dist1), self.dist_to_topic(dist2))
        return bsum/bc_times

    def bc_difference(self, seq_size, degree1, degree2, bc_times=20):
        bsum = 0
        for num in range(bc_times):
            dist1 = list(numpy.random.dirichlet([degree1] * seq_size))
            dist2 = list(numpy.random.dirichlet([degree2] * seq_size))
            bsum += self.bc.distance(self.dist_to_topic(dist1), self.dist_to_topic(dist2))
        return bsum / bc_times

    def mean_rand_dist(self, dist, seq_size, sample_size=30, sample_times=50):
        """

        :param dist:
        :param seq_size:
        :param sample_size:
        :param sample_times:
        :return:
        """
        dist_list = []
        for num in range(sample_times):
            dist_list.append(self.rand_dist(dist, seq_size, sample_size))

        mean_dist = []
        for num in range(seq_size):
            mean_dist.append(sum([d[num] for d in dist_list])/sample_times)
        return mean_dist

    def rand_dist(self, dist, seq_size, sample_size):
        """
        Get a new distribution on a random sample from a population with a specific distribution
        :param dist: the distribution of the population
        :param seq_size: the range of the population
        :param sample_size: the size of the sample
        :return:
        """
        # get the random sample
        sample = numpy.random.choice(seq_size, sample_size, p=dist)

        # calculate distribution
        sample_dist = []
        for num in range(seq_size):
            sample_dist.append(float(list(sample).count(num))/float(sample_size))
        return sample_dist

    def dist_to_topic(self, dist):
        """
        Output a topic object with the input distribution
        :param dist: a distribution list
        :return: a topic object
        """
        topic = TopicIO.Topic()
        topic.words_dist = [(index,num) for index, num in enumerate(dist)]
        return topic




