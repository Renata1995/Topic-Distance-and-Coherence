class Topic:
    """
    A topic object is a list of tuples. Each tuple contains a word and its probability in the topic
    """

    def __init__(self):
        """
        Initiate a Topic object.
        """
        self.words_dist = []

    def add(self, word_prob_tuple):
        """
        Add a word-probability tuple to the topic
        :param word_prob_tuple: (word,probability)
        """
        self.words_dist.append(word_prob_tuple)

    def get(self, t_index):
        """
        Get a specific word-probability tuple by index number
        :param t_index: index number
        :return: the word-probability tuple at t_index in the topic
        """
        return self.words_dist[t_index]

    def size(self):
        """
        :return: The size of the vocabulary of the current topic
        """
        return len(self.words_dist)

    def sort(self):
        """
        Sort the topic by probability values
        """
        self.words_dist = list(reversed(sorted(self.words_dist, key=lambda x: x[1])))

    def list(self, words_count=0, start=0):
        """
        Get the word-probability tuple list
        :param words_count: the number of tuples included in the list
        :param start: the start point of the list
        :return: a list of word-probability tuples
        """
        if words_count <= 0:
            words_count = len(self.words_dist)
        return self.words_dist[start:start+words_count]

    def list_words(self, words_count=0, start=0):
        """
        Get a list of words in the topic
        :param words_count: the number of words included in the list
        :param start: the start point of the list
        :return: a list of words
        """
        if words_count <= 0:
            words_count = len(self.words_dist)
        return [v[0] for v in self.words_dist[start:start+words_count]]
