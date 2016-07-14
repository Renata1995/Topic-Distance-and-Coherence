from utils.TopicIO import Topic
import numpy


class TopicCoherence:
    def topic_coherence(self, sub_topic, corpus_bow):
        """

        Notice: This method assumes that each doc in the corpus_bow is a dictionary

        :param sub_topic: a list of words
        :param corpus_bow: a list of doc. each doc is a word freqency dictionary
        :return:
        """
        csum = 0
        for index, m in enumerate(sub_topic[1:]):
            sublist = sub_topic[:index]

            for l in sublist:
                dl = self.word_doc_freq(l, corpus_bow)
                dml = self.words_doc_cofreq(m, l, corpus_bow)
                if dl > 0:
                    csum += numpy.log(float(dml+1)/dl)
        return csum

    def word_doc_freq(self, word, corpus_bow):
        freq = 0
        for doc in corpus_bow:
            if word in doc.keys():
                freq+=1
        return freq

    def words_doc_cofreq(self, word1, word2, corpus_bow):
        freq = 0
        for doc in corpus_bow:
            if word1 in doc.keys() and word2 in doc.keys():
                freq += 1
        return freq
