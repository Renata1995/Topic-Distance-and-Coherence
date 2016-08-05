# Write coherence values from individual data directory to a single file

length = 30
for te in ["lesk"]:
    ofname = "reuters_coherence_"+te+".txt"
    ofile = open(ofname, "w")

    for tc in range(10,260,10):
        for type in ["Words: " + str(tc), "tfidf", "binary", "bow"]:
            ofile.write("{:{l}}".format(type, l=length))
        ofile.write("\n")

        tfile = open("LDA_pp_reuters_tfidf_t10/"+te+"/w"+str(tc)+".txt", "r")
        bfile = open("LDA_pp_reuters_binary_t10/"+te+"/w"+str(tc)+".txt", "r")
        cfile = open("LDA_pp_reuters_bow_t10/"+te+"/w"+str(tc)+".txt", "r")

        tlist = []
        for line in tfile:
            if line.startswith("Topic"):
                tlist.append(line.strip())
            if line.startswith("Mean"):
                tlist.append(line.strip())
        blist = []
        for line in bfile:
            if line.startswith("Topic"):
                blist.append(line.strip())
            if line.startswith("Mean"):
                blist.append(line.strip())
        clist = []
        for line in cfile:
            if line.startswith("Topic"):
                clist.append(line.strip())
            if line.startswith("Mean"):
                clist.append(line.strip())

        for index, line in enumerate(tlist):
            if(index%2 == 0):
                strf = str(index/2)
            else:
                strf = ""
            ofile.write("{:{l}}".format(strf, l=length))
            ofile.write("{:{l}}".format(line, l=length))
            ofile.write("{:{l}}".format(blist[index], l=length))
            ofile.write("{:{l}}".format(clist[index], l=length))
            ofile.write("\n")

        ofile.write("\n" + "-" * length * 5 + "\n")

