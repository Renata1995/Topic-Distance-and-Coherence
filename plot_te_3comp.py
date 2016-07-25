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

start_wc = 10
stop_wc = 260
step_wc = 10
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/"+tc+"_median_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    randlist.append(avg)

typelist = [] 
for corpus_type in ("tfidf","bow","binary"):
    output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
    # get tc values from topics
    tclist = []  
    for num in range(start_wc, stop_wc, step_wc):
        ifile = open(output+"/"+tc+"/w"+str(num)+".txt")
        sub_tclist = []
        for line in ifile:
            if "Median" in line:
                sub_tclist.append(float(line.split()[1]))
        tclist.append(np.average(sub_tclist))
    typelist.append(tclist)

                 
# plot
fig = plt.figure()
fig.suptitle(tc.title()+" Similarity\nReuters 3 Corpus Type Comparison ("+str(topics_count)+ " topics)" ,fontsize=15)

plt.ylabel(tc)
plt.xlabel("# of words")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)

line_rand, = plt.plot(x_axis, randlist, color=(0,0,0), marker = "^")
for x, y in zip(x_axis, randlist):
    plt.annotate("{:.3f}".format(float(y)), xy=(x,y), xytext =(5,0), textcoords='offset points')

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

plt.legend([line_rand, linelist[0], linelist[1], linelist[2]], ["random words", "tfidf", "bow", "binary"],loc='lower right')

fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig("plot_median_3comp_"+topics_count+"_"+tc+".png")
