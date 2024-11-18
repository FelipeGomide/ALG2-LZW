from bitstring import *
from trie.binary_compact_trie import Trie

import sys

def countTotalBits(num):
     return len(bin(num)[2:])

def lzw_compress():
    print(sys.argv, len(sys.argv))

    dictionary = Trie()

    # Read binary content of the file
    c = BitStream(filename='input/casmurro.txt')
    file = open("compressed.txt", mode="wb")

    #print(len(c), len(c.b))

    """print("Arquivo codificado em string binária: ", c.bin)
    print("Tamanho: ", len(c))
    print("Bytes: ", len(c) // 8)
    print("BitStream size: ", sys.getsizeof(c))
    print("Binary String size: ", sys.getsizeof(c.bin))"""

    i = 0
    idx = 0
    n_bits = 9
    result = []  # Stores the resulting encoded string
    to_file = BitStream()
    
    max_bits_code = 9
    

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

        if countTotalBits(idx) > max_bits_code:
            # Limit exceeded: Only add the current code to the result
            print("Limite de bits excedido!")
            found, code = dictionary.find(w.b)
            if found:
                to_append = Bits(f'uint{n_bits}={code}')
                result.append(to_append.b)
                to_file.append(to_append)
            
            w = symbol
            
            # found, code_bits = dictionary.find(symbol.b)
            # if found:
            #     #result.append(code_bits)  # Append the code to the result
            #     to_append = Bits(f'uint{n_bits}={code}')
            #     to_file.append(to_append)
            #     result.append(to_append.b)

        else:
            wc = Bits(bin = w.b + symbol.b)

            found, code_bits = dictionary.find(wc.b)
            #print("Buscado:", wc.b, found , code_bits)

            if found:
                w = Bits(bin = wc.b)
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
                boolean, code = dictionary.find(w.b)
                #print(w.b, w.uint, boolean, code)
                to_append = Bits(f'uint{n_bits}={code}')

                #print("To_append", boolean, to_append)
                to_file.append(to_append)
                result.append(to_append.b)  # Append the previous match

                w = Bits(bin = symbol.b)  # Start a new sequence

        # Increment the position by step size
        i += 8
        #print(i)
        #dictionary.print()

    # Add any remaining sequence to the result
    if w:
        found, code = dictionary.find(w.b)
        if found:
            to_append = Bits(f'uint{n_bits}={code}')
            result.append(to_append.b)
            to_file.append(to_append)

    #print("Encoded Result:", result)
    #dictionary.print()
    #print(to_file.bin)
    to_file.tofile(file)
    file.close()

    return result


def lzw_decompress(compressed):
    dictionary = Trie()
    idx = 0

    c = BitStream(filename='compressed.txt')
    file = open("decompressed.txt", mode="wb")
    #print(c.bin)

    # Preenche tabela unicode
    for i in range(256):
        dictionary.insert(Bits(uint9=i).b, Bits(uint8=i).b)
        idx += 1

    #dictionary.print()
    
    i = 0
    passo = 9
    max_bits_code = 9
    n_bits = 9

    result = ""
    code = c.read(9).b 
    boolean, string = dictionary.find(code)
    
    to_append = Bits(b = string)
    to_append.tofile(file)
    
    result += string

    while True:
        try:
            code = c.read(9).b
        except:
            break
        
        #print("Lido no arquivo:" ,code)
        i += 1

        found, search = dictionary.find(code)
        #print(f"Found:{found}, Search:{search}")

        if found:
            entry = search
            
        elif code == Bits(uint9=idx).b:
            entry = string + string[:8]
            
        else:
            raise ValueError("Bad compression")
      
        #print("Entry=", f'\'{entry}\'')
        
        to_append = Bits(b = entry)
        #print("to_append:", to_append.b, len(to_append.b), i)
        to_append.tofile(file)
        result += str(entry)

        if idx <= 2**(max_bits_code)-1:
            dictionary.insert(Bits(uint9=idx).b, string+entry[:8])
        
        string = entry

        idx += 1

    #dictionary.print()
    return result

if __name__ == '__main__':
    compressed = lzw_compress()
    #print(compressed)

    # for c in compressed:
    #     number = Bits(bin = c).uint
    #     if number < 255:
    #         print(chr(number), )
    #     else: print(number)

    decompressed = lzw_decompress(compressed)
    #print(decompressed)