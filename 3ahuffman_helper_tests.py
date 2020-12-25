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

if __name__ == '__main__': 
   unittest.main()