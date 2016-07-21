from nltk.corpus import wordnet as wn
import numpy as np
from nltk import word_tokenize
import utils.name_convention as name
from exceptions import Exception

class DuplicationKey(Exception):
    def __init__(self, message=""):
        print "Keys are duplicated."
        print message


class WordNetEvaluator:
    """
    The WordNetEvaluator class includes different methods based on wordnet to evaluate topics
    """
    def read_file_into_dict(self, ifname):
        ifile = open(ifname, "r")
        tcdict = {}
        for line in ifile:
            value = line.split()
            if value[0] not in tcdict:
                tcdict[value[0]] = value[1]
        return tcdict

    def get_values(self, topic, words_num, ifname):
        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.list_words(words_num)

        # prepare the dictionary
        tcdict = self.read_file_into_dict(ifname)

        # Calculate results
        results = []
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                mlstr = ''. join(list(sorted([m, l])))
                results.append(float(tcdict[mlstr]))
        rsum = sum(results)
        r_nozero = [v for v in results if v > 0]
        rmean = np.average(r_nozero)
        rmedian = np.median(r_nozero)

        return rsum, rmean, rmedian, results

    def evaluate(self, topic, words_num, tc):
        # Choose an evaluation method
        if tc == "lch":
            func = self.lch
        elif tc == "wup":
            func = self.wup
        else:
            tc = "path"
            func = self.path
        print "topic evaluation method: " + tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.list_words(words_num)

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
        # Choose an evaluation method
        if tc == "lin":
            func = self.lin
        elif tc == "jcn":
            func = self.jcn
        else:
            tc = "res"
            func = self.res
        print "topic evaluation method: " + tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.list_words(words_num)

        # Calculate results
        results = []
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                results.append(self.sim_words_ic(m, l, ic, func))
        rsum = sum(results)
        r_nozero = [v for v in results if v > 0]
        rmean = np.average(r_nozero)
        rmedian = np.median(r_nozero)

        return rsum, rmean, rmedian, results

    def evaluate_write(self, topic, words_num, tc, ofile):
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
        print "topic evaluation method: " + tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.list_words(words_num)

        # Calculate results
        results_dict = {}
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                mlstr = ''.join(list(sorted([m, l])))
                if mlstr not in results_dict:
                    results_dict[mlstr] = self.sim_words(m, l, func)

        for key, value in results_dict.iteritems():
            ofile.write(key+" "+str(value)+"\n")

        results = [value for key, value in results_dict.iteritems()]
        rsum = sum(results)
        r_nozero = [v for v in results if v > 0]
        rmean = np.average(r_nozero)
        rmedian = np.median(r_nozero)

        return rsum, rmean, rmedian, results

    def evaluate_ic_write(self, topic, words_num, ic, tc, ofile):
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
        print "topic evaluation method: " + tc

        # Get the <word_num>-word sub-list from the topic
        topic.sort()
        tlist = topic.list_words(words_num)

        # Calculate results
        results_dict = {}
        for index, m in enumerate(tlist[1:]):
            m_index = index + 1
            for l in tlist[:m_index]:
                mlstr = ''.join(list(sorted([m, l])))
                if mlstr not in results_dict:
                    results_dict[mlstr] = self.sim_words_ic(m, l, ic, func)

        for key, value in results_dict.iteritems():
            ofile.write(key + " " + str(value) + "\n")

        results = [value for key, value in results_dict.iteritems() if value > 0]
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

                if func == self.lch:
                    # lch requires two synsets have the same pos tag
                    if s1.pos() == s2.pos():
                        simlist.append(func(s1, s2))
                else:
                    simlist.append(func(s1, s2))

        if len(simlist) == 0:
            # if the word does not exist in the wordnet
            smax = 0.0
        elif max(simlist) is None:
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
                if s1.pos() == "s" or s2.pos() == "s":
                    simlist.append(0.0)
                elif s1.pos() == s2.pos():
                    simlist.append(func(s1, s2, ic))
        if len(simlist) == 0:
            # if the word does not exist in the wordnet
            smax = 0.0
        elif max(simlist) is None:
            smax = 0.0
        else:
            smax = max(simlist)

        return smax

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

    def lesk(self, s1, s2):
        def1 = s1.definition()
        def2 = s2.definition()

        d1_tokens = [v for v in word_tokenize(def1) if v.isalpha()]
        d2_tokens = [v for v in word_tokenize(def2) if v.isalpha()]

        intersection = set(d1_tokens).intersection(set(d2_tokens))
        return len(intersection)


