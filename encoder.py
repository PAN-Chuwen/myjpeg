import argparse
from bitarray import bitarray
from bitarray.util import ba2int
import numpy as np
from PIL import Image
from DC_AC_extract import dct_quant_and_extract_DC_AC_from_padded_matrix
from entropy_encoding import DPCM, RLE, decompose_RLE_list_to_huffmanResBitarray_valueBitarray, encode_DC_entropy_all,decode_DC_entropy_all

from padding_image import *

def main():
    #usage: python3 encoder.py input_file output_file
    parser = argparse.ArgumentParser()
    parser.add_argument("image_to_compress", help="path to the input image")
    parser.add_argument("compressed_file", help="path to the output compressed file")
    args = parser.parse_args()
    input_image_path = args.image_to_compress
    output_image_path = args.compressed_file
    image_to_compress = Image.open(input_image_path)
    
    #image RGB -> YCbCr, -128 to center around 0
    ycbcr = image_to_compress.convert('YCbCr')
    npmat = np.array(ycbcr, dtype=int)-128
    rows,cols = npmat.shape[0],npmat.shape[1]
    
    #subsampling(4:2:0) + padding 
    y = npmat[:,:,0]
    Y_padded = matrix_padding(y)
    Cb = npmat[::2,::2,1]
    Cb_padded = matrix_padding(Cb)

    Cr = npmat[::2,::2,2]
    Cr_padded = matrix_padding(Cr)
    #DCT + quant + dc/ac extract
    
    dc_y,ac_arrays_y = dct_quant_and_extract_DC_AC_from_padded_matrix(Y_padded)
    dc_cb,ac_arrays_cb = dct_quant_and_extract_DC_AC_from_padded_matrix(Cb_padded)
    dc_cr,ac_arrays_cr = dct_quant_and_extract_DC_AC_from_padded_matrix(Cr_padded)
    #dpcm + entropy for dc
    dpcm_y = DPCM(dc_y)
    dpcm_cb = DPCM(dc_cb)
    dpcm_cr = DPCM(dc_cr)



    size_bitarray_dc_y, value_bitarray_dc_y = encode_DC_entropy_all(dpcm_y)
    size_bitarray_dc_cb, value_bitarray_dc_cb = encode_DC_entropy_all(dpcm_cb)
    size_bitarray_dc_cr, value_bitarray_dc_cr = encode_DC_entropy_all(dpcm_cr)
    #perform RLE + entropy for every AC array(number equaling total number of 8x8 blocks),then concat those bitarray together
    huffman_res_bitarray_ac_y = bitarray()
    value_res_bitarray_ac_y = bitarray()
    for ac_y in ac_arrays_y:
        tmp_RLE_res = RLE(ac_y)
        huffman_tmp_bitarray_ac_y, value_tmp_bitarray_ac_y = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
        huffman_res_bitarray_ac_y += huffman_tmp_bitarray_ac_y
        value_res_bitarray_ac_y += value_tmp_bitarray_ac_y
     #repeat for AC coefficients of cb,cr
    huffman_res_bitarray_ac_cb = bitarray()
    value_res_bitarray_ac_cb = bitarray()
    for ac_cb in ac_arrays_cb:
        tmp_RLE_res = RLE(ac_cb)
        huffman_tmp_bitarray_ac_cb, value_tmp_bitarray_ac_cb = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
        huffman_res_bitarray_ac_cb += huffman_tmp_bitarray_ac_cb
        value_res_bitarray_ac_cb += value_tmp_bitarray_ac_cb
    
    huffman_res_bitarray_ac_cr = bitarray()
    value_res_bitarray_ac_cr = bitarray()
    for ac_cr in ac_arrays_cr:
        tmp_RLE_res = RLE(ac_cr)
        huffman_tmp_bitarray_ac_cr, value_tmp_bitarray_ac_cr = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
        huffman_res_bitarray_ac_cr += huffman_tmp_bitarray_ac_cr
        value_res_bitarray_ac_cr += value_tmp_bitarray_ac_cr


    #create and write to compressed file
    #use 32bit to store each length of bitarray AT THE BEGINNING right after rows_barr AND cols_barr
    with open(output_image_path, 'wb') as outFile:
        bitarraylst = [
            size_bitarray_dc_y,value_bitarray_dc_y,\
            size_bitarray_dc_cb,value_bitarray_dc_cb,\
            size_bitarray_dc_cr,value_bitarray_dc_cr,\
            huffman_res_bitarray_ac_y,value_res_bitarray_ac_y,\
            huffman_res_bitarray_ac_cb,value_res_bitarray_ac_cb,\
            huffman_res_bitarray_ac_cr,value_res_bitarray_ac_cr]
        
        # bitarr_len_list = []
        write_bitarray = bitarray()
        rows_barr = bitarray(format(rows, '#018b')[2:])
        cols_barr = bitarray(format(cols, '#018b')[2:])
        write_bitarray+=rows_barr
        write_bitarray+=cols_barr
        for barr in bitarraylst:
            cur_bit_len_barr = bitarray(format(len(barr), '#034b')[2:])
            write_bitarray+=cur_bit_len_barr
            
             #store length of this bitarray as xx xx xx xx form

        for barr in bitarraylst:
            write_bitarray+=barr

        write_bitarray.tofile(outFile)


    



    

    

if __name__ == "__main__":
    main()