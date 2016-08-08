import sys

if len(sys.argv)<=1:
    corpus_type = "bow"
else:
    if sys.argv[1] == "t":
        corpus_type = "tfidf"
    elif sys.argv[1] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv)<=2:
    topics_count = 3
else:
    topics_count = sys.argv[2]

if len(sys.argv) <= 3:
    tfidf = False
else:
    if sys.argv[3] == "t":
        tfidf = True
    else:
        tfidf = False
        
if tfidf:
    ofname = "reuters_tfidftc_avg_"+corpus_type+"_t"+topics_count+".txt"
else:
    ofname = "reuters_tc_avg_"+corpus_type+"_t"+topics_count+".txt"
    
ofile = open(ofname, "w")
    
length = 30
for tc in range(10, 270, 20):
    for type in ["Word Counts: "+str(tc), "topic id", "TC", "AVG", "SD"]:
        ofile.write("{:{l}}".format(type, l=length))
    ofile.write("\n")

    if tfidf:
        ifile = open("LDA_pp_reuters_"+corpus_type+"_t"+topics_count+"/tc_tfidf_freq_"+str(tc)+".txt","r")
    else:
        ifile = open("LDA_pp_reuters_"+corpus_type+"_t"+topics_count+"/tc_freq_"+str(tc)+".txt","r")

    tlist = []
    tclist = []
    alist = []
    sdlist = []
    for line in ifile:
        if line.startswith("topic coherence"):
            tclist.append(line.split()[2])
        elif line.startswith("topic"):
            tlist.append(line.split()[1])
        elif line.startswith("AVG"):
            alist.append(line.split()[1])
        elif line.startswith("SD"):
            sdlist.append(line.split()[1])

    comblist = []
    for index, value in enumerate(tclist):
        comblist.append((tlist[index], float(tclist[index]), alist[index], sdlist[index]))
    comblist = list(reversed(sorted(comblist, key = lambda x:x[1])))
    
    for index, value in enumerate(comblist):
        ofile.write("{:{l}}".format(str(index), l=length))
        ofile.write("{:{l}}".format(value[0], l=length))
        ofile.write("{:{l}}".format(str(value[1]),l=length))
        ofile.write("{:{l}}".format(value[2],l=length))
        ofile.write("{:{l}}".format(value[3],l=length))
        ofile.write("\n")
    
    ofile.write("\n"+"-"*length*5+"\n")  
        
