from scipy import stats
import sys
import utils.name_convention as namecon
from similarity.SimTopicLists import SimTopicLists

tclist, tctlist, wnlist = [],[],[]

wn_names = ["path", "wup", "lch", "res", "lin", "jcn"]
for n in range(len(wn_names)):
    wnlist.append([])

for src in ["pp_reuters", "pp_brown"]:
    for corpus_type in ["tfidf", "bow", "binary"]:
        for topics_count in [5,10,15, 20]:
            dname = namecon.get_output_dir(corpus_type, topics_count, src)

            subtclist = []
            ofile = open(dname + "/top_topics_20_start0.txt")
            for line in ofile:
                if "topic" in line:
                    subtclist.append(("tc"+src+corpus_type+str(topics_count)+line.split()[1],float(line.split()[2]), int(line.split()[1])))
            subtclist = list(sorted(subtclist, key=lambda x: x[2]))
            tclist.extend(subtclist)

            subtctlist = []
            ofile = open(dname + "/top_topics_tfidf_20.txt")
            for line in ofile:
                if "topic" in line:
                    subtctlist.append(("tct"+src+corpus_type+str(topics_count)+line.split()[1],float(line.split()[2]), int(line.split()[1])))
            subtctlist = list(sorted(subtctlist, key=lambda x: x[2]))
            tctlist.extend(subtctlist)


            for wi, name in enumerate(wn_names):
                ifile = open(dname + "/" + name + "/" + "w020_start0.txt")
                linelist = []
                for line in ifile:
                    linelist.append(line)

                subwlist = []
                for lindex, line in enumerate(linelist):
                    if line.startswith("Topic"):
                        tnum = line.split()[1]
                        mean = float(linelist[lindex+1].split()[1])
                        subwlist.append((name+src+corpus_type+str(topics_count)+tnum,mean, int(tnum)))
                subwlist = list(sorted(subwlist, key=lambda x: x[2]))
                wnlist[wi].extend(subwlist)

tcco = [v[1] for v in tclist]
tctco = [v[1] for v in tctlist]
wnco = []
for wn in wnlist:
    wn= list(sorted(wn, key=lambda x: x[2])) 
    wnco.append([v[1] for v in wn])

tcrank = list(sorted(tclist, key=lambda x: x[1]))
tcrank = [v[0] for v in tcrank]
tctrank = list(sorted(tctlist, key=lambda x: x[1]))
tctrank = [v[0] for v in tctrank]
wnrank = []
for wn in wnlist:
    wnr = list(sorted(wn, key=lambda x: x[1]))
    wnrank.append([v[0] for v in wnr])
    

ofile = open("coherence_correlation.txt","w")
cototal = []
cototal.append(("tc", tcco))
cototal.append(("tct", tctco))
for wi, wlist in enumerate(wnco):
    cototal.append((wn_names[wi], wlist))

for c1, co1 in enumerate(cototal[1:]):
    for co2 in cototal[:c1+1]:
        co_values1 = co1[1]
        co_values2 = co2[1]

        ofile.write(co1[0] + "  " + co2[0] +" : ")
        ofile.write(str(stats.pearsonr(co_values1, co_values2)) + "\n")


ofile = open("coherence_rank.txt", "w")
corank = []
corank.append(("tc", tcrank))
corank.append(("tct", tctrank))
for wi, wlist in enumerate(wnrank):
    corank.append((wn_names[wi], wlist))

for c1, co1 in enumerate(corank[1:]):
    for co2 in corank[:c1+1]:
        co_values1 = co1[1]
        co_values2 = co2[1]

        ofile.write(co1[0] + "  " + co2[0] +" : ")
        ofile.write(str(stats.kendalltau(co_values1, co_values2)) + "\n")

