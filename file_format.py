from bitarray import *
from bitarray.util import *

def find_next_ffff_index(b):
    return b.find(bitarray('11111111111111111111'),0,len(b))

def return_bitarr_and_modify_file_bitarray(file_bitarray):
    next_ff_index = find_next_ffff_index(file_bitarray)
    b = file_bitarray[:next_ff_index]
    file_bitarray = file_bitarray[next_ff_index+16:]
    return b,file_bitarray


def file_bitarray_decompose(file_bitarray):
    rows = ba2int(file_bitarray[:16])
    cols = ba2int(file_bitarray[16:32])
    file_bitarray = file_bitarray[32:]



    size_bitarray_dc_y,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_dc_y,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    size_bitarray_dc_cb,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_dc_cb,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    size_bitarray_dc_cr,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_dc_cr,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)

    huffman_bitarray_ac_y,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_ac_y,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    huffman_bitarray_ac_cb,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_ac_cb,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    huffman_bitarray_ac_cr,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    value_bitarray_ac_cr,file_bitarray = return_bitarr_and_modify_file_bitarray(file_bitarray)
    lst = [rows,cols,size_bitarray_dc_y,value_bitarray_dc_y,size_bitarray_dc_cb,value_bitarray_dc_cb,size_bitarray_dc_cr,\
        value_bitarray_dc_cr,huffman_bitarray_ac_y,value_bitarray_ac_y,huffman_bitarray_ac_cb,value_bitarray_ac_cb,\
        huffman_bitarray_ac_cr,value_bitarray_ac_cr]
    return lst


    
