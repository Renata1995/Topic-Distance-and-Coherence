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


start_wc = 10
stop_wc = 270
step_wc = 20
# get tc values based on randomly generated numbers
randlist = []
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("reuters_LDA/tc_rand_"+str(num)+".txt")
    avg = float(ifile.readline().split()[1])
    sd = float(ifile.readline().split()[1])
    randlist.append((avg, sd))

rand_avglist = [value[0] for value in randlist]
log_rand = [np.log(-v) for v in rand_avglist]


# get tc values from topics
tclist = []  
for num in range(start_wc, stop_wc, step_wc):
    ifile = open("LDA_pp_reuters_"+corpus_type+"_t"+str(topics_count)+"/top_topics_"+str(num)+".txt")
    sub_tclist = []
    for line in ifile:
        if "Topic" in line:
            # format in the ifile: Topic num tc_value
            sub_tclist.append(float(line.split()[2]))
    # tuple: (most positive, most negative, avg, sd)
    tc_tuple = (sub_tclist[0], sub_tclist[-1], np.average(sub_tclist), np.std(sub_tclist))
    tclist.append(tc_tuple)

poslist = [value[0] for value in tclist]
neglist = [value[1] for value in tclist]
avglist = [value[2] for value in tclist]

log_pos = [np.log(-v) for v in poslist]
log_neg = [np.log(-v) for v in neglist]
log_avg = [np.log(-v) for v in avglist]

                 
# plot
fig = plt.figure()
fig.suptitle("Reuters "+corpus_type+str(topics_count)+ " topics" ,fontsize=15)

plt.ylabel("log( - topic coherence)")
plt.xlabel("log(# of words)")


# red dashes, blue squares and green triangles
x_axis = range(start_wc, stop_wc, step_wc)
log_x =[np.log(v) for v in x_axis]

line_rand, = plt.plot(log_x,log_rand, color=(0,0,0), marker = "^")
for x, y in zip(log_x,log_rand):
    plt.annotate("{:.2f}".format(float(y)), xy=(x,y))
    
line_pos, = plt.plot(log_x,log_pos, "r", marker = "o")
    
line_neg, = plt.plot(log_x,log_neg, "b", marker = "o")
    
line_avg, = plt.plot(log_x,log_avg, "g", marker = "o")
for x, y in zip(log_x,log_avg):
    plt.annotate("("+str("{:.2f}".format(float(x)))+", "+str("{:.2f}".format(float(y)))+")", xy=(x,y), xytext=(10,-10), textcoords='offset points')

plt.legend([line_rand, line_pos, line_neg, line_avg], ["random words", "most positive", "most negative", "avg"],loc='lower right')

plt.show()
