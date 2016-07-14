import math


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