from preprocess.MyTextPreProcess import MyTextPreProcess
from unittest import TestCase

class TestMyTextPreProcess(TestCase):
    def setUp(self):
        self.mt = MyTextPreProcess()

    def test_preprocess(self):
        str = "summer is a3\/^  coming. q+=, -f, .3gm. .a, .b, -wq0yv*x., ^abc a/n, a+b carry-out n-l-m a*b*c, In 1997, July, 13th, 777, &%jdlfj, 444@@@,U.S.A. pre-process. It's raining. C2H6OH Jun-3rd. don't"
        print self.mt.PreProcess(str)
        self.assertEqual(3,3)
