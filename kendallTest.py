from topic.topicio import TopicIO
from similarity.SimTopicLists import SimTopicLists
import sys
import utils.name_convention as name

topics_io = TopicIO()
stl = SimTopicLists()

if len(sys.argv) <= 1:
    corpus_type = "tfidf"
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
    src = "pp_test"
else:
    src = sys.argv[3]

dtw = name.get_output_dir(corpus_type, topics_count, src)


t_1 = dtw + "/topics"
t_list1 = topics_io.read_topics(t_1)
jlist = stl.jaccard(t_list1, t_list1, 200)
klist = stl.kendall(t_list1, t_list1)
dlist = stl.dcg(t_list1, t_list1)

ofname = dtw + "/self-comp_rank_kendell.html"
dist_output = open(ofname, "w")
stl.show_results_rank_bw(klist, dist_output)
