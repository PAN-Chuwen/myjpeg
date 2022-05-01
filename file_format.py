from logging import BufferingFormatter
from bitarray import *
from bitarray.util import *



def file_bitarray_decompose(file_bitarray):
    rows = ba2int(file_bitarray[:16])
    cols = ba2int(file_bitarray[16:32])
    file_bitarray = file_bitarray[32:]


    bitarr_len_lst = []
    for i in range(12):
        bitarr_len_lst.append(file_bitarray[:32])
        file_bitarray = file_bitarray[32:]


    bitarr_lst = []
    for bcur_bitarr_len in bitarr_len_lst:
        cur_len = ba2int(bcur_bitarr_len)
        bitarr_lst.append(file_bitarray[:cur_len])
        file_bitarray = file_bitarray[cur_len:] #whats fking wrong with this line?


    return rows,cols,bitarr_len_lst,bitarr_lst


    
