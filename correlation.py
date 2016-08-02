from scipy import stats
import sys
import utils.name_convention as name
from similarity.SimTopicLists import SimTopicLists

if len(sys.argv) <= 1:
    src = "pp_reuters"
else:
    src = sys.argv[1]

stl = SimTopicLists()

distance_list, rank_list = [], []
jtotal, ktotal, cos_total, kl_total, bha_total = [], [], [], [], []
jtotal_rank, ktotal_rank, costotal_rank, kltotal_rank, bhatotal_rank = [], [], [], [], []

for corpus_type in ["tfidf"]:
    for topics_count in [3]:
        dname = name.get_output_dir(corpus_type, topics_count, src)

        ofile = open(dname + "/sim_jaccard.txt", "r")
        jlist = stl.read_distance_list(ofile)
        jtotal.extend(jlist)

        ofile = open(dname + "/sim_kendall.txt", "r")
        klist = stl.read_distance_list(ofile)
        ktotal.extend(klist)

        ofile = open(dname + "/sim_cosine.txt", "r")
        cos_list = stl.read_distance_list(ofile)
        cos_total.extend(cos_list)

        ofile = open(dname + "/sim_kl.txt", "r")
        kl_list = stl.read_distance_list(ofile)
        kl_total.extend(kl_list)

        ofile = open(dname + "/sim_bha.txt", "r")
        bha_list = stl.read_distance_list(ofile)
        bha_total.extend(bha_list)

        jrank = stl.read_distance_rank(jlist, topics_count)
        jtotal_rank.extend(jrank)

        krank = stl.read_distance_rank(klist, topics_count)
        ktotal_rank.extend(krank)

        cos_rank = stl.read_distance_rank(cos_list, topics_count)
        costotal_rank.extend(cos_rank)

        kl_rank = stl.read_distance_rank(kl_list, topics_count)
        kltotal_rank.extend(kl_rank)

        bha_rank = stl.read_distance_rank(bha_list, topics_count)
        bhatotal_rank.extend(bha_rank)

distance_list.append(("jaccard", jtotal))
distance_list.append(("kendall", ktotal))
distance_list.append(("cos", cos_total))
distance_list.append(("kl", kl_total))
distance_list.append(("bha", bha_total))

rank_list.append(("jaccard", jtotal_rank))
rank_list.append(("kendall", ktotal_rank))
rank_list.append(("cos", costotal_rank))
rank_list.append(("kl", kltotal_rank))
rank_list.append(("bha", bhatotal_rank))

ofile = open("sim_correlation.txt", "w")
for index, list1 in enumerate(distance_list[1:]):
    for list2 in distance_list[:index+1]:
        sim_values1 = list1[1]
        sim_values2 = list2[1]

        ofile.write(list1[0]+"  " + list2[0]+" : ")
        ofile.write(str(stats.pearsonr(sim_values1, sim_values2))+"\n")

ofile = open("sim_rank.txt","w")
for index, list1 in enumerate(rank_list[1:]):
    for list2 in rank_list[:index+1]:
        sim_values1 = list1[1]
        sim_values2 = list2[1]

        ofile.write(list1[0]+"  " + list2[0]+" : ")
        ofile.write(str(stats.kendalltau(sim_values1, sim_values2))+"\n")




