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
                    csum += numpy.log(float(dml + 1) / dl)
        return csum

    def tc_dict(self, sub_topic, doc_freq_list, cofreq_list, ofile):
        csum = 0.0
        flist = []
        for index, m in enumerate(sub_topic[1:]):
            m_index = index + 1
            sublist = sub_topic[:m_index]

            for l in sublist:
                dl = doc_freq_list[l]

                ml = list(sorted([m, l]))
                mlstr = str(ml[0]) + " " + str(ml[1])
                dml = cofreq_list[mlstr]

                if dl > 0:
                    ftc = numpy.log(float(dml + 1) / float(dl))
                    csum += ftc
                    flist.append((mlstr, ftc))
        flist = list(sorted(flist, key = lambda x:x[1]))
        ofile.write("Topic coherence: "+str(csum)+"\n")
        ofile.write("AVG: " + str(numpy.average([v[1] for v in flist]))+"\n")
        ofile.write("SD:  " + str(numpy.std([v[1] for v in flist])) + "\n")
        for ftuple in flist:
            ofile.write(ftuple[0]+"  "+str(ftuple[1]/csum)+"     "+str(ftuple[1])+"/"+str(csum)+"\n")
        return csum

    def word_doc_freq(self, word, corpus_bow):
        freq = 0
        for doc in corpus_bow:
            if word in doc.keys():
                freq += 1
        return freq

    def words_doc_cofreq(self, word1, word2, corpus_bow):
        freq = 0
        for doc in corpus_bow:
            if word1 in doc.keys() and word2 in doc.keys():
                freq += 1
        return freq

    def word_list_doc_freq(self, wlist, corpus, dict):
        flist = {}
        for w in wlist:
            flist[dict.get(w)] = self.word_doc_freq(w, corpus)
        return flist

    def words_cooccur(self, wlist, corpus, dict):
        flist = {}
        for index, w in enumerate(wlist[1:]):
            sublist = wlist[:index+1]
            for l in sublist:
                wl = list(sorted([dict.get(w), dict.get(l)]))
                wlstr = wl[0] + " " + wl[1]
                if wlstr not in flist:
                    flist[wlstr] = self.words_doc_cofreq(w, l, corpus)
        return flist


    def write_freqlist(self, freq_list, ofile):
        ofile = open(ofile, "w")
        for key, value in freq_list.iteritems():
            ofile.write(str(key)+"+"+str(value)+"\n")

    def read_flist(self, ifile):
        ifile = open(ifile)
        fdict = {}
        for line in ifile:
            linelist = line.split("+")
            fdict[linelist[0]] = int(linelist[1])
        return fdict

