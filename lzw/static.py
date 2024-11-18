from bitstring import *
from .trie.binary_compact_trie import Trie

import sys
import os

def countTotalBits(num):
     return len(bin(num)[2:])

def lzw_static_compress(input_file, max_dict_size):
    print(sys.argv, len(sys.argv))

    dictionary = Trie()

    compressed_file = os.path.splitext(input_file)[0] + ".ceflzw"

    # Read binary content of the file
    c = BitStream(filename=f'input/{input_file}')
    file = open(f"compressed/{compressed_file}", mode="wb")

    # """print("Arquivo codificado em string binária: ", c.bin)
    # print("Tamanho: ", len(c))
    # print("Bytes: ", len(c) // 8)
    # print("BitStream size: ", sys.getsizeof(c))
    # print("Binary String size: ", sys.getsizeof(c.bin))"""

    i = 0
    idx = 0
    #n_bits = 9

    #result = []  # Stores the resulting encoded string
    to_file = BitStream()
    
    #max_bits_code = 9
    

    # Preenche tabela unicode
    for j in range(256):
        dictionary.insert(Bits(uint8=j).b, idx)
        idx += 1
    
    #print(c.b)
    w = c.read(8)
    i += 8

    while i < len(c):
        # Read the next byte (8 bits) as a binary string
        symbol = c.read(8)
        #print(f"{i//8} iteração. Lido: {symbol.b}, Number: {symbol.uint}, {chr(symbol.uint)}")

        #print("Decode_byte", decode_byte, chr(decode_byte.uint))
        #print("--> " + decode_byte)

        if countTotalBits(idx) > max_dict_size:
            # Limit exceeded: Only add the current code to the result
            print("Limite de bits excedido!")
            found, code = dictionary.find(w.b)
            if found:
                to_append = Bits(f'uint{max_dict_size}={code}')
                #result.append(to_append.b)
                to_file.append(to_append)
            
            w = symbol

        else:
            wc = Bits(bin = w.b + symbol.b)

            found, code_bits = dictionary.find(wc.b)
            #print("Buscado:", wc.b, found , code_bits)

            if found:
                w = wc
                #print("match!")
                #result.append(code_bits)

                # to_append = Bits(f'uint{n_bits}={code_bits}')
                # result.append(to_append.b)
                # to_file.append(to_append)


            else:
                # Insert the new sequence in the Trie
                dictionary.insert(wc.b, idx)
                idx += 1
                # to_append = Bits(f'uint{n_bits}={w.uint}')

                _, code = dictionary.find(w.b)
                
                to_append = Bits(f'uint{max_dict_size}={code}')
                to_file.append(to_append)
                #result.append(to_append.b)  # Append the previous match

                w = symbol  # Start a new sequence

        # Increment the position by step size
        i += 8

    # Add any remaining sequence to the result
    if w:
        found, code = dictionary.find(w.b)
        if found:
            to_append = Bits(f'uint{max_dict_size}={code}')
            #result.append(to_append.b)
            to_file.append(to_append)

    to_file.tofile(file)
    file.close()

    return compressed_file


def lzw_static_decompress(compressed_file, max_dict_size):
    dictionary = Trie()
    idx = 0

    out_file = os.path.splitext(compressed_file)[0] + ".txt"


    c = BitStream(filename=f'compressed/{compressed_file}')
    file = open(f"decompressed/{out_file}", mode="wb")
    #print(c.bin)

    # Preenche tabela unicode
    for i in range(256):
        dictionary.insert(Bits(f'uint{max_dict_size}={i}').b, Bits(uint8=i).b)
        idx += 1

    #dictionary.print()
    
    i = 0
    #passo = 9
    #max_bits_code = 9
    #n_bits = 9

    result = ""
    code = c.read(max_dict_size).b 
    boolean, string = dictionary.find(code)
    
    to_append = Bits(b = string)
    to_append.tofile(file)
    
    result += string

    while True:
        try:
            code = c.read(max_dict_size).b
        except:
            break
        
        #print("Lido no arquivo:" ,code)
        i += 1

        found, search = dictionary.find(code)
        #print(f"Found:{found}, Search:{search}")

        if found:
            entry = search
            
        elif code == Bits(f"uint{max_dict_size}={idx}").b:
            entry = string + string[:8]
            
        else:
            raise ValueError("Bad compression")
      
        #print("Entry=", f'\'{entry}\'')
        
        to_append = Bits(b = entry)
        #print("to_append:", to_append.b, len(to_append.b), i)
        to_append.tofile(file)
        result += str(entry)

        if idx <= 2**(max_dict_size)-1:
            dictionary.insert(Bits(f"uint{max_dict_size}={idx}").b, string+entry[:8])
        
        string = entry

        idx += 1

    #dictionary.print()
    return result

if __name__ == '__main__':
    print("Módulo apenas de import executado como código")