import sys
import utils.name_convention as name
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) <= 1:
    tc = "tc"
else:
    tc = sys.argv[1]
    
if len(sys.argv) <= 2:
    src = "pp_reuters"
else:
    src = sys.argv[2]

if len(sys.argv) <= 3:
    measure = "mean"
else:
    measure = "median"

type_names = ["binary", "bow", "tfidf"]
typelist = [[],[],[]]

x_axis = [5,10,15,20]
for index, corpus_type in enumerate(type_names):
    for topics_count in x_axis:
        dname = name.get_output_dir(corpus_type, topics_count, src)

        if tc == "tc":
            ifile = open(dname + "/top_topics_20_start0.txt")
            tclist = []
            for line in ifile:
                if line.startswith("topic"):
                    tclist.append(float(line.split()[2]))
                            
        elif tc == "tct":
            ifile = open(dname + "/top_topics_tfidf_20.txt")
            tclist = []
            for line in ifile:
                if line.startswith("topic"):
                    tclist.append(float(line.split()[2]))
        else:
            ifile = open(dname + "/" + tc +"/w020_start0.txt")
            linelist = []
            for line in ifile:
                linelist.append(line)

            tclist = []
            for lindex, l in enumerate(linelist):
                if l.startswith("Topic"):
                    if measure == "mean":
                        value = linelist[lindex+1]
                    else:
                        value = linelist[lindex+2]
                    tclist.append(float(value.split()[1]))
        typelist[index].append(np.average(tclist))

# plot
fig = plt.figure()
if tc == "tc":
    title = "Co-occurrence Based Topic Coherence"
    ylabel = "Co-occurrence TC"
elif tc == "tct":
    title = "Tfidf Co-occurrence Based Topic Coherence"
    ylabel = "Tfidf Co-occurrence TC"
else:
    title = tc.upper() + " Coherence"
    ylabel = tc.upper()
    
fig.suptitle(title +" \n - " + src.replace("pp_","").title() ,fontsize=20)

plt.ylabel(ylabel)
plt.xlabel("# of topics")

linelist = [0, 0, 0]
for index, tclist in enumerate(typelist):
    color = [0, 0, 0]
    if index == 1:
        color[index] = 0.5
    else:
        color[index] = 0.9
    linelist[index], = plt.plot(x_axis, tclist, color=(color[0], color[1], color[2]), marker="o")
    for x, y in zip(x_axis, tclist):
        if index == 0:
            yoffset = 10
        elif index == 1:
            yoffset = 10
        elif index == 2:
            yoffset = 0
        plt.annotate("("+str(x)+", "+str("{:.2f}".format(float(y)))+")", xy=(x, y), color=(color[0], color[1], color[2]), fontsize=20,
                     xytext=(-25, yoffset), textcoords='offset points')

plt.legend(linelist, type_names, bbox_to_anchor=(1, -0.05), ncol=4)

fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig("plot_3comp_" + tc + "_" + src + ".png")

