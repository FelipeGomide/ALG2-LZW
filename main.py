from lzw.static import *
from lzw.dynamic import *
from lzw.static_reset import *

import sys
import os
import time

log = 0
compress = 0
decompress = 0
dynamic_mode = False
min_dict_size = 9
max_dict_size = 12
file = "input/input.txt"

compression_time = 0
decompress_time = 0


def main():
    parse_args()
    
    global compression_time, decompress_time
    start_time = time.time()

    if dynamic_mode:
        if compress and decompress:
            out = lzw_dynamic_compress(file, max_dict_size, min_dict_size)
            compression_time = time.time() - start_time
            lzw_dynamic_decompress(out, max_dict_size, min_dict_size)
        else:
            if compress:
                lzw_dynamic_compress(file, max_dict_size, min_dict_size)
                compression_time = time.time() - start_time

            if decompress:
                lzw_dynamic_decompress(file, max_dict_size, min_dict_size)
    else:
        if compress and decompress:
            out = lzw_static_compress(file, max_dict_size)
            compression_time = time.time() - start_time
            lzw_static_decompress(out, max_dict_size)
        else:
            if compress:
                lzw_static_compress(file, max_dict_size)
                compression_time = time.time() - start_time

            if decompress:
                lzw_static_decompress(file, max_dict_size)
    
    if compression_time > 0:
        decompress_time = time.time() - compression_time - start_time
    else:
        decompress_time = time.time() - start_time

    if log:
        generate_log()

def parse_args():
    args = sys.argv

    if (len(args) < 2):
        raise "Not enough arguments!"

    global file, log
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
            case '--log' | '-l':
                log = 1
            case _:
                pass
    return


def generate_log():
    print('\033[1m' + "Configurações" + '\033[0m')
    if dynamic_mode:
        print("Modo:\t\tDinâmico")
        print(f"Tam min:\t{min_dict_size}")
        print(f"Tam max:\t{max_dict_size}")
    else:
        print("Modo:\t\tEstático")
        print(f"Tam dict:\t{max_dict_size}")
    
    if compress:
        file_stats = os.stat(f"input/{file}")
        input_size = file_stats.st_size/1024
    
        print("Input size:\t{:.2f} KB".format(input_size))

        compressed_file = os.path.splitext(file)[0] + ".ceflzw"
        file_stats = os.stat(f'compressed/{compressed_file}')
        output_size = file_stats.st_size/1025
        print("Comp Size:\t{:.2f} KB".format(output_size))

        print("Comp %:\t\t{:.2f}%".format(output_size/input_size * 100))

    if not compress and decompress:
        compressed_file = os.path.splitext(file)[0] + ".ceflzw"
        file_stats = os.stat(f'compressed/{compressed_file}')
        output_size = file_stats.st_size/1025
        print("Comp Size:\t{:.2f} KB".format(output_size))

    if compress:
        print("Comp Time:\t{:.3f}s".format(compression_time))
    if decompress:
        print("Decomp Time:\t{:.3f}s".format(decompress_time))

    log_file = open(f"logs/{os.path.splitext(file)[0]}_{dynamic_mode}_{min_dict_size}_{max_dict_size}.txt", mode="w")
    log_file.write(f"{dynamic_mode} {min_dict_size} {max_dict_size} {input_size} {output_size} {output_size/input_size * 100} {compression_time} {decompress_time}")
    log_file.close()


if __name__ == '__main__':
    main()