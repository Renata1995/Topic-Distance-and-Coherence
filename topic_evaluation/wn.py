from nltk.corpus import wordnet as wn
import numpy as np
from nltk import word_tokenize
import utils.name_convention as name
from exceptions import Exception
from Queue import Queue


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
                mlstr = ''.join(list(sorted([m, l])))
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
        elif tc == "lesk":
            func = self.lesk
        elif tc == "hso":
            func = self.hso
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
        elif tc == "lesk":
            func = self.lesk
        elif tc == "hso":
            func = self.hso
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
            ofile.write(key + " " + str(value) + "\n")

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

    def hso(self, s1, s2):
        if s1 == s2:
            return self.hso_cal(0, 0)

        # Init queue
        # Each item in squeue is a list of synsets
        squeue = Queue()
        # Element in squeue: [no_hyper(bool), direction, turns(int), path, last synset]
        squeue.put([False, 0, 0, 0, s1])

        while not squeue.empty():
            # get the last synsets list in the queue
            slist = squeue.get()
            no_hyper, direction, turns, path, last = slist[0], slist[1], slist[2], slist[3], slist[4]

            if path > 5 or turns > 1:
                return 0

            # If hypernyms are allowed
            if not no_hyper:
                if direction < 0: # go downwards before
                    new_turns = turns + 1
                else:
                    new_turns = turns

                new_direction = 1
                has_s2, hypers = self.hyper(last, s2)
                if has_s2:
                    return self.hso_cal(path+1, new_turns)
                else:
                    for synset in hypers:
                        slist_new = [False, new_direction, new_turns, path+1, synset]
                        squeue.put(slist_new)

            # get all related synsets of s1
            has_s2, hori = self.horizontal(last, s2)
            new_direction = 0
            if has_s2:
                return self.hso_cal(path+1, turns)
            else:
                # if any related nodes of <last> is not s2, revise the queue and start over
                for synset in hori:
                    slist_new = [True,new_direction, turns, path+1, synset]
                    squeue.put(slist_new)


            if direction > 0:
                new_turns = turns + 1
            else:
                new_turns = turns
            new_direction = -1
            hao_s2, hypos = self.hypos(last, s2)
            if hao_s2:
                return self.hso_cal(path+1, new_turns)
            else:
                for synset in hypos:
                    slist_new = [True,new_direction, new_turns, path+1, synset]
                    squeue.put(slist_new)


    def hso_cal(self, path, turns):
        sim = 6 - path - 1 * turns
        return sim

    def hyper(self, s1, s2):
        hypers = s1.hypernyms()
        if s2 in hypers:
            return True, []
        else:
            return False, hypers

    def horizontal(self, s1, s2):
        # horizontal relation
        horizontal = self.antonym(s1) + (self.pertainym(s1)) + (self.pertainym(s1))
        if s2 in horizontal:
            return True, []
        else:
            return False, horizontal

    def hypos(self, s1, s2):
        # down direction
        hypos = s1.hyponyms()
        if s2 in hypos:
            return True, []
        else:
            return False, hypos

    def antonym(self, s1):
        lemmas = s1.lemmas()
        antonyms = []
        for lemma in lemmas:
            antonyms.extend([l.synset() for l in lemma.antonyms()])
        return antonyms

    def pertainym(self, s):
        lemmas = s.lemmas()
        pertainyms = []
        for lemma in lemmas:
            pertainyms.extend([l.synset() for l in lemma.pertainyms()])
        return pertainyms

    def synonym(self, s):
        lemmas = s.lemmas()
        synonyms = []
        for lemma in lemmas:
            synonyms.extend([l.synset() for l in lemma.similar_tos()])
        return synonyms

        # def antonym(self, s1, s2):
        #     # Get all lemmas in each synset
        #     lemma_set1 = set(s1.lemmas())
        #     lemma_set2 = set(s2.lemmas())
        #
        #     # Compare whether a lemma in synset1 and a lemma in synset2 are antonym
        #     for lemma_s1 in lemma_set1:
        #         # Get all antonyms of the a lemma in synset1
        #         anto1 = set(lemma_s1.antonyms())
        #         # check whether any lemma in synset2 exist in this antonym set
        #         if set(anto1.intersection(lemma_set2))!= 0:
        #             return True
        #     return False
        #
        # def pertainym(self, s1, s2):
        #     # Get all lemmas in each synset
        #     lemma_set1 = set(s1.lemmas())
        #     lemma_set2 = set(s2.lemmas())
        #
        #     # Compare whether a lemma in synset1 and a lemma in synset2 are antonym
        #     for lemma_s1 in lemma_set1:
        #         # Get all antonyms of the a lemma in synset1
        #         anto1 = set(lemma_s1.pertainyms())
        #         # check whether any lemma in synset2 exist in this antonym set
        #         if set(anto1.intersection(lemma_set2)) != 0:
        #             return True
        #     return False
        #
        # def similarity(self, s1, s2):
        #     # Get all lemmas in each synset
        #     lemma_set1 = set(s1.lemmas())
        #     lemma_set2 = set(s2.lemmas())
        #
        #     # Compare whether a lemma in synset1 and a lemma in synset2 are antonym
        #     for lemma_s1 in lemma_set1:
        #         # Get all antonyms of the a lemma in synset1
        #         anto1 = set(lemma_s1.similar_tos())
        #         # check whether any lemma in synset2 exist in this antonym set
        #         if set(anto1.intersection(lemma_set2)) != 0:
        #             return True
        #     return False
        #
        #
        #
        #
        #
