from trie.binary_compact_trie import Trie

from bitstring import *

import sys

def main():
    print(sys.argv, len(sys.argv))

    mydict = Trie()
    mydict.insert('010', 3)
    mydict.insert('0101', 1)
    mydict.insert('0111', 2)
    mydict.insert('0', 4)
    mydict.print()


    teste = Trie()

    c = BitStream(filename='test.txt')

    print("Arquivo codificado em string binária: ", c.bin)
    print("Tamanho: ", len(c))
    print("Bytes: ", len(c)//8)
    print("BitStream size: ", sys.getsizeof(c))
    print("Binary String size: ", sys.getsizeof(c.bin))

    i = 0
    idx = 0
    passo = 8
    result = ''
    while i < len(c):
        decode_byte = Bits(bin = c.bin[i:i+passo])
        teste.insert(decode_byte.bin, idx)
        i += passo
        idx += 1
        result += chr(decode_byte.uint)

    print(result)

    teste.print()


if __name__ == '__main__':
    main()