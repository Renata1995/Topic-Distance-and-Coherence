from nltk.corpus import wordnet as wn
import numpy as np


class WordNetEvaluator:
    """
    The WordNetEvaluator class includes different methods based on wordnet to evaluate topics
    """
    def evaluate(self, topic, words_num, tc):
        """
        Evaluate a topic by calculating a similarity score for each word pair in the topic
        :param topic: A topic including word distribution pairs
        :type topic: A topic object
        :param words_num: A number to indicate how many words with top probabilities in the topic to be used
        :param tc: A string indicates method to use.
        a) tc = "lch":  use LCh similarity method to evaluate the topic
        b) tc = "wup":  use WuP similarity method to evaluate the topic
        c) tc is equal to anything else or missing: use PATH similarity method to evaluate the topic

        :return:
        rsum: the sum of the similarity value of each word pair
        rmean: the mean of the similarity value of each word
        rmedian: the mean of the similarity value of each word pair
        results: a list of all similarity values
        """
        # Choose an evaluation method
        if tc == "lch":
            func = self.lch
        elif tc == "wup":
            func = self.wup
        else:
            tc = "path"
            func = self.path
        print "topic evaluation method: "+tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.sublist_words(words_num)

        # Calculate results
        results = []
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                results.append(self.sim_words(m, l, func))
        rsum = sum(results)
        r_nozero = [v for v in results if v > 0]
        rmean = np.average(r_nozero)
        rmedian = np.median(r_nozero)

        return rsum, rmean, rmedian, results

    def evaluate_ic(self, topic, words_num, ic, tc):
        """
            Evaluate a topic by calculating a similarity score for each word pair in the topic
            An information content file is needed

            :param topic: A topic including word distribution pairs
            :type topic: A topic object
            :param words_num: A number to indicate how many words with top probabilities in the topic to be used
            :param ic: An information content file
            :param tc: A string indicates method to use.
            a) tc = "lin":  use LIN similarity method to evaluate the topic
            b) tc = "jcn":  use JCN similarity method to evaluate the topic
            c) tc is equal to anything else or missing: use RES similarity method to evaluate the topic

            :return:
            rsum: the sum of the similarity value of each word pair
            rmean: the mean of the similarity value of each word
            rmedian: the mean of the similarity value of each word pair
            results: a list of all similarity values
            """
        # Choose an evaluation method
        if tc == "lin":
            func = self.lin
        elif tc == "jcn":
            func = self.jcn
        else:
            tc = "res"
            func = self.res
        print "topic evaluation method: "+tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.sublist_words(words_num)

        # Calculate results
        results = []
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                results.append(self.sim_words_ic(m, l, ic, func))
        rsum = sum(results)
        rmean = np.average(results)
        rmedian = np.median(results)

        return rsum, rmean, rmedian, results

    def sim_words(self, w1, w2, func):
        w1_synsets = wn.synsets(w1)
        w2_synsets = wn.synsets(w2)

        simlist = []
        for s1 in w1_synsets:
            for s2 in w2_synsets:
                simlist.append(func(s1, s2))

        if len(simlist)== 0:
            print w1+"  "+w2
            return 0.0

        if max(simlist)== None:
            smax = 0.0
        else:
            smax = max(simlist)

        return smax

    def sim_words_ic(self, w1, w2, ic, func):
        w1_synsets = wn.synsets(w1)
        w2_synsets = wn.synsets(w2)

        simlist = []
        for s1 in w1_synsets:
            for s2 in w2_synsets:
                if s1.pos() == s2.pos():
                    simlist.append(func(s1, s2, ic))
        print str(simlist)

        return max(simlist)

    # Similarity measures that do not require an information content file
    def path(self, s1, s2):
        return s1.path_similarity(s2)

    def lch(self, s1, s2):
        return s1.lch_similarity(s2)

    def wup(self, s1, s2):
        return s1.wup_similarity(s2)

    # Similarity measures that require an information content dictionary
    def lin(self, s1, s2, ic):
        return s1.lin_similarity(s2, ic)

    def res(self, s1, s2, ic):
        return s1.res_similarity(s2, ic)

    def jcn(self, s1, s2, ic):
        return s1.jcn_similarity(s2, ic)
