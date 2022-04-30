import numpy as np
from DCT_quant import *
from padding_image import *
from zigzag import *


def block_generator(padded_matrix):
    #need to do the loop in parallel later
    block = np.empty((8,8),dtype=int)
    block_index = -1
    for block_row_index in range(0,padded_matrix.shape[0],8):
        for block_col_index in range(0,padded_matrix.shape[1],8):
            block = padded_matrix[block_row_index:block_row_index+8,block_col_index:block_col_index+8]
            block_index += 1
            yield (block_row_index, block_col_index,block,block_index)


#need to change later, we need to do it in parallel
def extract_DC_AC(padded_matrix,dc,ac):
    tmp_array = np.empty(64,dtype=int)
    for (block_row_index, block_col_index, block, block_index) in block_generator(padded_matrix):
        quanted_block = quant_block(DCT_2D(block),'lum')
        tmp_array = zigzag_block_to_array(quanted_block)
        dc[block_index] = tmp_array[0]
        ac[block_index:block_index+63]=tmp_array[1:64]
        if(block_index==0): print("quanted_block:",quanted_block)

def restore_quanted_matrix_from_DC_AC(dc,ac,block_row_total, block_col_total):
    restored_matrix = np.empty((8*block_row_total,8*block_col_total),dtype=int)
    tmp_block = np.empty((8,8),dtype=int)
    for row in range(0,block_row_total):
        for col in range(0,block_col_total):
            block_index = row*block_col_total + col
            tmp_block = zigzag_array_to_block(np.concatenate((dc[block_index:block_index+1],ac[63*block_index:63*block_index+63])))
            restored_matrix[row*8:row*8+8,col*8:col*8+8] = tmp_block
    return restored_matrix



print(Y_padded)
print(Y_padded.shape)
print(Cb_padded)
print(Cr_padded)


y_block_num = int(Y_padded.size/64)
cb_block_num = int(Cb_padded.size/64)
cr_block_num = int(Cr_padded.size/64)
print(y_block_num,cb_block_num,cr_block_num)

dc_y = np.empty(y_block_num,dtype=int)
ac_y = np.empty(y_block_num*63,dtype=int)


dc_cb = np.empty(cb_block_num,dtype=int)
ac_cb = np.empty(cb_block_num*63,dtype=int)

dc_cr = np.empty(cr_block_num,dtype=int)
ac_cr = np.empty(cr_block_num*63,dtype=int)





extract_DC_AC(Y_padded,dc_y,ac_y)
extract_DC_AC(Cb_padded,dc_cb,ac_cr)
extract_DC_AC(Cr_padded,dc_cb,ac_cr)

print("dc_y",dc_y)
print("dc_y.shape",dc_y.shape)
print("ac_y",ac_y)
print("ac_y.shape",ac_y.shape)

print("dc_cb",dc_cb)
print("dc_cb.shape",dc_cb.shape)
print("ac_cb",ac_cb)
print("ac_cb.shape",ac_cb.shape)

y_restored_quant_matrix = restore_quanted_matrix_from_DC_AC(dc_y,ac_y,int(Y_padded.shape[0]/8),int(Y_padded.shape[1]/8))


print("Y_quant_restored:",y_restored_quant_matrix)





# RLE on AC

# Differential coding on DC