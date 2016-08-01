import numpy as np


#
#  Generate binary corpus by a term-frequency corpus
#

def BinaryCorpus(corpus):
    cnew = []
    for c1 in corpus:
        s = [];
        for q in c1:
            q1 = list(q);
            q1[1] = 1
            s.append(tuple(q1))
        cnew.append(s);
    return cnew


def arg_tfidf(bow_corpus, dictionary):
    """
    Transfer a bow corpus into an augmented tfidf corpus

    For term t in document d,
    tf = 0.5 + raw frequency of t / max raw frequency in d
    idf = log(total document/document frequency of t)

    :param bow_corpus: a bow corpus
    :param dictionary: dictionary of the bow corpus
    :return: an augmented tfidf corpus
    """
    tfidf_corpus = []
    for index, doc in enumerate(bow_corpus):
        if len(doc) != 0:
            max_tf = max([v[1] for v in doc])
            tfidf_doc = []

        for wtuple in doc:
            key = wtuple[0]
            raw_frequency = wtuple[1]

            tf = float(raw_frequency)/max_tf
            df = dictionary.dfs[key]
            idf = np.log(float(dictionary.num_docs)/df)

            tfidf = tf * idf
            tfidf_doc.append((key, tfidf))

        tfidf_corpus.append(tfidf_doc)

    return tfidf_corpus


