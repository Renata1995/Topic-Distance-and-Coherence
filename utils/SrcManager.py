import shutil
import random
import os


class SrcManager:
    def process_cats_file(self, fname, ofname):
        ifile = open(fname, "r")
        catslist = [tuple(line.split()) for line in ifile]

        filelist = [[]]
        i = 0
        filelist[0].append(catslist[0][1])
        for index, ctuple in enumerate(catslist[1:]):
            if catslist[index][1] == catslist[index - 1][1]:
                filelist[i].append(catslist[index][0])
            else:
                i += 1
                filelist.append([catslist[index][1], catslist[index][0]])

        ofile = open(ofname, "w")
        for sublist in filelist:
            for item in sublist:
                ofile.write(item + " ")
            ofile.write("\n")

    def process_cats_file2(self, dname, ofname):
        rawlist = [fname for fname in os.listdir(dname)]
        catslist = [tuple(line.split("_1_")) for line in rawlist]

        filelist = [[]]
        i = 0
        filelist[0].append(catslist[0][0])
        for index, ctuple in enumerate(catslist[1:]):
            if catslist[index][0] == catslist[index - 1][0]:
                filelist[i].append(catslist[index][0]+"_1_"+catslist[index][1])
            else:
                i += 1
                filelist.append([catslist[index][0], catslist[index][0]+"_1_"+catslist[index][1]])

        ofile = open(ofname, "w")
        for sublist in filelist:
            for item in sublist:
                ofile.write(item + " ")
            ofile.write("\n")

    def process_cats_file3(self, fname, ofname):
        ifile = open(fname, "r")
        catslist = [(line.split()[1], line.split()[0]) for line in ifile]
        catslist = list(sorted(catslist))
        for item in catslist:
            print item

        filelist = [[]]
        i = 0
        filelist[0].append(catslist[0][0])
        for index, ctuple in enumerate(catslist):
            fname = catslist[index][1].replace("/","_")
            if catslist[index][0] == catslist[index - 1][0]:
                filelist[i].append(fname)
            else:
                i += 1
                filelist.append([catslist[index][0], fname])

        ofile = open(ofname, "w")
        for sublist in filelist:
            for item in sublist:
                ofile.write(item + " ")
            ofile.write("\n")

    def src_to_one_dir(self, src, output):

        """
        Copy files in all sub_directories of the source data directory into one single directory
        :param src: source data directory name
        :param output: the output directory name
        """

        fname_list = []
        if not os.path.exists(output):
            os.makedirs(output)

        for sub in os.listdir(src):
            sub_path = src + "/" + sub
            for fname in os.listdir(sub_path):
                fpath = sub_path + "/" + fname

                # check whether the current file already exist
                # if exists, rename the current file
                ofname = output + "/" + sub + "_" + fname
                shutil.copyfile(fpath, ofname)
                fname_list.append(ofname.replace(output + "/", ""))

        return fname_list

    def src_to_name_list(self, src):
        name_list = []
        for dname in src:
            name_list.extend([fname for fname in os.listdir(dname)])
        return name_list
