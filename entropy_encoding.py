import numpy as np
from bitstring import BitArray
from DC_AC_extract import *
from bitarray import *
import sys
# np.set_printoptions(threshold=sys.maximize())

#this part is damn hard
#from https://www.globalspec.com/reference/39556/203279/appendix-b-huffman-tables-for-the-dc-and-ac-coefficients-of-the-jpeg-baseline-encoder
huffman_table_DC = {
    '0':bitarray('00'),
    '1':bitarray('010'),
    '2':bitarray('011'),
    '3':bitarray('100'),
    '4':bitarray('101'),
    '5':bitarray('110'),
    '6':bitarray('1110'),
    '7':bitarray('11110'),
    '8':bitarray('111110'),
    '9':bitarray('1111110'),
    'a':bitarray('11111110'),
    'b':bitarray('111111110')
}

huffman_table_AC = {
    (0,0):bitarray('1010'),
    (0,1):bitarray('00'),
    (0,2):bitarray('01'),
    (0,3):bitarray('100'),
    (0,4):bitarray('1011'),
    (0,5):bitarray('1011'),
    (0,6):bitarray('1011'),
    (0,7):bitarray('1011'),
    (0,8):bitarray('1011'),
    (0,9):bitarray('1011'),
    (0,10):bitarray('1011')

    (1,1):bitarray('00'),
    (1,2):bitarray('01'),
    (1,3):bitarray('100'),
    (1,4):bitarray('1011'),
    (1,5):bitarray('1011'),
    (1,6):bitarray('1011'),
    (1,7):bitarray('1011'),
    (1,8):bitarray('1011'),
    (1,9):bitarray('1011'),
    (1,10):bitarray('1011'),

    (2,1):bitarray('00'),
    (2,2):bitarray('01'),
    (2,3):bitarray('100'),
    (2,4):bitarray('1011'),
    (2,5):bitarray('1011'),
    (2,6):bitarray('1011'),
    (2,7):bitarray('1011'),
    (2,8):bitarray('1011'),
    (2,9):bitarray('1011'),
    (2,10):bitarray('1011'),

    (3,1):bitarray('00'),
    (3,2):bitarray('01'),
    (3,3):bitarray('100'),
    (3,4):bitarray('1011'),
    (3,5):bitarray('1011'),
    (3,6):bitarray('1011'),
    (3,7):bitarray('1011'),
    (3,8):bitarray('1011'),
    (3,9):bitarray('1011'),
    (3,10):bitarray('1011'),

    (4,1):bitarray('00'),
    (4,2):bitarray('01'),
    (4,3):bitarray('100'),
    (4,4):bitarray('1011'),
    (4,5):bitarray('1011'),
    (4,6):bitarray('1011'),
    (4,7):bitarray('1011'),
    (4,8):bitarray('1011'),
    (4,9):bitarray('1011'),
    (4,10):bitarray('1011'),

    (5,1):bitarray('00'),
    (5,2):bitarray('01'),
    (5,3):bitarray('100'),
    (5,4):bitarray('1011'),
    (5,5):bitarray('1011'),
    (5,6):bitarray('1011'),
    (5,7):bitarray('1011'),
    (5,8):bitarray('1011'),
    (5,9):bitarray('1011'),
    (5,10):bitarray('1011'),

    (6,1):bitarray('00'),
    (6,2):bitarray('01'),
    (6,3):bitarray('100'),
    (6,4):bitarray('1011'),
    (6,5):bitarray('1011'),
    (6,6):bitarray('1011'),
    (6,7):bitarray('1011'),
    (6,8):bitarray('1011'),
    (6,9):bitarray('1011'),
    (6,10):bitarray('1011'),


}
#n>=1
def create_nested_list(n):
    lst = [None,None]
    #don't use recursion, some lists are calculated repeatedly
    while(n>1):
        lst = [lst,lst]
        n = n - 1 
    return lst

#would not work, if we modify node,huffman_tree would NOT be modified
def construct_huffman_tree_from_huffman_dict(huffman_dict):
    n = len('1111111111000110') #one of the longests 
    huffman_tree = create_nested_list(n) #yes, we make huffmantree a nested list
    for(tupp,bit_array) in huffman_dict.items():
        node = huffman_tree
        for index in bit_array:
            node = node[index]
        node = tupp
    return


#not the pythonic way of writing this, but at least it works
def DPCM(dc):
    dpcm_arr = np.empty(dc.shape,dtype=dc.dtype)
    dpcm_arr[0] = dc[0]
    for i in range(1,dc.shape[0]):
        dpcm_arr[i] = dc[i]-dc[i-1]
    return dpcm_arr

def DPCM_decode(dpcm_arr):
    dc_restored = np.empty(dpcm_arr.shape,dtype=dpcm_arr.dtype)
    dc_restored[0] = dpcm_arr[0]
    for i in range(1,dpcm_arr.shape[0]):
        dc_restored[i] = dpcm_arr[i] + dc_restored[i-1]
    return dc_restored

#bitarray sux, cant even flip itself
def flip_bitarray(barr):
    converted_str = barr.to01()
    flipped_str = ''
    for i in converted_str:
        if (i=='0'): flipped_str+='1'
        else: flipped_str+='0'
    return bitarray(flipped_str)

def decompose_int_to_size_value(n):
    size = len(bin(abs(n)))-2
    flag = np.sign(n)
    abs_bitarray = bitarray(bin(abs(n))[2:])
    if(flag == -1): value_bitarray = flip_bitarray(abs_bitarray)
    else: value_bitarray = abs_bitarray
    return (size,value_bitarray)

#value_bitarray changes every time this function's called
def compose_size_value_to_int(size,value_bitarray):
    if(value_bitarray[0]==1): flag = 1  #positive
    else:                     flag = -1 #negative
    if(flag ==1):
        restored_int_val = int(value_bitarray[:size].to01(),2)
    elif(flag==-1):
        restored_int_val = (-1)*int(flip_bitarray(value_bitarray[:size]).to01(),2)
    return restored_int_val

#return string of 1s and 0s,example "0101010111...", check huffmantable above
def encode_DC_entropy_all(dpcm_arr):
    size_bitarray = bitarray()
    value_bitarray = bitarray()
    for n in dpcm_arr:
        cur_size, cur_value_bitarray = decompose_int_to_size_value(n)
        cur_size_bitarray = huffman_table_DC[hex(cur_size)[2:]]
        size_bitarray += cur_size_bitarray
        value_bitarray += cur_value_bitarray
    return size_bitarray,value_bitarray

#no need to import DC_numbers, after decoding size_bitarray, the length of np array is exactly the number of DC
def decode_DC_entropy_all(size_bitarray,value_bitarray):
    size_decoded_list = size_bitarray.decode(huffman_table_DC)
    DC_numbers = len(size_decoded_list)
    dpcm_arr_restored = np.empty(DC_numbers,dtype=int)
    index = 0
    for str_cur_size in size_decoded_list: # str_cur_size may have values of 'a' 'b' '9' etc
        cur_size = int(str_cur_size,16)
        restored_val = compose_size_value_to_int(cur_size,value_bitarray)
        dpcm_arr_restored[index] = restored_val
        #change value_bitarray & index
        value_bitarray = value_bitarray[cur_size:]
        index+=1
    return dpcm_arr_restored


def RLE(ac):
    #ac should be 1D np array containing 63 AC coefficients
    #rle_arr is not LENGTH-FIXED! depending on how many 0s it has
    #use list first, append, then np.array() switching to nparray
    rle_list = []
    consecutive_0s = 0
    for ac_coefficient in ac:
        if(ac_coefficient!=0): 
            consecutive_0s+=1
        else:
            consecutive_0s=0
            rle_list.append((consecutive_0s,ac_coefficient))
    #do not append(0,0), insert it directly in huffman_ac(for example we have 21 consecutive 0s at the end, we do NOT store as (21,0,0))
    return rle_list

def RLE_decode(rle):
    ac_restored_lst = []
    for consecutive_0s,number in rle:
         ac_restored_lst.extend([0]*consecutive_0s)
         ac_restored_lst.append(number)
    ac_restored_lst.extend([0]*(63-len(ac_restored_lst))) #add 0s at the tail
    ac_restored_array = np.array(ac_restored_lst)
    return ac_restored_array

def decompose_RLE_list_to_huffmanResBitarray_valueBitarray(rle_list):
    huffman_res_bitarray = bitarray()
    value_bitarray = bitarray() 
    for item in rle_list:
        consecutive_0s = item[0]
        (cur_size,cur_value_bitarray) = decompose_int_to_size_value(item[1])
        cur_huffman_key_tuple = (consecutive_0s,cur_size)
        cur_huffman_res_bitarray = huffman_table_AC[cur_huffman_key_tuple]
        huffman_res_bitarray += cur_huffman_res_bitarray
        value_bitarray += cur_value_bitarray
    return huffman_res_bitarray,value_bitarray

def AC_huffman_decode_one_step(huffman_bitarray_to_be_decoded):
    huffman_tree_AC = construct_huffman_tree_from_huffman_dict(huffman_table_AC)
    cur_node = huffman_tree_AC
    for int_i in huffman_bitarray_to_be_decoded:
        cur_node = cur_node[int_i]
        if cur_node is None:
            raise ValueError
        elif isinstance(cur_node[0], int):
            ret = cur_node #(cur_consecutive_0s,cur_size)
    return ret

#AC entropy encode/decode is NOT symmetric, encode only did 1 block, but decode needs to deal with huffman encoded result from ALL blocks(as they are stored tgt)
def All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(all_block_huffman_res_bitarray,all_block_value_bitarray):
    all_block_rle_lists = []
    huffman_to_be_decoded = all_block_huffman_res_bitarray
    value_bitarray_left = all_block_value_bitarray
    cur_block_index = 0
    cur_block_RLE_lst = []
    while(len(huffman_to_be_decoded)):
        cur_consecutive_0s,cur_size = AC_huffman_decode_one_step(huffman_to_be_decoded)
        if((cur_consecutive_0s,cur_size) == (0,0)): #reaching end of 1 8x8 block
            all_block_rle_lists.append(cur_block_RLE_lst)
            cur_block_index += 1
            cur_block_RLE_lst = []
        restored_val = compose_size_value_to_int(cur_size,value_bitarray_left)
        cur_block_RLE_lst.append((cur_consecutive_0s,restored_val))
        
        huffman_to_be_decoded = huffman_to_be_decoded[len(huffman_table_AC[(cur_consecutive_0s,cur_size)]):] #update huffman_to_be_decoded, remove those already decoded
        value_bitarray_left = value_bitarray_left[cur_size:]
    return all_block_rle_lists

    






all_0s = np.zeros(63,dtype=int)
a = bitarray('11010100')
a_flipped = flip_bitarray(a)
print(a_flipped)
print(decompose_int_to_size_value(-11))
print("============")
print("dc:",dc_y[:10])
dc_y_dpcm_arr = DPCM(dc_y)
DC_entropy_encode_res = encode_DC_entropy_all(dc_y_dpcm_arr)
print("dc dpcm origin:",dc_y_dpcm_arr[:10])
(size_bitarray,value_bitarray) = DC_entropy_encode_res
dpcm_restored = decode_DC_entropy_all(size_bitarray,value_bitarray)
dc_y_restored = DPCM_decode(dpcm_restored)
print("dpcm restored:",dpcm_restored[:10])
print("dc_y_restored:",dc_y_restored[:10])
print(size_bitarray,value_bitarray)

mylst = create_nested_list(3)
# print(id(mylst))
# node = mylst[0]
# print(id(node))
# node = 1
# print(node)
# print(mylst)
lst2= (0,1,1)
print(mylst(lst2))

#怎么创建list中部分list的reference？ 用numpy array？





