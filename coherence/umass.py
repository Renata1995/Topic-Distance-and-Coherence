import numpy


class TopicCoherence:
    def coherence(self, sub_topic, corpus, epsilon=1):
        """
        Calculate topic coherence value of a topic/subtopic
        Notice: This method assumes that each doc in the corpus_bow is a dictionary

        :param sub_topic: a list of words
        :param corpus: a list of doc. each doc is a word freqency dictionary
        :return:
        """
        tc_sum = 0
        for index, m in enumerate(sub_topic[1:]):
            m_index = index + 1
            sublist = sub_topic[:m_index]

            for l in sublist:
                dl = self.word_doc_freq(l, corpus)
                dml = self.words_doc_cofreq(m, l, corpus)
                if dl > 0:
                    tc_sum += numpy.log(float(dml + epsilon) / dl)

        return tc_sum

    def coherence_dict(self, sub_topic, term_freq_dict, cofreq_dict, ofile, epsilon=1):
        """
        Calculate topic coherence based on a term frequency dict and a co-occurence frequency dict
        :param sub_topic: a (sub) topic
        :param term_freq_dict: a dictionary of term frequency
        :param cofreq_dict: a dictionary of co-occurrence frequency
        :param ofile: an output file to record each word pair in the topic and its contribution
        to the topic coherence value
        :return: coherence value
        """
        csum = 0.0  # init coherence value

        # calculate co-occurrence frequency / term frequency for each pair of words and
        # add this value to the coherence value
        flist = []
        for index, m in enumerate(sub_topic[1:]):
            m_index = index + 1
            sublist = sub_topic[:m_index]

            for l in sublist:
                dl = term_freq_dict[l]

                ml = list(sorted([m, l]))
                mlstr = str(ml[0]) + " " + str(ml[1])
                dml = cofreq_dict[mlstr]

                if dl > 0:
                    ftc = numpy.log(float(dml + epsilon) / float(dl))
                    csum += ftc
                    flist.append((mlstr, ftc))

        # output
        ofile.write("topic coherence: " + str(csum) + "\n")
        ofile.write("AVG: " + str(numpy.average([v[1] for v in flist])) + "\n")
        ofile.write("SD:  " + str(numpy.std([v[1] for v in flist])) + "\n")

        for ftuple in flist:
            ofile.write(ftuple[0] + "  " + str(ftuple[1] / csum) + "     " + str(ftuple[1]) + "/" + str(csum) + "\n")
        return csum

    def word_doc_freq(self, word, corpus):
        """
        For a word w and a document d,
        UMass TC:  document frequency = binary(w,d)
        Tfidf UMass TC: document frequency = tfidf(w,d)

        :param word: word id (int)
        :param corpus: a list of doc which consists of word id and word frequency tuples
        :return: document frequency of a word
        """
        freq = 0
        for doc in corpus:
            if word in doc.keys():
                freq += doc[word]
        return freq

    def words_doc_cofreq(self, word1, word2, corpus):
        """
        For words w1, w2 and a document d,
        For UMass TC: document co-occurrence =  binary (w1,d) * binary (w2,d)
        Tfidf UMass TC: document co-occurrence = tfidf(w1,d) * tfidf(w2,d)
        :param word1: word id 1 (int)
        :param word2: word id 2 (int)
        :param corpus: a list of doc which consists of word id and word frequency tuples
        :return: document co-occurrence frequency
        """
        freq = 0
        for doc in corpus:
            if word1 in doc.keys() and word2 in doc.keys():
                freq += (doc[word1] * doc[word2])
        return freq

    def word_list_doc_freq(self, wlist, corpus, dict):
        """
        Calculate term frequency for all words in a word list
        :param wlist: a word list
        :param corpus: a corpus (binary or tfidf) used to calculate term frequency
        :param dict: a gensim.corpora.dictioanry related with the input corpus
        :return: a dictionary of term frequency
        """
        flist = {}
        for w in wlist:
            flist[dict.get(w)] = self.word_doc_freq(w, corpus)
        return flist

    def words_cooccur(self, wlist, corpus, dict):
        """
        Calculate term co-occurrence for all words in a word list
        :param wlist: a word list
        :param corpus:  a corpus (tfidf or binary)
        :param dict: a gensim.corpora.dictioanry related with the input corpus
        :return: a dictionary of term co-occurrence values
        """

        flist = {}
        for index, w in enumerate(wlist[1:]):
            sublist = wlist[:index + 1]

            for l in sublist:
                # create a unique key for each two-word pair
                wl = list(sorted([dict.get(w), dict.get(l)]))
                wlstr = wl[0] + " " + wl[1]

                if wlstr not in flist:
                    flist[wlstr] = self.words_doc_cofreq(w, l, corpus)
        return flist

    def write_dict(self, dict, ofile):
        """
        Write a dictionary to a file
        :param dict: a dictionary
        :param ofile: output file name
        """
        ofile = open(ofile, "w")
        for key, value in dict.iteritems():
            ofile.write(str(key) + "+" + str(value) + "\n")

    def read_into_dict(self, ifile):
        """
        Read a file into a dictionary
        :param ifile: input file
        """
        ifile = open(ifile)
        fdict = {}
        for line in ifile:
            linelist = line.strip().split("+")
            fdict[linelist[0]] = float(linelist[1])
        return fdict
