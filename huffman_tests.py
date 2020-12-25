import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
#huffman decoding tests

    def test_parse_header01(self):
        bit_reader = HuffmanBitReader('file2_out_compressed.txt')
        header_string = bit_reader.read_str()
        self.assertEqual(header_string, '97 2 98 4 99 8 100 16 102 2\n')
        list_freqs = parse_header(header_string)
        self.assertEqual(list_freqs[97], 2)
        self.assertEqual(list_freqs[98], 4)
        self.assertEqual(list_freqs[99], 8)
        self.assertEqual(list_freqs[100], 16)
        self.assertEqual(list_freqs[102], 2)
        correct_list = [0]*256
        correct_list[97] = 2
        correct_list[98] = 4
        correct_list[99] = 8
        correct_list[100] = 16
        correct_list[102] = 2
        self.assertEqual(list_freqs, correct_list)
        bit_reader.close()

    def test_parse_header02(self):
        bit_reader = HuffmanBitReader('empty_file.txt')
        header_string = bit_reader.read_str()
        self.assertEqual(header_string, '')
        bit_reader.close()

    def test_huffman_decode01(self):
        huffman_decode('empty_file_out_compressed.txt', 'empty_file_decompressed.txt')
        err = subprocess.call("diff -wb empty_file.txt empty_file_decompressed.txt", shell = True)
        self.assertEqual(err, 0)

    def test_huffman_decode02(self):
        huffman_decode('file2_out_compressed.txt', 'file2_decompressed.txt')
        err = subprocess.call("diff -wb file2.txt file2_decompressed.txt", shell = True)
        self.assertEqual(err, 0)

    def test_huffman_decode03(self):
        huffman_decode('file0_out_compressed.txt', 'file0_decompressed.txt')
        err = subprocess.call("diff -wb file0.txt file0_decompressed.txt", shell = True)
        self.assertEqual(err, 0)

    def test_huffman_decode04(self):
        huffman_decode('declaration_out_compressed.txt', 'declaration_decompressed.txt')
        err = subprocess.call("diff -wb declaration.txt declaration_decompressed.txt", shell = True)
        self.assertEqual(err, 0)

    def test_huffman_decode05(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode('hahahhahah.txt', 'lalaland.txt')

#copied tests from decode tests
    def test_01a_test_file1_parse_header(self):
        f = open('file1_compressed_soln.txt', 'rb')
        header = f.readline()        
        f.close()
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.compare_freq_counts(parse_header(header), expected)
        
    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell = True)
        self.assertEqual(err, 0)

    def compare_freq_counts(self, freq, exp):
        for i in range(256):
            stu = 'Frequency for ASCII ' + str(i) + ': ' + str(freq[i])
            ins = 'Frequency for ASCII ' + str(i) + ': ' + str(exp[i])
            self.assertEqual(stu, ins)

#huffman encoding tests

    def test_cnt_freq00(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    def test_cnt_freq01(self):
        with self.assertRaises(FileNotFoundError):
            cnt_freq('something.tre')

        
    def test_lt_and_eq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)
                    
              
    def test_create_huff_tree01(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_huff_tree02(self):
        freqlist = [0]*256
        freqlist[97] = 1
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 1)
        self.assertEqual(hufftree.char, 97)
        self.assertEqual(hufftree.left, None)
        self.assertEqual(hufftree.right, None)

    def test_create_huff_tree03(self):
        freqlist = [0]*256
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree, None)

        
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")


    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_create_code02(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        


    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_02_textfile(self):
        huffman_encode("file2.txt", "file2_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_03_textfile(self):
        huffman_encode("multiline.txt", "multiline_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb multiline_out.txt multiline_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb multiline_out_compressed.txt multiline_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_04_textfile(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)

#test for empty files and 1 character files

    def test_05_textfile(self):
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb empty_file_out.txt empty_file.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb empty_file_out_compressed.txt empty_file.txt", shell = True)
        self.assertEqual(err, 0)

    def test_06_textfile(self):
        huffman_encode("file0.txt", "file0_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file0_out.txt file0_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file0_out_compressed.txt file0_out.txt", shell = True)
        self.assertEqual(err, 0)

#test for when file DNE

    def test_07_textfile(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode('somethingelse.txt', 'something.txt')


if __name__ == '__main__': 
   unittest.main()