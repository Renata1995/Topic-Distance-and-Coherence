from scipy import stats
import sys
import utils.name_convention as name
from similarity.SimTopicLists import SimTopicLists

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

dname = name.get_output_dir(corpus_type, topics_count, src)

stl = SimTopicLists()

distance_list = []
ofile = open(dname + "/sim_jaccard.txt", "r")
jlist = stl.read_distance_list(ofile)
distance_list.append(("jaccard", jlist))

ofile = open(dname + "/sim_kendall.txt", "r")
klist = stl.read_distance_list(ofile)
distance_list.append(("kendall", klist))

ofile = open(dname + "/sim_cosine.txt", "r")
cos_list = stl.read_distance_list(ofile)
distance_list.append(("cos", cos_list))

ofile = open(dname + "/sim_kl.txt", "r")
kl_list = stl.read_distance_list(ofile)
distance_list.append(("kl", kl_list))

ofile = open(dname + "/sim_bha.txt", "r")
bha_list = stl.read_distance_list(ofile)
distance_list.append(("bha", bha_list))


rank_list = []
jrank = stl.read_distance_rank(jlist, topics_count)
rank_list.append(("jaccard", jrank))
krank = stl.read_distance_rank(klist, topics_count)
rank_list.append(("kendall", klist))
cos_rank = stl.read_distance_rank(cos_list, topics_count)
rank_list.append(("cos", cos_list))
kl_rank = stl.read_distance_rank(kl_list, topics_count)
rank_list.append(("kl", kl_list))
bha_rank = stl.read_distance_rank(bha_list, topics_count)
rank_list.append(("bha", bha_list))

ofile = open(dname + "/sim_correlation.txt","w")
for index, list1 in enumerate(distance_list[1:]):
    for list2 in distance_list[:index+1]:
        sim_values1 = list1[1]
        sim_values2 = list2[1]

        ofile.write(list1[0]+"  " + list2[0]+" : ")
        ofile.write(str(stats.pearsonr(sim_values1, sim_values2))+"\n")

ofile = open(dname + "/sim_rank.txt","w")
for index, list1 in enumerate(rank_list[1:]):
    for list2 in rank_list[:index+1]:
        sim_values1 = list1[1]
        sim_values2 = list2[1]

        ofile.write(list1[0]+"  " + list2[0]+" : ")
        ofile.write(str(stats.kendalltau(sim_values1, sim_values2))+"\n")




