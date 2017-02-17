from utils.write_table import output
import utils.name_convention as name
import sys
import numpy as np

if len(sys.argv) <= 1:
    sim = "bha"
else:
    sim = sys.argv[1]

if len(sys.argv) <= 2:
    src = "pp_reuters"
else:
    src = sys.argv[2]


if src == "pp_reuters":
    x_axis = [10,20,30,40,50]
elif src == "pp_brown":
    x_axis = [12,14,16,18,20]


type_names = ["binary", "bow", "tfidf"]
typelist = [[], [], []]
for tindex, corpus_type in enumerate(type_names):
    for topics_count in x_axis:
        dname = name.get_output_dir(corpus_type, topics_count, src)

        ifile = open(dname + "/sim_"+sim + ".txt","r")

        value_list = []
        for line in ifile:
            v = float(line)
            value_list.append(v)

        typelist[tindex].append(np.average(value_list))

output(sim+".xls", sim, typelist, type_names)







