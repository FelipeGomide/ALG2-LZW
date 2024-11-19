from bitstring import *
from .trie.binary_compact_trie import Trie

import sys
import os

def countTotalBits(num):
     return len(bin(num)[2:])

#@profile
def lzw_static_compress(input_file, max_dict_size):

    dictionary = Trie()

    compressed_file = os.path.splitext(input_file)[0] + ".ceflzw"

    # Read binary content of the file
    c = BitStream(filename=f'input/{input_file}')
    file = open(f"compressed/{compressed_file}", mode="wb")

    i = 0
    idx = 0

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
            # Insiro na Trie
            if countTotalBits(idx) <= max_dict_size:    
                dictionary.insert(wc.b, idx)
                idx += 1

            _, code = dictionary.find(w.b)
            
            # Insiro no arquivo
            to_append = Bits(f'uint{max_dict_size}={code}')
            to_file.append(to_append)

            w = symbol  # Inicio nova sequência

        # Increment the position by step size
        i += 8

    # Adiciono que sobrar ao arquivo
    if w:
        found, code = dictionary.find(w.b)
        if found:
            to_append = Bits(f'uint{max_dict_size}={code}')
            to_file.append(to_append)

    to_file.tofile(file)
    file.close()

    return compressed_file

#@profile
def lzw_static_decompress(compressed_file, max_dict_size):
    dictionary = Trie()
    idx = 0

    out_file = os.path.splitext(compressed_file)[0] + ".txt"
    c = BitStream(filename=f'compressed/{compressed_file}')
    file = open(f"decompressed/{out_file}", mode="wb")

    # Preenche tabela unicode
    for i in range(256):
        dictionary.insert(Bits(f'uint{max_dict_size}={i}').b, Bits(uint8=i).b)
        idx += 1

    result = ""
    code = c.read(max_dict_size).b 
    boolean, string = dictionary.find(code)
    
    to_append = Bits(b = string)
    to_append.tofile(file)
    
    result += string
    i = 0
    while True:
        try:
            code = c.read(max_dict_size).b
        except:
            break
        
        i+=1
        # if countTotalBits(idx) > max_dict_size:
        #     print("Limite de bits excedido!", i)
        #     new_dict = Trie()
        #     dictionary =  new_dict
        #     idx = 0

        #     for j in range(256):
        #         dictionary.insert(Bits(f'uint{max_dict_size}={j}').b, Bits(uint8=j).b)
        #         idx += 1

        found, search = dictionary.find(code)
        #print(f"Found:{found}, Search:{search}")

        if found:
            entry = search
            
        elif code == Bits(f"uint{max_dict_size}={idx}").b:
            entry = string + string[:8]
            
        else:
            print(f"{code}, {idx}, {Bits(f'uint{max_dict_size}={idx}').b}")
            raise ValueError("Bad compression")
      
        #print("Entry=", f'\'{entry}\'')
        
        to_append = Bits(b = entry)
        #print("to_append:", to_append.b, len(to_append.b), i)
        to_append.tofile(file)
        result += str(entry)

        if countTotalBits(idx) <= max_dict_size:
            dictionary.insert(Bits(f"uint{max_dict_size}={idx}").b, string+entry[:8])
            idx += 1
        
        string = entry


    #dictionary.print()
    return result

if __name__ == '__main__':
    print("Módulo apenas de import executado como código")