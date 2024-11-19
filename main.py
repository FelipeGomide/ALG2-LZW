from lzw.static import *
from lzw.dynamic import *
from lzw.static_reset import *

import sys

compress = 0
decompress = 0
dynamic_mode = False
min_dict_size = 9
max_dict_size = 12
file = "input/input.txt"

def main():
    parse_args()

    print("Configurações", "\nDynamic", dynamic_mode, "\nMin", min_dict_size)
    print("Max", max_dict_size, "\nFilename", file)
    print('Compress', compress, '\nDecompress', decompress)
    
    
    if dynamic_mode:
        if compress and decompress:
            out = lzw_dynamic_compress(file, max_dict_size, min_dict_size)
            print("Descompressão")
            lzw_dynamic_decompress(out, max_dict_size, min_dict_size)
        else:
            if compress:
                lzw_dynamic_compress(file, max_dict_size, min_dict_size)

            if decompress:
                lzw_dynamic_decompress(file, max_dict_size, min_dict_size)
    else:
        if compress and decompress:
            out = lzw_static_compress_reset(file, max_dict_size)
            print("Descompressão")
            lzw_static_decompress_reset(out, max_dict_size)
        else:
            if compress:
                lzw_static_compress(file, max_dict_size)

            if decompress:
                lzw_static_decompress(file, max_dict_size)
            

def parse_args():
    args = sys.argv
    print(args, len(args))

    if (len(args) < 2):
        raise "Not enough arguments!"

    global file
    global min_dict_size
    global max_dict_size
    global dynamic_mode
    global decompress, compress

    file = args[1]

    for i in range(len(args)):
        match args[i]:
            case '--static':
                dynamic_mode = False
            case '--dynamic':
                dynamic_mode = True
            case '--max':
                max_dict_size = int(args[i+1])
            case '--min':
                min_dict_size = int(args[i+1])
            case '--compress' | '-c':
                compress = 1
            case '--decompress' | '-d':
                decompress = 1
            case '--both' | '-b':
                decompress = 1
                compress = 1
            case _:
                pass
    
    return





if __name__ == '__main__':
    main()