from abc import ABCMeta, abstractmethod


class SimABC:
    """
    similarity calculation abstract class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def distance(self):
        """
        Calculate the similarity between two topics
        :return:
        """
        pass
