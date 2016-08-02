from BCDistance import BCDistance
from KLDivergence import KLDivergence
from CosDistance import CosDistance
from similarity import Similarity


class SimTopicLists:
    """
    Compare similarities between topics in two topic lists
    """

    def __init__(self):
        self.bha = BCDistance()
        self.kl = KLDivergence()
        self.cs = CosDistance()
        self.sim = Similarity()

    # def cross_comp(self, topic_num1, topic_num2, dname, fnum=5):
    #     tm_list1 = []
    #     tm_list2 = []
    #     for num in range(1, fnum+1):
    #


    def bc_distance(self, t_list1, t_list2):
        """
        Compare the Bhattacharyya Distance between each of two topics in two topic lists and store the results
        in a 2D list
        :return: a 2D list stores the results
        """
        distance_list = []

        for value1 in t_list1:
            sub_list = [self.bha.distance(value1, value2) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def bc_coeff(self, t_list1, t_list2):
        """
        Compare the Bhattacharyya Distance between each of two topics in two topic lists and store the results
        in a 2D list
        :return: a 2D list stores the results
        """
        distance_list = []

        for value1 in t_list1:
            sub_list = [self.bha.bc_coeff(value1, value2) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def kl_divergence(self, t_list1, t_list2):
        """
        Compare the KL Divergence between each of two topics in two topic lists and store the results
        in a 2D list
        :return: a 2D list stores the results
        """
        distance_list = []

        for value1 in t_list1:
            sub_list = [self.kl.distance(value1, value2) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def cos_distance(self, t_list1, t_list2):
        """
            Compare the KL Divergence between each of two topics in two topic lists and store the results
            in a 2D list
            :return: a 2D list stores the results
            """
        distance_list = []

        for value1 in t_list1:
            sub_list = [self.cs.distance(value1, value2) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def kendall(self, t_list1, t_list2):
        """
            Compare the KL Divergence between each of two topics in two topic lists and store the results
            in a 2D list
            :return: a 2D list stores the results
            """
        distance_list = []

        for index1, value1 in enumerate(t_list1):
            sub_list = []
            for index2, value2 in enumerate(t_list2):
                result = self.sim.kendall_tau(value2, value1)
                sub_list.append(result)
            distance_list.append(sub_list)

        return distance_list

    def dcg(self, t_list1, t_list2, word_limit=0):
        """
            Compare the KL Divergence between each of two topics in two topic lists and store the results
            in a 2D list
            :return: a 2D list stores the results
            """
        distance_list = []

        if word_limit == 0:
            word_limit = len(t_list1)

        for value1 in t_list1:
            sub_list = [self.sim.dcg_similarity(value1, value2, word_limit) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def jaccard(self, t_list1, t_list2, threshold):
        """
            Compare the KL Divergence between each of two topics in two topic lists and store the results
            in a 2D list
            :return: a 2D list stores the results
            """
        distance_list = []

        for value1 in t_list1:
            sub_list = [self.sim.jaccard_coeff(value1, value2, threshold) for value2 in t_list2]
            distance_list.append(sub_list)

        return distance_list

    def find_smallest(self, num_list):
        if num_list[0] < num_list[1]:
            row_min, row_min2, i1, i2 = num_list[0], num_list[1], 0, 1
        else:
            row_min, row_min2, i1, i2 = num_list[1], num_list[0], 1, 0

        for index, value in enumerate(num_list):
            if value < row_min:
                row_min2, i2 = row_min, i1
                row_min, i1 = value, index
            elif (row_min < value < row_min2) or (row_min == value and i1 != index):
                row_min2, i2 = value, index

        return i1, i2

    def find_smallest_self(self, num_list):
        if num_list[0] < num_list[1]:
            row_min, row_min2, i1, i2 = num_list[0], num_list[1], 0, 1
        else:
            row_min, row_min2, i1, i2 = num_list[1], num_list[0], 1, 0

        for index, value in enumerate(num_list):
            if value < row_min:
                row_min2, i2 = row_min, i1
                row_min, i1 = value, index
            elif (row_min < value < row_min2) or (row_min == value and i1 != index):
                row_min2, i2 = value, index

        return i1, i2

    def find_largest_two(self, num_list):
        if num_list[0] > num_list[1]:
            row_max, row_max2, i1, i2 = num_list[0], num_list[1], 0, 1
        else:
            row_max, row_max2, i1, i2 = num_list[1], num_list[0], 1, 0

        for index, value in enumerate(num_list):
            if value > row_max:
                row_max2, i2 = row_max, i1
                row_max, i1 = value, index
            elif (row_max > value > row_max2) or (row_max == value and i1 != index):
                row_max2, i2 = value, index

        return i1, i2

    def find_largest_one(self, num_list):
        lmax = num_list[0]
        i = 0

        for index, value in enumerate(num_list):
            if value > lmax:
                lmax = value
                i = index
        return i

    def rank(self, nlist):
        # rank = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
        rank = list(range(0, len(nlist)))

        sorted_list = list(sorted(nlist))
        ranklist = {}
        for index, num in enumerate(sorted_list):
            ranklist[num] = rank[index]

        newlist = []
        for index, num in enumerate(nlist):
            newlist.append(str(ranklist[num]) + " " + str('{0:.6f}'.format(num)))
        return newlist

    def show_results_rank(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("<style>table, th, td {border: 1px solid black;}</style>")
        file.write("<table><thead><tr><th></th>")
        for value in range(len(distance_list[0])):
            file.write("<th> topic" + str(value) + "</th>")
        file.write("</tr></thead><tbody>")

        colordiff = int(16777215 / (len(distance_list[0])))

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write("<tr><td> topic" + str(index) + "</td>")
            # rank
            sublist = self.rank(sublist)
            for sub_i, value in enumerate(sublist):
                ranknum = float(value.split()[0])
                colornum = int(16777215 - ranknum * colordiff)
                color = format(colornum, "06X")
                file.write("<td><span style='background-color: #" + str(color) + "'>")
                file.write(value.split()[1])
                file.write("</span></td>")
            file.write("</tr>")
        file.write("</tbody></table>")

    def show_results_rank_bw(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("<style>table, th, td {border: 1px solid black;}</style>")
        file.write("<table><thead><tr><th></th>")
        for value in range(len(distance_list[0])):
            file.write("<th> topic" + str(value) + "</th>")
        file.write("</tr></thead><tbody>")

        colordiff = int(255 / (len(distance_list[0])))

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write("<tr><td> topic" + str(index) + "</td>")
            # rank
            sublist = self.rank(sublist)
            for sub_i, value in enumerate(sublist):
                ranknum = int(value.split()[0])
                colornum = str(255 - ranknum * colordiff)
                rgbstr = "rgb(" + colornum + "," + colornum + "," + colornum + ")"
                file.write("<td><span style='background-color: " + rgbstr + "'>")
                file.write(value.split()[1])
                file.write("</span></td>")
            file.write("</tr>")
        file.write("</tbody></table>")

    def show_results_rank_reverse(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("<style>table, th, td {border: 1px solid black;}</style>")
        file.write("<table><thead><tr><th></th>")
        for value in range(len(distance_list[0])):
            file.write("<th> topic" + str(value) + "</th>")
        file.write("</tr></thead><tbody>")

        colordiff = int(255.0 / (len(distance_list[0])))


        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write("<tr><td> topic" + str(index) + "</td>")
            # rank
            sublist = self.rank(sublist)
            for sub_i, value in enumerate(sublist):
                ranknum = int(value.split()[0])
                colornum = str(ranknum * colordiff)
                rgbstr = "rgb(" + colornum + "," + colornum + "," + colornum + ")"
                file.write("<td><span style='background-color: " + rgbstr + "'>")
                file.write(value.split()[1])
                file.write("</span></td>")
            file.write("</tr>")
        file.write("</tbody></table>")

    def show_results_value(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("<style>table, th, td {border: 1px solid black;}</style>")
        file.write("<table><thead><tr><th></th>")
        for value in range(len(distance_list[0])):
            file.write("<th> topic" + str(value) + "</th>")
        file.write("</tr></thead><tbody>")

        max_value = max([max(v) for v in distance_list])
        min_value = min([min(v) for v in distance_list])

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write("<tr><td> topic" + str(index) + "</td>")
            for sub_i, value in enumerate(sublist):
                percent = (value - min_value)/(max_value - min_value)
                colornum = str(int(255 * (1 - percent)))
                rgbstr = "rgb(" + colornum + "," + colornum + "," + colornum + ")"
                file.write("<td><span style='background-color: " + rgbstr + "'>")
                value = '{0:.6f}'.format(value)
                file.write(str(value))
                file.write("</span></td>")
            file.write("</tr>")
        file.write("</tbody></table>")

    def show_results_value_reverse(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("<style>table, th, td {border: 1px solid black;}</style>")
        file.write("<table><thead><tr><th></th>")
        for value in range(len(distance_list[0])):
            file.write("<th> topic" + str(value) + "</th>")
        file.write("</tr></thead><tbody>")

        max_list = []
        for sub in distance_list:
            max_list.append(max([v for v in sub if round(v, 6) != 1.000000]))
        max_value = max(max_list)
        min_value = min([min(v) for v in distance_list])

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write("<tr><td> topic" + str(index) + "</td>")
            for sub_i, value in enumerate(sublist):
                if round(value,6) == 1.000000:
                    colornum = "255"
                else:
                    percent = (value - min_value)/(max_value - min_value)
                    colornum = str(int(255 * percent))

                rgbstr = "rgb(" + colornum + "," + colornum + "," + colornum + ")"
                file.write("<td><span style='background-color: " + rgbstr + "'>")
                value = '{0:.6f}'.format(value)
                file.write(str(value))
                file.write("</span></td>")
            file.write("</tr>")
        file.write("</tbody></table>")


    def show_results(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("{:{w}}".format("T_List1/T_List2", w=width))
        for value in range(len(distance_list[0])):
            file.write('{:{w}}'.format("     topic" + str(value), w=width))
        file.write("\n")

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write('{:{w}}'.format("    topic" + str(index), w=width))
            # find row and col max
            rmax = self.find_largest_one(sublist)
            cmax_list = []
            for i in range(len(sublist)):
                col_list = [v[i] for v in distance_list]
                cmax_list.append(self.find_largest_one(col_list))

            for sub_i, value in enumerate(sublist):
                print value
                value = '{0:.6f}'.format(value)
                if sub_i == rmax and index != cmax_list[sub_i]:
                    file.write('{:{w}}'.format("|  **" + value, w=width))
                elif sub_i != rmax and index == cmax_list[sub_i]:
                    file.write('{:{w}}'.format("|  ++" + value, w=width))
                elif sub_i == rmax and index == cmax_list[sub_i]:
                    file.write('{:{w}}'.format("|  *+" + value, w=width))
                else:
                    file.write('{:{w}}'.format("|    " + value, w=width))
            file.write("\n" + "-" * width * (len(distance_list[0]) + 1) + "\n")

    def show_results_self(self, distance_list, file):
        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # calculate smallest results
        # show row labels
        file.write("{:{w}}".format("T_List1/T_List2", w=width))
        for value in range(len(distance_list[0])):
            file.write('{:{w}}'.format("     topic" + str(value), w=width))
        file.write("\n")

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write('{:{w}}'.format("    topic" + str(index), w=width))
            # find row and col max
            rmax = self.find_largest_one(sublist)

            for sub_i, value in enumerate(sublist):
                value = '{0:.6f}'.format(value)
                if sub_i == rmax:
                    file.write('{:{w}}'.format("|  **" + value, w=width))
                else:
                    file.write('{:{w}}'.format("|    " + value, w=width))
            file.write("\n" + "-" * width * (len(distance_list[0]) + 1) + "\n")

    def show_results_2min_self(self, distance_list, file):

        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # show row labels
        file.write("{:{w}}".format("T_List1/T_List2", w=width))
        for value in range(len(distance_list[0])):
            file.write('{:{w}}'.format("     topic" + str(value), w=width))
        file.write("\n")

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write('{:{w}}'.format("    topic" + str(index), w=width))
            # show data in each cell
            min_1, min_2 = self.find_smallest(sublist)
            for sub_i, value in enumerate(sublist):
                value = '{0:.6f}'.format(value)
                if sub_i == min_1:
                    file.write('{:{w}}'.format("|##" + value, w=width))
                elif sub_i == min_2:
                    file.write('{:{w}}'.format("| #" + value, w=width))
                else:
                    file.write('{:{w}}'.format("|   " + value, w=width))
            file.write("\n" + "-" * width * (len(distance_list[0]) + 1) + "\n")

    def show_results_2max_self(self, distance_list, file):

        """
        Show the results from the comp_topic_lists method
        :param distance_list: a 2D list of data
        """
        width = 14
        file.write("\ntopic List 1 is vertical and topic List 2 is horizontal\n")

        # show row labels
        file.write("{:{w}}".format("T_List1/T_List2", w=width))
        for value in range(len(distance_list[0])):
            file.write('{:{w}}'.format("     topic" + str(value), w=width))
        file.write("\n")

        for index, sublist in enumerate(distance_list):
            # show column labels
            file.write('{:{w}}'.format("    topic" + str(index), w=width))
            # show data in each cell
            max_1, max_2 = self.find_largest_two(sublist)
            for sub_i, value in enumerate(sublist):
                value = '{0:.6f}'.format(value)
                if sub_i == max_1:
                    file.write('{:{w}}'.format("|   " + value, w=width))
                elif sub_i == max_2:
                    file.write('{:{w}}'.format("| **" + value, w=width))
                else:
                    file.write('{:{w}}'.format("|   " + value, w=width))
            file.write("\n" + "-" * width * (len(distance_list[0]) + 1) + "\n")


    def write_distance(self, distance_list, ofile):
        for i1, sublist in enumerate(distance_list):
            for i2, value in enumerate(sublist[i1+1:]):
                ofile.write(str(value)+"\n")
        
                
