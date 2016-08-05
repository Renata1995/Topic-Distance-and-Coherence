from topic.topicio import TopicIO
from similarity.SimTopicLists import SimTopicLists
import sys
import utils.name_convention as name

topics_io = TopicIO()
stl = SimTopicLists()

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

dtw = name.get_output_dir(corpus_type, topics_count, src)


t_1 = dtw + "/topics"
t_list1 = topics_io.read_topics(t_1)

bha_list = stl.bc_distance(t_list1, t_list1)
cos_list = stl.cos_distance(t_list1, t_list1)
kl_list = stl.kl_divergence(t_list1, t_list1)
jlist = stl.jaccard(t_list1, t_list1, 500)

kprepare = []
for topic in t_list1:
    topic.sort()
    kprepare.append(topic.list_words())
    
klist = stl.kendall(kprepare,kprepare)


ofile = open(dtw + "/sim_jaccard.txt", "w")
stl.write_distance(jlist, ofile)

ofile = open(dtw + "/sim_kendall.txt", "w")
stl.write_distance(klist, ofile)

ofile = open(dtw + "/sim_cosine.txt", "w")
stl.write_distance(cos_list, ofile)

ofile = open(dtw + "/sim_kl.txt", "w")
stl.write_distance(kl_list, ofile)

ofile = open(dtw + "/sim_bha.txt", "w")
stl.write_distance(bha_list, ofile)


