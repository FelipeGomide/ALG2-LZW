from lzw.trie.binary_compact_trie import Trie
from lzw.static import lzw_compress

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

    new = open('reescrita.txt', mode='wb')

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
        decode_byte = c.read(8)
        teste.insert(decode_byte.b, idx)
        i += passo
        idx += 1

        decode_byte.tofile(new)

        result += chr(decode_byte.uint)

    new.close()

    print(result)
    teste.print()

    # to_search = Bits(uint=ord('f'), length=8)
    # a = teste.find(to_search.b)
    # print(a, to_search.b)

    compressed = lzw_compress()
    print(compressed)


if __name__ == '__main__':
    main()

#decompressed = lzw_decompress(compressed)