from topic_evaluation.wn import WordNetEvaluator
import sys
import utils.name_convention as name
from topic.topicio import TopicIO
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
from utils.WordCounter import WordCounter


if len(sys.argv) <= 1:
    corpus_type = "bow"
else:
    if sys.argv[1] == "t":
        corpus_type = "tfidf"
    elif sys.argv[1] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 2:
    topics_count = 3
else:
    topics_count = int(sys.argv[2])

if len(sys.argv) <= 3:
    src = "pp_reuters"
else:
    src = sys.argv[3]

if len(sys.argv) <= 4:
    tc = "path"
else:
    tc = sys.argv[4]

if len(sys.argv) <= 5:
    need_ic = False
else:
    if sys.argv[5] == "ic":
        need_ic = True
    else:
        need_ic = False

if len(sys.argv) <= 6:
    words_count = 10
else:
    words_count = int(sys.argv[6])

if len(sys.argv) <= 7:
    startw = 0
else:
    startw = int(sys.argv[7])

dname = name.get_output_dir(corpus_type, topics_count, src)

# read wp topics
tio = TopicIO()
tlist = tio.read_topics(dname + "/topics_doc_tfidf")

# generate te file name
fname = dname + "/" + tc + "/pre_doctfidf_"+str(words_count)+"_start"+str(startw)+".txt"
prefile = open(fname, "w")

# calculate topic evaluation values
tclist = []
te = WordNetEvaluator()
if not need_ic:
    for index, topic in enumerate(tlist):
        tclist.append([index, te.evaluate_write(topic, words_count, tc, prefile, startw=startw)])
else:
    reuters_ic = wn.ic(reuters, False, 0.0)
    for index, topic in enumerate(tlist):
        tclist.append([index, te.evaluate_ic_write(topic, words_count, reuters_ic, tc, prefile, startw=startw)])


