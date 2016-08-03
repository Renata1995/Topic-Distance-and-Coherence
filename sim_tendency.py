import sys
import utils.name_convention as name
import numpy as np
import matplotlib.pyplot as plt

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
else:
    x_axis = range(10,50,10)

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

# plot
fig = plt.figure()
if sim == "kendall":
    title = sim + "'s tau correlation"
else:
    title = sim + " distance"
fig.suptitle(title.title()+" \n - " + src.replace("pp_","").title() ,fontsize=15)

plt.ylabel(sim.title())
plt.xlabel("# of topics")

linelist = [0, 0, 0]
for index, tclist in enumerate(typelist):
    color = [0, 0, 0]
    color[index] = 1
    linelist[index], = plt.plot(x_axis, tclist, color=(color[0], color[1], color[2]), marker="o")
    for x, y in zip(x_axis, tclist):
        if index == 0:
            yoffset = -15
        elif index == 1:
            yoffset = 20
        elif index == 2:
            yoffset = 10
        plt.annotate("("+str(x)+", "+str("{:.6f}".format(float(y)))+")", xy=(x, y), color=(color[0], color[1], color[2]),
                     xytext=(0, yoffset), textcoords='offset points')

plt.legend(linelist, type_names, bbox_to_anchor=(1, -0.05), ncol=4)

fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig("plot_3comp_" + sim + "_" + src + ".png")



