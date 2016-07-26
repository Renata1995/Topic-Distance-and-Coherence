import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) <= 1:
    topics_count = 3
else:
    topics_count = sys.argv[1]

if len(sys.argv) <=2:
    corpus_type = "bow"
else:
    if sys.argv[2] == "t":
        corpus_type = "tfidf"
    elif sys.argv[2] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 3:
    tc = "path"
else:
    tc = sys.argv[3]

print corpus_type

if len(sys.argv) <= 4:
    startw = 0
else:
    startw = int(sys.argv[4])


start_wc = 10
stop_wc = 260
step_wc = 10
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/"+tc+"_median_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    randlist.append(avg)

output = "LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)
# get tc values from topics
tclist = []  
for num in range(start_wc, stop_wc, step_wc):
    if startw == 0:
        ifile = open(output+"/"+tc+"/w"+str(num)+".txt")
    else:
        ifile = open(output+"/"+tc+"/w"+str(num)+ "_start"+str(startw)+".txt")

    sub_tclist = []
    for line in ifile:
        if "Median" in line:
            sub_tclist.append(float(line.split()[1]))
    tclist.append(np.average(sub_tclist))

                 
# plot
fig = plt.figure()
fig.suptitle("Reuters "+corpus_type+"  "+str(topics_count)+ " topics" ,fontsize=15)

plt.ylabel(tc)
plt.xlabel("# of words")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)

line_rand, = plt.plot(x_axis, randlist, color=(0,0,0), marker = "^")
for x, y in zip(x_axis, randlist):
    plt.annotate("{:.3f}".format(float(y)), xy=(x,y), xytext =(5,0), textcoords='offset points')
    
line_avg, = plt.plot(x_axis, tclist, "g", marker = "o")
for x, y in zip(x_axis, tclist):
    if (x/10)%2 == 0:
        yoffset = 10
    else:
        yoffset = -30
    
    plt.annotate("("+str(x)+",\n"+str("{:.3f}".format(float(y)))+")", xy=(x,y), xytext=(-10,yoffset), textcoords='offset points')

plt.legend([line_rand, line_avg], ["random words", "avg of median"],loc='lower right')

fig = plt.gcf()
fig.set_size_inches(16,12)
if startw == 0:
    plt.savefig(output + "/plot_median_"+corpus_type+"_"+topics_count+"_"+tc+".png")
else:
    plt.savefig(output + "/plot_median_"+corpus_type+"_"+topics_count+"_"+tc+"_start"+str(startw)+".png")
