import numpy as np
import matplotlib.pyplot as plt
import sys
import random

#
# This program is used to plot topic coherence values change for each individual topic
#

if len(sys.argv) <=1:
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


start_wc = 10
stop_wc = 270
step_wc = 20
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, 20):
    ifile = open("reuters_LDA/tc_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    sd = float(ifile.readline().split()[1])
    randlist.append((avg, sd))

rand_avglist = [value[0] for value in randlist]
log_rand = [np.log(-v) for v in rand_avglist]


# init a 2D list to contain all topic coherence values for each topics
tclist = []
for tnum in range(topics_count):
    tclist.append([])


#
# put values in the 2D list
#
output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
for num in range(start_wc, stop_wc, step_wc):
    ifile = open(output+"/top_topics_"+str(num)+".txt")
    for line in ifile:
        if "Topic" in line:
            # format in the ifile: Topic num tc_value
            tid = int(line.split()[1])
            tclist[tid].append(float(line.split()[2])) 
                 
# plot
fig = plt.figure()
fig.suptitle("Reuters "+ corpus_type + " " + str(topics_count)+ " topics" ,fontsize=15)

plt.ylabel("log( - topic coherence)")
plt.xlabel("log(# of words)")


# red dashes, blue squares and green triangles
x_axis_rand = range(start_wc, stop_wc, 20)
log_x_rand =[np.log(v) for v in x_axis_rand]

line_rand, = plt.plot(log_x_rand,log_rand, color=(0,0,0), marker = "^")
for x, y in zip(log_x_rand, log_rand):
    plt.annotate("{:.2f}".format(float(y)), xy=(x,y))

x_axis = range(start_wc, stop_wc, step_wc)
log_x =[np.log(v) for v in x_axis]
#colordiff = int(16777215.0 / topics_count)
log_list = []
linelist = [0]*topics_count
for index, tid in enumerate(range(topics_count)):
    log_tc = [np.log(-v) for v in tclist[tid]]
    log_list.append(log_tc)
    # color
    randcolor = int(random.randint(1, 16777000))
    # colornum = int(tid * colordiff)
    colorhex = format(randcolor, "06x")

    linelist[index], = plt.plot(log_x,log_tc, color="#"+str(colorhex), marker = "o")
    plt.annotate("id: "+str(tid), xy=(log_x[0], log_tc[0]), xytext=(-35,0), textcoords='offset points')
legendlist = ["topic"+str(tid) for tid in range(topics_count)]
# plt.legend([line_rand, line_pos, line_neg, line_avg], ["random words", "most positive", "most negative", "avg"],loc='lower right')
plt.legend(linelist, legendlist,loc='lower right')


fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig(output + "/plot_eachtc.png")
