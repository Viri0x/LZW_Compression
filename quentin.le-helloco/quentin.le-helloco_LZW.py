#!/usr/bin/env python
# coding: utf-8

# # LZW Compress/Uncompress Algorithm

# ### Statement:

# Implement a unique python 3 script algorithm that resolve LZW compression-decompression
# 
# Only available libraries are:
# * Pandas/csv
# * Numpy
# * Argparse
# 
# ###### ----------------------
# #### Compression
# Should be called with ```quentin.le-helloco_LZW.py -c -p path/to/file.txt```
# 
# ```-c``` is used to specified compression and ```-p``` for the path
# 
# 
# ###### Return
# The dictionnary file as a csv ```myfile_dico.csv``` with ```%``` as the reserved character.
# 
# The text file ```myfile.lzw```:
# * a string of the binary code as first line
# * the size before and after compression on second and third line
# * the compression rate as fourth line.
# 
# The table as if it was done by hand as a csv ```myfile_LZWtable.csv```
# ###### ----------------------
# ##### Uncompression
# Should be called with ```quentin.le-helloco_LZW.py -u -p path/to/file.lzw```
# 
# ```-u``` is used to specified uncompression and ```-p``` for the path
# 
# Unlike the compression file, this one will only have the first line (binary code) of the txt format.
# The dictionnary will be given in the same directory, also it should be automatically loaded with the file given in argument.
# 
# ###### Return
# The text file ```myfile2.txt``` containing the uncompressed text, to be save in the current directory of the script.
# ###### ----------------------
# ##### Utils
# For csv, the separator is ```,```.
# 
# All return files are to be written in the current directory of the script.
# 
# Particularly, the first line of csv table file should be exactly the same as the one given, as they will be tested that way
# 
# The script will be placed in a ```quentin.le-helloco/``` directory.
# The parent directory will contained ```compression/``` and ```decompression/``` each containing the .txt and .lzw file to test

# ### Import
from argparse import ArgumentParser
import numpy
import pandas as pd
import os

#---------------------
#### SIDE FUNCTIONS

# ##### Create dic from text line
def get_dic(lines):
    hist=[False] * 256
    count = 0
    length_line = len(lines)

    #Add the % reserved character
    hist[ord('%')] = True

    for l in lines:
        count+=1

        #remove the last \n
        if count == length_line:
            l = l[:-1]

        for c in l:
            index = ord(c)
            if not hist[index]:
                hist[index] = True

    dic=[]

    for i in range(256):
        if hist[i]:
            dic.append(chr(i))

    return dic


# #### Write dico as csv
def dico_to_csv(dico, filename):
    csv_name = filename + "_dico.csv"

    f = open(csv_name, "w+")
    csv = ""
    length_dico = len(dico)

    for i in range(length_dico):
        csv += dico[i]

        if i < length_dico - 1:
            csv += ","

    f.write(csv)


# #### Write the csv table
def csv_table(data, filename, first=False):
    csv_name = filename + "_LZWtable.csv"

    if first:
        f = open(csv_name, "w+")
        f.write("Buffer,Input,New sequence,Address,Output\n")
    else:
        f = open(csv_name, "a")
        f.write(data[0] + "," + data[1] + "," + data[2] + "," + data[3] + "," + data[4] + "\n")


# ##### Write the output file
def lzw_out(filename, output, create=False):
    csv_name = filename + ".lzw"

    if create:
        f = open(csv_name, "w+")
    else:
        f = open(csv_name, "a")

    f.write(output)


# ##### Conversion to bit
def index_to_bit(index, size):
    #get index as binary
    res = format(index, 'b')

    length = len(res)

    # add 0 before if needed
    for i in range(length, size):
        res = "0" + res

    return res

# ##### Load dico
def load_dico(args):
    path = args.p[:-4] + "_dico.csv"

    data = pd.read_csv(path)

    dico = []
    for d in data.columns:
        dico.append(d)

    return dico

# #### Bits to int
def bits_to_index(bits):
    #get index as decimal
    res = int(bits, 2)

    return res

# #### Create txt output file
def output_txt(filename, out):
    txt_name = filename + ".txt"

    f = open(txt_name, "w+")
    f.write(out)



# #### Utils
def add_strings(lines):
    res = ""

    for l in lines:
        res += l

    return res

def find_size(n):
    res = format(n, 'b')
    return len(res)


#---------------------
##### MAINS FUNCTIONS

# ### Compression

def compression(args, lines):
    """
    Main function for zwl compression (-c)
    """
    #final variables
    without_c = 0
    with_c = 0

    #Get filename without extention
    filename = os.path.basename(args.p)[:-4]

    #Get dico from file
    dico = get_dic(lines)
    size = find_size(len(dico) - 1)

    #Create dico csv
    dico_to_csv(dico, filename)

    #Transform all lines into one string
    input = add_strings(lines)
    length = len(input)

    #find without compression performance (minus last \n)
    without_c = length * size - size

    #Create buffer
    buffer = []
    output = ""

    #Parse all characters
    for i in range(length):
        #print(input[i])
        add_size = False
        #Initialisation Step
        if buffer == [] and input[i] in dico:
            csv_table(["", "", "", "", ""], filename, first=True)
            csv_table(["", input[0], "", "", ""], filename)

            buffer.append(input[i])
        else:
            curr_char = input[i]
            #Delete last EOF \n
            if i == length - 1:
                curr_char = ""

            #Concatene with buffer
            buffer_seq = add_strings(buffer)
            seq = buffer_seq + curr_char
            nw_id = ""

            #Search if seq in dico
            if not seq in dico:
                #Add seq to dico, add binary address to output, pop previous buffer
                dico.append(seq)
                nw_id =  index_to_bit(dico.index(buffer_seq), size)
                with_c += size
                output += nw_id
                buffer = []

                out = "@[%s]=%d" % (buffer_seq, dico.index(buffer_seq))
                idx = str(dico.index(seq))
            else:
                out = ""
                seq = ""
                idx = ""

                #Delete last EOF \n
                if i == length - 1:
                    out = "@[%s]=%d" % (buffer_seq, dico.index(buffer_seq))
                    output += index_to_bit(dico.index(buffer_seq), size)
                    with_c += size
                else:
                    #Check if we need to increase size of bit
                    #NEED TO BE A LOOP AND NOT UPDATING BUFFER BEFORE
                    while find_size(dico.index(add_strings(buffer) + curr_char)) > size:
                        #print(find_size(dico.index(add_strings(buffer) + curr_char)), " ", size)
                        add_size = True
                        out = "@[%s]=%d" % ("%", dico.index("%"))
                        csv_table([buffer_seq, curr_char, seq, idx, out], filename)
                        output+= index_to_bit(dico.index("%"), size)
                        with_c += size
                        size += 1

            #Add to buffer
            buffer.append(curr_char)

            if not add_size:
                csv_table([buffer_seq, curr_char, seq, idx, out], filename)

    lzw_out(filename, output + "\n", create=True)
    without_line = "Size before LZW compression: " + str(without_c) + " bits\n"
    lzw_out(filename, without_line)
    with_line = "Size after LZW compression: " + str(with_c) + " bits\n"
    lzw_out(filename, with_line)
    rate = with_c / without_c
    rate_line = "Compression ratio: " + "{:.3f}".format(rate)
    lzw_out(filename, rate_line)



# ### UNCOMPRESSION
def uncompression(args, lines):

    #Get dico from csv:
    dico = load_dico(args)

    #Initialize variables
    filename = os.path.basename(args.p)[:-4]
    buffer = []
    output = ""
    size = find_size(len(dico) - 1)
    index = 0

    #Transform all lines into one string
    input = add_strings(lines)
    length = len(input)

    while index < length:
        bin = ""

        #Get size number of bits
        for s in range(size):
            bin += input[index]
            index+=1

        #Convert to decimal address in dico
        add = bits_to_index(bin)
        #print(bin, "", add)

        #Check if address is not special character %
        if dico[add] == "%":
            size+=1
        else:
            buff_seq = add_strings(buffer)
            seq = buff_seq + (dico[add])[0]
            if not seq in dico:
                dico.append(seq)

            output+= buff_seq

            buffer = []
            buffer.append(dico[add])

    buff_seq = add_strings(buffer)
    output+= buff_seq

    output_txt(filename, output)
    return output


# ### Parsing Arguments

if __name__ == "__main__":
    parser = ArgumentParser(description="LWZ Un/Compressor")

    parser.add_argument("-p",                         help="Path to the file to load",                        action="store")

    parser.add_argument("-c",                         help="Activate compression features",                        action="store_true")

    parser.add_argument("-u",                         help="Activate uncompression features",                        action="store_true")

    #args = parser.parse_args("-c -p ../décompression/toto.lzw".split())
    args = parser.parse_args()

    # ### Read file
    if (not args.p):
        print("No path")
    else:
        f = open(args.p, "r")
        lines = f.readlines()

    if (args.c):
        print("compression on file ", args.p)
        compression(args, lines)
    elif (args.u):
        print("uncompression on file ", args.p)
        uncompression(args, lines)
    else:
        print("no args")




