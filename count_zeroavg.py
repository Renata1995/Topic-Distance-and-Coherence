import sys
import utils.name_convention as name
import numpy as np

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
    words_count = 150
else:
    words_count = int(sys.argv[5])

word_pairs = pow((words_count - 1),2)/2
ofile = open("wn_zeros_summary.txt", "w")

for tc in "path wup lch lin res jcn".split():
    ofile.write(tc + ":  ")
    avgwn_list = []
    avgdist_list = []
    
    for corpus_type in ["tfidf", "bow","binary"]:
        for topics_count in [5,10,15,20]:
            dname = name.get_output_dir(corpus_type, topics_count, src)
            zfile = open(dname + "/zeros_sum_" + tc + "_w" + str(words_count) + ".txt")
            
            not_in_wn = int(zfile.readline().split(":")[1])
            no_distance = int(zfile.readline().split(":")[1])
            
            avg_wn = float(not_in_wn)/(topics_count * word_pairs)
            avgwn_list.append(avg_wn)
            avg_dis = float(no_distance)/(topics_count * word_pairs)
            avgdist_list.append(avg_dis)
    ofile.write("not in wn: " + str(np.average(avgwn_list))+ "  no distance: " + str(np.average(avgdist_list))+"\n")
