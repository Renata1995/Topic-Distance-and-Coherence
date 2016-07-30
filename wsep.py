from topic.topicio import TopicIO
from topic.topic import Topic
import utils.name_convention as name
import sys

if len(sys.argv) <= 1:
    corpus_type = "bow"
else:
    if sys.argv[1] == "t":
        corpus_type = "tfidf"
    elif sys.argv[1] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 2:
    topics_count = 8;
else:
    topics_count = int(sys.argv[2]);

if len(sys.argv) <= 3:
    src = "pp_reuters"
else:
    src = sys.argv[3];

if len(sys.argv) <= 4:
    tc = "path"
else:
    tc = sys.argv[4]
    
if len(sys.argv) <= 5:
    words_count = 5
else:
    words_count = int(sys.argv[5])

if len(sys.argv) <= 6:
    startw = 0
else:
    startw = int(sys.argv[6])

if len(sys.argv) <= 7:
    max_words = 250
else:
    max_words = int(sys.argv[7])

output = "LDA_" + src + "_" + corpus_type + "_t" + str(topics_count)



fname = output + name.te_preprocess(tc, max_words, 0)
prefile = open(fname, "r")

worddict = {}
for line in prefile:
    l = line.split()
    if l[0] not in worddict:
        worddict[l[0]] = float(l[1])

        


tio = TopicIO()
tlist = tio.read_topics(output + "/topics")


tlist_sep = []
for num in range(topics_count):
    tlist_sep.append([])
    
for num in range(0,155,5):
    wepfile = open(output+"/"+tc+"/wsep"+str(words_count)+"_start"+str(num)+".txt")

    linelist = []
    for line in wepfile:
        linelist.append(line)

    for index, l in enumerate(linelist):
               
        if "Topic" in l:
            tid = int(l.split()[1])
            tcmean = float(linelist[index+1].split()[1])
            tlist_sep[tid].append(tcmean)


ofile = open("wordsep_"+tc+"_"+src+"_"+corpus_type+"_t"+str(topics_count)+".txt", "w")
for tindex, t in enumerate(tlist):
    t.sort()
    tlist = t.list(max_words)
    ofile.write("\nTopic: "+str(tindex)+"\n")
    for windex, num in enumerate(range(0,155,5)):
        sublist = tlist[num:num+words_count]
        ofile.write("\n"+tc+": "+str(tlist_sep[tindex][windex])+"\n")
        for word in sublist:
            ofile.write(word[0]+"  ")
        ofile.write("\n")

        for i, m in enumerate(sublist[1:]):
            m = m [0]
            m_i = i+1
            for l in sublist[:m_i]:
                l = l[0]
                ofile.write("\n"+ m +" "+l+": ")
                ml_list = list(sorted([m,l]))
                key = "".join(ml_list)
                ofile.write(str(worddict[key]))
        ofile.write("\n----------------")
                
    ofile.write("\n---------------------------------------------------------\n")
                    
        
    

