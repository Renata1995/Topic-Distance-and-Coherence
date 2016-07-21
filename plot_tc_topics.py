import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <= 1:
    topics_count = 3
else:
    topics_count = int(sys.argv[1])
    
if len(sys.argv) <=2:
    corpus_type = "bow"
else:
    if sys.argv[2] == "t":
        corpus_type = "tfidf"
    elif sys.argv[2] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"


start_wc = 10
stop_wc = 90
step_wc = 20
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/tc_rand_"+str(num)+".txt")
    avg = ifile.readline().split()[1]
    sd = ifile.readline().split()[1]
    randlist.append((avg, sd))

rand_avglist = [value[0] for value in randlist]


# get tc values from topics
tclist = []  
for tc in "3 4 5 6 7 8 9 10 15 20 30 50".split():
    topiclist = []
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open("LDA_pp_reuters_"+corpus_type+"_t"+str(tc)+"/top_topics_"+str(num)+".txt")
        sub_tclist = []
        for line in ifile:
            if "Topic" in line:
                # format in the ifile: Topic num tc_value
                sub_tclist.append(float(line.split()[2]))
        topiclist.append(np.average(sub_tclist))
    tclist.append(topiclist)

btclist = []  
for tc in "3 4 5 6 7 8 9 10 15 20 30 50".split():
    topiclist = []
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open("LDA_pp_reuters_binary_t"+str(tc)+"/top_topics_"+str(num)+".txt")
        sub_tclist = []
        for line in ifile:
            if "Topic" in line:
                # format in the ifile: Topic num tc_value
                sub_tclist.append(float(line.split()[2]))
        topiclist.append(np.average(sub_tclist))
    btclist.append(topiclist)

ctclist = []  
for tc in "3 4 5 6 7 8 9 10 15 20 30 50".split():
    topiclist = []
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open("LDA_pp_reuters_bow_t"+str(tc)+"/top_topics_"+str(num)+".txt")
        sub_tclist = []
        for line in ifile:
            if "Topic" in line:
                # format in the ifile: Topic num tc_value
                sub_tclist.append(float(line.split()[2]))
        topiclist.append(np.average(sub_tclist))
    ctclist.append(topiclist)
    
                 
# plot
fig = plt.figure()
fig.suptitle("TC - Reuters topic number comparison" ,fontsize=15)

plt.ylabel("topic coherence")
plt.xlabel("# of words")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)
line_rand, = plt.plot(x_axis,rand_avglist, "r")
for x, y in zip(x_axis,rand_avglist):
    plt.annotate("{:.2f}".format(float(y)), xy=(x,y))

colordiff = 1.0/(len(tclist)+5)
for index, value in enumerate(tclist):
    plt.plot(x_axis, tclist[index], color = (colordiff*index,0,0))

colordiff = 1.0/(len(btclist)+5)
for index, value in enumerate(tclist):
    plt.plot(x_axis, btclist[index], color = (0,colordiff*index,0))

colordiff = 1.0/(len(ctclist)+5)
for index, value in enumerate(tclist):
    plt.plot(x_axis, ctclist[index], color = (0,0,colordiff*index))


plt.legend([line_rand], ["random words"])

plt.show()
