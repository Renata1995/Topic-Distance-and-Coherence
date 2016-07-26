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

if len(sys.argv) <= 3:
    te = "path"
else:
    te = sys.argv[3]


start_wc = 10
stop_wc = 260
step_wc = 10
# get tc values based on randomly generated numbers
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/"+te+"_median_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    randlist.append(avg)

# init a 2D list to contain all topic coherence values for each topics
tclist = []
for tnum in range(topics_count):
    tclist.append([])

#
# put values in the 2D list
#
output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
for num in range(start_wc, stop_wc, step_wc):
    ifile = open(output+"/"+te+"/w"+str(num)+".txt")

    content = [l for l in ifile]
        
    for index,line in enumerate(content):
        if "Topic" in line:
            tid = int(line.split()[1])
            median = content[index+2].split()[1]
            tclist[tid].append(float(median)) 
                 
# plot
fig = plt.figure()
fig.suptitle(te.upper() + "\nReuters "+ corpus_type + " " + str(topics_count)+ " topics" ,fontsize=15)

plt.ylabel(te.upper())
plt.xlabel("# of words with top probabilities")

x_axis = range(start_wc, stop_wc, step_wc)

line_rand, = plt.plot(x_axis,randlist, color=(0,0,0), marker = "^")
for x, y in zip(x_axis, randlist):
    plt.annotate("{:.2f}".format(float(y)), xy=(x,y))

linelist = [0]*topics_count
for index, tid in enumerate(range(topics_count)):
    # color
    randcolor = int(random.randint(1, 16777000))
    # colornum = int(tid * colordiff)
    colorhex = format(randcolor, "06x")

    linelist[index], = plt.plot(x_axis, tclist[index], color="#"+str(colorhex), marker = "o")
    plt.annotate("id: "+str(tid), xy=(x_axis[0], tclist[index][0]), xytext=(-35,0), textcoords='offset points')
linelist.append(line_rand)

legendlist = ["topic"+str(tid) for tid in range(topics_count)]
legendlist.append("random")
plt.legend(linelist, legendlist, bbox_to_anchor=(1.13, 1))


fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig(te+"_eachtc_"+corpus_type+"_"+str(topics_count)+".png")
