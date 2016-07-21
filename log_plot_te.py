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



start_wc = 10
stop_wc = 270
step_wc = 20
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/te_median_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    randlist.append(avg)

log_rand = [np.log(v) for v in rand_list]


# get tc values from topics
tclist = []  
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)+"/"+tc+"/w"+str(num)+".txt")
    sub_tclist = []
    for line in ifile:
        sub_tclist.append(float(line.split()[1]))
    # tuple: (most positive, most negative, avg, sd)
    tclist.append(np.average(sub_tclist)

log_avg = [np.log(-v) for v in tclist]

                 
# plot
fig = plt.figure()
fig.suptitle("Reuters "+corpus_type++"  "+str(topics_count)+ " topics" ,fontsize=15)

plt.ylabel("log("+tc+")")
plt.xlabel("log(# of words)")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)
log_x =[np.log(v) for v in x_axis]

line_rand, = plt.plot(log_x,log_rand, color=(0,0,0), marker = "^")
for x, y in zip(log_x,log_rand):
    plt.annotate("{:.2f}".format(float(y)), xy=(x,y))
    
line_avg, = plt.plot(log_x,log_avg, "g", marker = "o")
for x, y in zip(log_x,log_avg):
    plt.annotate("("+str("{:.2f}".format(float(x)))+", "+str("{:.2f}".format(float(y)))+")", xy=(x,y), xytext=(10,-10), textcoords='offset points')

plt.legend([line_rand, line_avg], ["random words", "avg of median"],loc='lower right')

fig = plt.gcf()
fig.set_size_inches(16,12)
plt.savefig(output + "/log_plot_"+tc+".png")
