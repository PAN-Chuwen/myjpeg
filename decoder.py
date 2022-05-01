import argparse
from bitarray import bitarray
from bitarray.util import *
import numpy as np
from PIL import Image
from DC_AC_extract import *
from entropy_encoding import *
from file_format import *
import math

#usage: python3 decoder.py compressed_file image_restored.png
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_to_decompress", help="file path for decompression")
    parser.add_argument("image_restored", help="restored image name")
    args = parser.parse_args()
    file_path_to_decompress = args.file_to_decompress
    image_restored_path = args.image_restored
    #read file, extract information
    file_to_decompress = open(file_path_to_decompress,"rb")
    file_bitarray = bitarray()
    file_bitarray.fromfile(file_to_decompress)
    rows,cols,bitarr_len_lst,bitarr_lst = file_bitarray_decompose(file_bitarray)
    

    

    size_bitarray_dc_y,value_bitarray_dc_y,\
    size_bitarray_dc_cb,value_bitarray_dc_cb,\
    size_bitarray_dc_cr,value_bitarray_dc_cr,\
    huffman_bitarray_ac_y,value_bitarray_ac_y,\
    huffman_bitarray_ac_cb,value_bitarray_ac_cb,\
    huffman_bitarray_ac_cr,value_bitarray_ac_cr = bitarr_lst
    
    for bar in bitarr_lst:
        bitarray_len = len(bar)


    dpcm_y_restored = decode_DC_entropy_all(size_bitarray_dc_y,value_bitarray_dc_y)
    dpcm_cb_restored = decode_DC_entropy_all(size_bitarray_dc_cb,value_bitarray_dc_cb)
    dpcm_cr_restored = decode_DC_entropy_all(size_bitarray_dc_cr,value_bitarray_dc_cr)
    dc_y_restored = DPCM_decode(dpcm_y_restored)
    dc_cb_restored = DPCM_decode(dpcm_cb_restored)
    dc_cr_restored = DPCM_decode(dpcm_cr_restored)

    
    

    all_block_RLE_lists_y = All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(huffman_bitarray_ac_y,value_bitarray_ac_y)
    all_block_RLE_lists_cb = All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(huffman_bitarray_ac_cb,value_bitarray_ac_cb)
    all_block_RLE_lists_cr = All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(huffman_bitarray_ac_cr,value_bitarray_ac_cr)
    #calculate y,cb,cr 8x8 block index from ogirinal rows and cols
    block_rows_y,block_cols_y = math.ceil(rows/8),math.ceil(cols/8) 
    block_rows_cb,block_cols_cb = block_rows_cr,block_cols_cr = math.ceil(rows/2/8),math.ceil(cols/2/8)
    block_total_y = block_rows_y * block_cols_y
    block_total_cb = block_total_cr = block_rows_cb * block_cols_cb
    
    ac_arrays_y_restored = np.empty((block_total_y,63),dtype=int)
    ac_arrays_cb_restored = np.empty((block_total_cb,63),dtype=int)
    ac_arrays_cr_restored = np.empty((block_total_y,63),dtype=int)


    block_index = 0
    for rle in all_block_RLE_lists_y:
        cur_ac_array_y = RLE_decode(rle)
        ac_arrays_y_restored[block_index] = cur_ac_array_y
        block_index += 1

    block_index = 0
    for rle in all_block_RLE_lists_cb:
        cur_ac_array_cb = RLE_decode(rle)
        ac_arrays_cb_restored[block_index] = cur_ac_array_cb
        block_index += 1
    
    block_index = 0
    for rle in all_block_RLE_lists_cr:
        cur_ac_array_cr = RLE_decode(rle)
        ac_arrays_cr_restored[block_index] = cur_ac_array_cr
        block_index += 1
   
    padded_matrix_restored_y = restore_padded_matrix_from_DC_AC(dc_y_restored,ac_arrays_y_restored,block_rows_y,block_cols_y,'lum')
    padded_matrix_restored_cb = restore_padded_matrix_from_DC_AC(dc_cb_restored,ac_arrays_cb_restored,block_rows_cb,block_cols_cb,'chrom')
    padded_matrix_restored_cr = restore_padded_matrix_from_DC_AC(dc_cr_restored,ac_arrays_cr_restored,block_rows_cr,block_cols_cr,'chrom')

    npmat_restored = restore_img_from_padding(padded_matrix_restored_y,padded_matrix_restored_cb,padded_matrix_restored_cr,rows,cols)+128
    image = Image.fromarray(npmat_restored, 'YCbCr')
    image = image.convert('RGB')
    image.save(image_restored_path)
if __name__ == "__main__":
    main()