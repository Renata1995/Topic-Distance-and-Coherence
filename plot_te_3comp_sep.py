import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <= 1:
    topics_count = 3
else:
    topics_count = sys.argv[1]

if len(sys.argv) <= 2:
    tc = "path"
else:
    tc = sys.argv[2]

if len(sys.argv) <= 3:
    mean = True
else:
    mean = False

if mean:
    measure = "mean"
else:
    measure = "median"
print measure

start_wc = 10
stop_wc = 155
step_wc = 5

typelist = [] 
for corpus_type in ("binary","bow","tfidf"):
    output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
    # get tc values from topics
    tclist = []  
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open(output+"/"+tc+"/wsep5"+"_start"+str(num)+".txt")
        sub_tclist = []
        for line in ifile:
            if measure.title() in line:
                sub_tclist.append(float(line.split()[1]))
        tclist.append(np.average(sub_tclist))
    typelist.append(tclist)

                 
# plot
fig = plt.figure()
fig.suptitle(tc.upper()+" Topic Coherence\nReuters 3 Corpus 5-Word Seperation ("+str(topics_count)+ " topics)" ,fontsize=15)

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

plt.legend([linelist[0], linelist[1], linelist[2]], ["binary", "bow", "tfidf"],bbox_to_anchor=(1,-0.05), ncol=4)

fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig("plot_sep_"+measure+"_"+topics_count+"_"+tc+".png")