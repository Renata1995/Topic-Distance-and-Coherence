from topic.topicio import TopicIO
from similarity.SimTopicLists import SimTopicLists
import sys
import utils.name_convention as name
<<<<<<< HEAD
=======
from scipy import stats
>>>>>>> c0bd379ba5dc846ac9d61bb4c627bc32a09ca49e

topics_io = TopicIO()
stl = SimTopicLists()

if len(sys.argv) <= 1:
<<<<<<< HEAD
    corpus_type = "tfidf"
=======
    corpus_type = "bow"
>>>>>>> c0bd379ba5dc846ac9d61bb4c627bc32a09ca49e
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
<<<<<<< HEAD
    src = "pp_test"
=======
    src = "pp_reuters"
>>>>>>> c0bd379ba5dc846ac9d61bb4c627bc32a09ca49e
else:
    src = sys.argv[3]

dtw = name.get_output_dir(corpus_type, topics_count, src)


t_1 = dtw + "/topics"
t_list1 = topics_io.read_topics(t_1)
<<<<<<< HEAD
jlist = stl.jaccard(t_list1, t_list1, 200)
klist = stl.kendall(t_list1, t_list1)
dlist = stl.dcg(t_list1, t_list1)

ofname = dtw + "/self-comp_rank_kendell.html"
dist_output = open(ofname, "w")
stl.show_results_rank_bw(klist, dist_output)
=======
jlist = stl.jaccard(t_list1, t_list1, 500)

kprepare = []
for topic in t_list1:
    topic.sort()
    kprepare.append(topic.list_words())
    
klist = stl.kendall(kprepare,kprepare)


ofname = dtw + "/self-comp_kendell.txt"
dist_output = open(ofname, "w")
stl.show_results_2min_self(klist, dist_output)


ofname = dtw + "/self-comp_rank_kendell.html"
dist_output = open(ofname, "w")
stl.show_results_rank_reverse(klist, dist_output)

ofname = dtw + "/self-comp_jaccard.txt"
dist_output = open(ofname, "w")
stl.show_results_2min_self(jlist, dist_output)

ofname = dtw + "/self-comp_rank_jaccard.html"
dist_output = open(ofname, "w")
stl.show_results_rank_reverse(jlist, dist_output)

>>>>>>> c0bd379ba5dc846ac9d61bb4c627bc32a09ca49e
