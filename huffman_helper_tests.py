import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_lt_and_eq01(self):
        a = HuffmanNode('a', 2)
        b = HuffmanNode('a', 1)
        c = HuffmanNode('b', 1)
        n = HuffmanNode('a', 1)
        self.assertEqual(b, n)
        self.assertTrue(n==b)
        self.assertFalse(a==n)
        self.assertFalse(c<b)
        self.assertTrue(b<c) 
        self.assertFalse(b>a)
        self.assertTrue(a>b)

    def test_get_num_chars01(self):
        self.assertEqual(get_num_chars([0]*256), 0)
        list = [0]*256
        list[97] = 9
        self.assertEqual(get_num_chars(list), 9)

    def test_write_chars_helper01(self):
        test_file = open('tested_helper.txt', 'w')
        write_chars_helper(HuffmanNode(97, 1), '', 'lala', test_file)
        test_file.close()
        err = subprocess.call("diff -wb file0.txt tested_helper.txt", shell = True)
        self.assertEqual(err, 0)

if __name__ == '__main__': 
   unittest.main()