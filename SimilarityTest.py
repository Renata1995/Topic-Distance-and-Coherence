from similarity.BCDistance import BCDistance
from utils.TopicIO import TopicIO
from similarity.SimTopicLists import SimTopicLists
import os
import shutil
import sys

# Calculate the similarity between two topics
topics_io = TopicIO()
stl = SimTopicLists()
idir = "topics"
ofile = "kl_test.txt"
dist_output = open(ofile, "w")

for i in range(1):
    t_1 = idir
    t_2 = idir

    t_list1 = topics_io.read_topics(t_1)
    t_list2 = topics_io.read_topics(t_2)

    dist_output.write("\n" + str(i) + " Topics: T_List 1\n")
    dist_output.write(str(i+1) + " Topics: T_List 2\n")
    stl.show_results(stl.kl_divergence(t_list1, t_list2), dist_output)
    # stl.show_results(stl.bc_distance(t_list1,t_list2), dist_output)
    #stl.show_results(stl.cos_distance(t_list1, t_list2), dist_output)
