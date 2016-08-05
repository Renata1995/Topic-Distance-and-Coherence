import unittest
import similarity
from similarity.SimTopicLists import SimTopicLists


def mock_bc(self, v1, v2):
    return v1 + v2

similarity.BCDistance.BCDistance.distance = mock_bc
similarity.BCDistance.BCDistance.bc_coeff = mock_bc


class TestSimTopicLists(unittest.TestCase):
    def setUp(self):
        self.stl = SimTopicLists()
        self.t_list1 = [(1, 1), (2, 2), (3, 3), (4, 4)]
        self.t_list2 = [(1, 3), (2, 5), (3, 7), (4, 1)]

    # def test_bc_distance(self):
    #     mock_results = [[4, 6, 8, 2], [5, 7, 9, 3], [6, 8, 10, 4], [7, 9, 11, 5]]
    #     self.assertEqual(self.stl.bc_distance(self.t_list1, self.t_list2), mock_results)
    #
    # def test_bc_coeff(self):
    #     mock_results = [[4, 6, 8, 2], [5, 7, 9, 3], [6, 8, 10, 4], [7, 9, 11, 5]]
    #     self.assertEqual(self.stl.bc_coeff(self.t_list1, self.t_list2), mock_results)

    def test_find_smallest(self):
        list = [0,10,3,7,2,8,9,30,1,5]
        print self.stl.find_smallest(list)
        self.assertEqual(self.stl.find_smallest(list), (0, 8))

        list = [6, 0, 36, 18, 34, 8, 9, 30, 20, 5]
        self.assertEqual(self.stl.find_smallest(list), (1, 9))

        list = [20, 10, 3, 7, 20, 3, 9, 30, 15, 5]
        self.assertEqual(self.stl.find_smallest(list), (2, 5))

        list = [2, 1, 3, 7, 20, 3, 9, 30, 15, 5]
        self.assertEqual(self.stl.find_smallest(list), (1, 0))

    def test_find_largest(self):
        list = [0, 10, 3, 7, 2, 8, 9, 30, 1, 5]
        self.assertEqual(self.stl.find_largest_two(list), (7, 1))

        list = [6, 0, 36, 18, 34, 8, 9, 30, 20, 5]
        self.assertEqual(self.stl.find_largest_two(list), (2, 4))

        list = [30, 10, 3, 7, 20, 3, 9, 30, 15, 5]
        self.assertEqual(self.stl.find_largest_two(list), (0, 7))

        list = [50, 60, 3, 7, 20, 3, 9, 30, 15, 5]
        self.assertEqual(self.stl.find_largest_two(list), (1, 0))