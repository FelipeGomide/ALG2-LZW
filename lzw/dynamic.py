from bitstring import *
from .trie.binary_compact_trie import Trie

import sys
import os
from math import log, floor

def countTotalBits(num):
    return len(bin(num)[2:])

@profile
def lzw_dynamic_compress(input_file, max_dict_size, min_dict_size):
    dictionary = Trie()

    compressed_file = os.path.splitext(input_file)[0] + ".ceflzw"

    # Read binary content of the file
    c = BitStream(filename=f'input/{input_file}')
    file = open(f"compressed/{compressed_file}", mode="wb")

    i = 0
    idx = 0
    n_bits = min_dict_size

    to_file = BitStream()

    # Preenche tabela unicode
    for j in range(256):
        dictionary.insert(Bits(uint8=j).b, idx)
        idx += 1
    
    w = c.read(8)
    i += 8

    while i < len(c):
        # Read the next byte (8 bits) as a binary string
        symbol = c.read(8)

        wc = Bits(bin = w.b + symbol.b)

        found, code_bits = dictionary.find(wc.b)

        if found:
            w = wc

        else:
            # Insert the new sequence in the Trie
            if countTotalBits(idx) <= max_dict_size:
                dictionary.insert(wc.b, idx)
                idx += 1

            _, code = dictionary.find(w.b)
                
            to_append = Bits(f'uint{n_bits}={code}')
            #print("to_append", i//8,  to_append.bin)
            to_file.append(to_append)

            # if countTotalBits(idx) > max_dict_size:
            #     # Limit exceeded: Only add the current code to the result
            #     print("Limite de bits excedido!", i//8)
            #     new_dict = Trie()
            #     dictionary = new_dict
            #     idx = 0
            #     n_bits = min_dict_size

            #     for j in range(256):
            #         dictionary.insert(Bits(uint8=j).b, idx)
            #         idx += 1

            #n_bits = countTotalBits(idx)
            w = symbol  # Start a new sequence

        # Increment the position by step size
        i += 8
        n_bits = countTotalBits(idx)
    

    # Add any remaining sequence to the result
    if w:
        found, code = dictionary.find(w.b)
        if found:
            to_append = Bits(f'uint{n_bits}={code}')
            to_file.append(to_append)

    to_file.tofile(file)
    file.close()

    return compressed_file

@profile
def lzw_dynamic_decompress(compressed_file, max_dict_size, min_dict_size):
    dictionary = Trie()
    idx = 0
    n_bits = min_dict_size

    out_file = os.path.splitext(compressed_file)[0] + ".txt"
    c = BitStream(filename=f'compressed/{compressed_file}')
    file = open(f"decompressed/{out_file}", mode="wb")

    # Preenche tabela unicode
    for i in range(256):
        dictionary.insert(Bits(f'uint{max_dict_size}={i}').b, Bits(uint8=i).b)
        idx += 1

    n_bits = countTotalBits(idx)

    result = ""
    code = c.read(n_bits)
    code = Bits(f'uint{max_dict_size}={code.uint}').b

    boolean, string = dictionary.find(code)
    
    to_append = Bits(b = string)
    to_append.tofile(file)
    
    result += string
    i= 0 

    while c.pos + n_bits < len(c):
        n_bits = countTotalBits(idx+1)
        code = c.read(n_bits)
        code = Bits(f'uint{max_dict_size}={code.uint}').b

        i += 1
        found, search = dictionary.find(code)

        if found:
            entry = search
            
        elif code == Bits(f"uint{max_dict_size}={idx}").b:
            entry = string + string[:8]
            
        else:
            print(f"{code}, {Bits(bin = code).uint},{idx}, {Bits(f'uint{max_dict_size}={idx}').b}")
            raise ValueError("Bad compression")
      
        
        to_append = Bits(b = entry)
        to_append.tofile(file)
        #result += str(entry)

        if countTotalBits(idx) <= max_dict_size:
            dictionary.insert(Bits(f"uint{max_dict_size}={idx}").b, string+entry[:8])
            idx += 1

        string = entry
        

        n_bits = countTotalBits(idx)

        # if countTotalBits(idx+1) > max_dict_size:
        #     print("Limite de bits excedido!", i)
        #     new_dict = Trie()
        #     dictionary =  new_dict
        #     idx = 0
        #     n_bits = min_dict_size

        #     for j in range(256):
        #         dictionary.insert(Bits(f'uint{max_dict_size}={j}').b, Bits(uint8=j).b)
        #         idx += 1


        
        


    #dictionary.print()
    return result

if __name__ == '__main__':
    print("Módulo apenas de import executado como código")