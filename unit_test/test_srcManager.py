from utils.SrcManager import SrcManager
from unittest import TestCase
import os
import shutil

class TestSrcManager(TestCase):

    def setUp(self):
        self.sm = SrcManager()

    def test_src_to_one_dir(self):
        src = 'test_data/src_d'
        self.sm.src_to_one_dir(src, 'test_src')
        self.assertTrue(os.path.exists('test_src'))
