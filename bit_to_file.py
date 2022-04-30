from bitarray import *

def write_str_to_file_bitform(str,file):
    bitarr= bitarray(str)
    f = open(file,"wb")
    bitarr.tofile(f)


def read_from_file_bit_form(file):
    f = open(file,"rb")
    b = bitarray()
    b.fromfile(f)
    lst = b.tolist()
    str1 = ''.join(str(e) for e in lst)
    return str1


write_str_to_file_bitform("11110000","file000")

file_str = read_from_file_bit_form("file000")
print(file_str)