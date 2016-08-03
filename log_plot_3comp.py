import numpy as np
import numpy
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <= 1:
    topics_count = 3
else:
    topics_count = sys.argv[1]

start_wc = 10
stop_wc = 150
step_wc = 5
# get tc values based on randomly generated numbers
randlist = []
for num in range(10,150,10):
    ifile = open("reuters_LDA/tc_rand_" + str(num) + ".txt")
    avg = ifile.readline().split()[1]
    sd = ifile.readline().split()[1]
    randlist.append((avg, sd))

rand_avglist = [value[0] for value in randlist]

# get tc values from topics
tlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("LDA_pp_reuters_tfidf_t" + str(topics_count) + "/top_topics_" + str(num) + "_start0.txt")
    sub_tclist = []
    for line in ifile:
        if "topic" in line:
            # format in the ifile: Topic num tc_value
            sub_tclist.append(float(line.split()[2]))
    # tuple: (most positive, most negative, avg, sd)
    tlist.append(np.average(sub_tclist))

blist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("LDA_pp_reuters_binary_t" + str(topics_count) + "/top_topics_" + str(num) + "_start0.txt")
    sub_tclist = []
    for line in ifile:
        if "topic" in line:
            # format in the ifile: Topic num tc_value
            sub_tclist.append(float(line.split()[2]))
    # tuple: (most positive, most negative, avg, sd)
    blist.append(np.average(sub_tclist))

clist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("LDA_pp_reuters_bow_t" + str(topics_count) + "/top_topics_" + str(num) + "_start0.txt")
    sub_tclist = []
    for line in ifile:
        if "topic" in line:
            # format in the ifile: Topic num tc_value
            sub_tclist.append(float(line.split()[2]))
    # tuple: (most positive, most negative, avg, sd)
    clist.append(np.average(sub_tclist))
    

# plot
fig = plt.figure()
fig.suptitle("Co-occurence Based Topic Coherence \nReuters 3 Corpus Type Comparison(3 topics)", fontsize=15)

plt.ylabel("log( - topic coherence)")
plt.xlabel("log(# of words)")

# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)
x_axis = [np.log(v) for v in x_axis]

rand_x = list(range(10,150,10))
rand_x = [np.log(v) for v in rand_x]
line_rand, = plt.plot(rand_x, [np.log(-float(v)) for v in rand_avglist], color=(0, 0, 0), marker="o")
for x, y in zip(x_axis, rand_avglist):
    plt.annotate("{:.2f}".format(float(y)), xy=(x, y))

line_pos, = plt.plot(x_axis, [np.log(-v) for v in tlist], "g", marker="^")

line_neg, = plt.plot(x_axis, [np.log(-v) for v in clist], "b", marker="^")

line_avg, = plt.plot(x_axis, [np.log(-v) for v in blist], "r", marker="^")

plt.legend([line_rand, line_pos, line_neg, line_avg], ["random words", "tfidf", "bow", "binary"], loc="lower right")

fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig("plot_3comp_tc_t" + str(topics_count) + "_reuters" + ".png")
