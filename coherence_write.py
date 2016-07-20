ofname = "reuters_coherence_10.txt"
ofile = open(ofname, "w")

length = 30
for tc in [3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 80, 100]:
    for type in ["Topics: " + str(tc), "tfidf", "binary", "bow"]:
        ofile.write("{:{l}}".format(type, l=length))
    ofile.write("\n")

    tfile = open("LDA_pp_reuters_tfidf_t" + str(tc) + "/top_topics_10.txt", "r")
    bfile = open("LDA_pp_reuters_binary_t" + str(tc) + "/top_topics_10.txt", "r")
    cfile = open("LDA_pp_reuters_bow_t" + str(tc) + "/top_topics_10.txt", "r")

    tlist = []
    for line in tfile:
        if line.startswith("topic"):
            tlist.append(line.strip())
    blist = []
    for line in bfile:
        if line.startswith("topic"):
            blist.append(line.strip())
    clist = []
    for line in cfile:
        if line.startswith("topic"):
            clist.append(line.strip())

    for index, line in enumerate(tlist):
        ofile.write("{:{l}}".format(str(index), l=length))
        ofile.write("{:{l}}".format(line, l=length))
        ofile.write("{:{l}}".format(blist[index], l=length))
        ofile.write("{:{l}}".format(clist[index], l=length))
        ofile.write("\n")

    ofile.write("\n" + "-" * length * 5 + "\n")
