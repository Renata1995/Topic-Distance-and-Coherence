import numpy as np
import matplotlib.pyplot as plt
import sys
import random

if len(sys.argv) <= 1:
    topics_count = 3
else:
    topics_count = sys.argv[1]

if len(sys.argv) <= 2:
    tc = "path"
else:
    tc = sys.argv[2]


start_wc = 10
stop_wc = 260
step_wc = 10


# get tc values from topics
typelist = [] 
for corpus_type in ("binary","bow","tfidf"):
    output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
    # get tc values from topics
    tclist = []  
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open(output+"/"+tc+"/w"+str(num)+"_start0.txt")
        sub_tclist = []
        for line in ifile:
            if "Median" in line:
                sub_tclist.append(float(line.split()[1]))
        tclist.append(np.average(sub_tclist))
    typelist.append(tclist)

notoplist = []
#topwords = [20, 30, 40, 50, 60, 70]
topwords = [20,30]
for startw in topwords:
    output = "LDA_pp_reuters_binary_t"+str(topics_count)
    # get tc values from topics
    tclist = []  
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open(output+"/"+tc+"/w"+str(num)+"_start"+str(startw)+".txt")
        sub_tclist = []
        for line in ifile:
            if "Median" in line:
                sub_tclist.append(float(line.split()[1]))
        tclist.append(np.average(sub_tclist))
    notoplist.append(tclist)

                 
# plot
fig = plt.figure()
fig.suptitle(tc.upper()+" Topic Coherence\nReuters 3 Corpus Type Comparison ("+str(topics_count)+ " topics)" ,fontsize=15)

plt.ylabel(tc.upper())
plt.xlabel("# of words")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)

linelist = [0,0,0]
for index, tclist in enumerate(typelist):
    color = [0,0,0]
    color[index] = 1
    linelist[index], = plt.plot(x_axis, tclist, color = (color[0],color[1],color[2]), marker = "o")
    for x, y in zip(x_axis, tclist):
        if (x/10)%2 == 0:
            yoffset = 10
        else:
            yoffset = -15
        
        plt.annotate(str("{:.3f}".format(float(y))), xy=(x,y),color = (color[0],color[1],color[2]), xytext=(-10,yoffset), textcoords='offset points')

linelist2 = [0]*len(notoplist)
colordiff = 0.9 / len(notoplist)
for index, tclist in enumerate(notoplist):
    randcolor = int(random.randint(1, 16777000))
    # colornum = int(tid * colordiff)
    colorhex = format(randcolor, "06x")
    linelist2[index], = plt.plot(x_axis, tclist, color = "#"+str(colorhex), marker = "^")
    for x, y in zip(x_axis, tclist):
        if (x/10)%2 == 0:
            yoffset = 10
        else:
            yoffset = -15
        
        plt.annotate(str("{:.3f}".format(float(y))), xy=(x,y),color = "#"+str(colorhex) , xytext=(-10,yoffset), textcoords='offset points')

legendlist = ["binary", "bow", "tfidf"]
for n in topwords:
    legendlist.append(str(n))
linelist.extend(linelist2)

plt.legend(linelist, legendlist, loc='lower right',bbox_to_anchor=(1.13,0))

fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig("plot_bnotop_"+topics_count+"_"+tc+".png")
