import sys
import utils.name_convention as name
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
    topics_count = 3
else:
    topics_count = int(sys.argv[2])

if len(sys.argv) <= 3:
    src = "pp_reuters"
else:
    src = sys.argv[3]

if len(sys.argv) <= 4:
    tc = "path"
else:
    tc = sys.argv[4]

if len(sys.argv) <= 5:
    words_count = 10
else:
    words_count = int(sys.argv[5])

dname = name.get_output_dir(corpus_type, topics_count, src)
zerofile = dname + "/zeros_" + tc + "_w" + str(words_count) + ".txt"
zerofile = open(zerofile)

not_in_wn = []
no_distance = []
for line in zerofile:
    if "not in wn" in line:
        not_in_wn.append(line)
    elif "no distance" in line:
        no_distance.append(line)

zfile = dname + "/zeros_sum_" + tc + "_w" + str(words_count) + ".txt"
zfile = open(zfile,"w")
zfile.write("sum not in wn: "+str(len(not_in_wn))+"\n")
zfile.write("sum no distance: "+str(len(no_distance))+"\n")

for l in not_in_wn:
    zfile.write(l)
for l in no_distance:
    zfile.write(l)
