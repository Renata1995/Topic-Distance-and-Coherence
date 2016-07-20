class Topic:
    """
    A topic object is a list of tuples. Each tuple contains a word and its distribution
    """
    def __init__(self):
        self.words_dist = []

    def add(self,word_dist_tuple):
        self.words_dist.append(word_dist_tuple)

    def get(self,index):
        return self.words_dist[index]

    def size(self):
        return len(self.words_dist)

    def sort(self):
        self.words_dist = list(reversed(sorted(self.words_dist, key=lambda x: x[1])))

    def sublist(self, words_count):
        return self.words_dist[:words_count]

    def sublist_words(self, words_count):
        return [v[0] for v in self.words_dist[:words_count]]


