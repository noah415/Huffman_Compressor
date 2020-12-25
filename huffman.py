from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        return type(other) == HuffmanNode and\
                other.char == self.char and\
                other.freq == self.freq
        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq == other.freq:
            return self.char < other.char

        return self.freq < other.freq

def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    try:#makes sure that the file exists, if not then raise FileNotFoundError
        file_lines = open(filename, 'r')#opens file for reading
    except:
        raise FileNotFoundError

    ascii_list = [0]*256#creates a list for the frequencies of the chars in ascii values

    for line in file_lines:#traverses through the file line by line in order to count the frequencies of each ascii character
        for char in line:
            ascii_list[ord(char)] += 1#increments the index of ascii value by 1 everytime a character of that value is found
    file_lines.close()#closes the file in order to keep python from getting mad at me
    return ascii_list#returns the frequency list for further use


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    ordered_list = OrderedList()#initializes an Orderedlist for the HuffmanNodes to be put into

    initializing_orderedlist_helper(char_freq, ordered_list)#puts nodes containing frequencies and ascii values in ordered_list
    if ordered_list.size() == 0:#if the ordered_list conatains nothing, return None
        return None

    while ordered_list.size() > 1:#while loop that creates a huffman tree 
        node1 = ordered_list.pop(0)#pops lowest node
        node2 = ordered_list.pop(0)#pops next lowest node

        if node1.char > node2.char:#ensures that the char used for the new root node is the char that is lowest
            char = node2.char
        else:
            char = node1.char

        freq = node1.freq + node2.freq#makes the freq of new root node the sum of both nodes being made children

        new_root = HuffmanNode(char, freq)#creates the new root node and makes lowest node the left node and the next the right node
        new_root.left = node1
        new_root.right = node2

        ordered_list.add(new_root)#adds the new root node back into the ordered_list

    return ordered_list.pop(0)#pops the very last node in ordered list after while loop has ran (this gives the root to the complete huffman tree)


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    if node is None:
        return ['']*256

    list_of_tups = create_code_helper(node)#creates a whole new list of tups (huff code, ascii number)
    list_of_codes = ['']*256#creates the final list to be returned 

    for tup in list_of_tups:#for loop runs through the list of tups and inputs codes into the list to be returned
        list_of_codes[tup[1]] = tup[0]

    return list_of_codes#returns list of huff codes


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    header_list = []#initializes a list for ints of ascii nums and frequencies

    for i in range(len(freqs)):#for every index of the list of freqs check if index is non zero
        freq = freqs[i]
        if freq != 0:#if index value is non zero then ...
            header_list.append(str(i))#append the index (ascii value)
            header_list.append(str(freq))#append the index frequency

    return ' '.join(header_list)#return a string of the joined values of the header_list
            

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    freq_list = cnt_freq(in_file)#gets frequency list of ascii indices
    tree_root = create_huff_tree(freq_list)#gets root to huffman tree
    code_list = create_code(tree_root)#uses huffman tree to create list of huffman codes cooresponding to the ascii values
    header_string = create_header(freq_list)#creates header of the out_file for decompression
    out_comp_file_name_string = out_file[:-4]+'_compressed.txt'#creates comp file name
    out_comp = HuffmanBitWriter(out_comp_file_name_string)#calls class for writing comp file

    out_file_opened = open(out_file, 'w')#opens outfile for writing in the header

    if header_string != '':
        out_file_opened.write(header_string+'\n')#writes the header for the out_file
        out_comp.write_str(header_string+'\n')#writes header in the comp file
        out_file_opened.close()#closes the out_file
        
        write_huffman_code_out_file(in_file, out_file, code_list, out_comp)#writes all the huffmancode in the out_file
    else:
        out_file_opened.close()
        out_comp.close()


def huffman_decode(encoded_file, decode_file):
    '''Takes a input string of the encoded_file and writes the decoded text into an output text file, decode_file
    using the Huffman Tree produced by using the header information. If the encoded_file does not exist, then raise the 
    FileNotFoundError exception. if the specified output file already exists, overwrite it. Use HuffmanBitReader to read the 
    header.
    ----------
    Remember to stop reading bits when the correct amount of chars have been translated. Without this in mind, bugs 
    may occur due to padding.'''
    try:
        encoded_file = HuffmanBitReader(encoded_file)#tries to opend the encoded file
    except:
        raise FileNotFoundError#if the encoded file string does not exist then raise FileNotFoundError

    header_string = encoded_file.read_str()#creates a header string
    freq_list = parse_header(header_string)#creates a freq list
    tree_root = create_huff_tree(freq_list)#creates a huffman tree
    total_chars = get_num_chars(freq_list)#counts the total chars 

    decoded_file = open(decode_file, 'w')#opends a file to decode the encoded file into

    if tree_root is not None:#if the huffman tree is not None
        for i in range(total_chars):#for loop that iterates through each bit 
            #calls the recursive function to write each char
            write_chars_helper(tree_root, header_string, encoded_file, decoded_file)

    #closes both the encoded file and the decoded file
    encoded_file.close()
    decoded_file.close()

    


def parse_header(header_string):
    '''Takes a string input (first line of the input file) and returns a list of frequencies (same format as cnt_freqs())
    Once list of freqs is created, pass it to create_huff_tree(list_of_freqs) to recreate Huffman Tree.'''

    header_list = header_string.split()#tries to split the header string

    freq_list = [0]*256#creates freq list

    for i in range(0, len(header_list), 2):#for loop that iterates by 2 
        freq_list[int(header_list[i])] = int(header_list[i+1])#takes the 1st and 2nd index and inputs the freq into the freq list

    return freq_list#returns the freq list




# Helper Funcs -------------------------------------------------------------------------------------------------------

#decoded helper funcs

#recursive function for decoding a file that writes a char for every leaf node reached
def write_chars_helper(tree_root, header_string, encoded_file, decoded_file):
    if tree_root.left is None and tree_root.right is None:
        decoded_file.write(chr(tree_root.char))#writes correct char in the decoded_file
        #print(str(tree_root.freq))
    else:
        bit = encoded_file.read_bit()#returns true if bit is 1 and false if bit is 0
        if bit:#calls recursively to find the leaf node if bit reader returns true
            write_chars_helper(tree_root.right, header_string, encoded_file, decoded_file)
        else:#calls recursively to find the leaf node if bit reader returns false
            write_chars_helper(tree_root.left, header_string, encoded_file, decoded_file)


#for loop that gets the number of chars in a file
def get_num_chars(freq_list):
    sum = 0
    for i in range(len(freq_list)):#for loop that adds each index of the freq_list
        sum += freq_list[i]

    return sum #returns the sum of the indices of the freq_list



#encoded helper funcs


#initializes the OrderedList and fills it with HuffmanNodes to be ready for creating the 
#Huffman Tree
def initializing_orderedlist_helper(char_freq, ordered_list):
    for i in range(len(char_freq)):
        freq = char_freq[i]
        if freq != 0:
            ordered_list.add(HuffmanNode(i, freq))


#returns a list of tupils that holds (huff code, ascii number)
def create_code_helper(node, string=''):
    if node.left == None and node.right == None:
        return [(string, node.char)]

    if node.left != None and node.right != None:
        return create_code_helper(node.left, string + '0') + create_code_helper(node.right, string + '1')


#opens the in_file and out_file (for appending) and converts every character to the correct huffman code
def write_huffman_code_out_file(in_file, out_file, code_list, out_comp):
    in_file = open(in_file, 'r')#opens in_file to read
    out_file = open(out_file, 'a')#opens out_file to append
    

    for line in in_file:#finds the huffman code for each character and puts it in the out_file
        for char in line:
            if code_list is not None:
                out_file.write(code_list[ord(char)])
                out_comp.write_code(code_list[ord(char)])#writes bits for compressed file

    #closes all opened files
    in_file.close()
    out_file.close()
    out_comp.close()



