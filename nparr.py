from PIL import Image
import numpy as np
from bitarray import *
from bitarray.util import *
from entropy_encoding import *

A = np.array([[1,2],[3,4],[5,6]])
print(A)
B = A[0:2]
print(B)
B[1][1] = 99
print(B)
print(A)
C = A[::2,0]
D = A[:,1]
print(C)
print(D)

A1 = np.array([1,2,3,4,5])
A2 = np.array([6,7,8,9,10])
A3 = np.array([11,12,13,14,15])

npmat_restored = np.empty([3,5,3],dtype=np.uint8)
print(npmat_restored)
npmat_restored[:,:,0] = A1
print(npmat_restored)


tmp_array = np.empty((64))
print(tmp_array)
print(type(A1[0:1]))
print(type(A2[1:4]))
print(np.concatenate((A1[0:1],A2[1:4])))

A = []
print(type(A))
A.append([1,1])
A.append([2,2])
A =np.array(A)
print(A)
print(type(A))
C = np.array((1,2))
D = np.array((*C,3))
print(C)
print(D)
print(type(D))

all_0s = np.zeros(63,dtype=int)
print(type(bin(8)))
print(bin(11))



a = bitarray('11001111')
a = bitarray
str2 = '11110000'

a = bitarray(str2)
# b = np.array(a.tolist())
# print(b)
f = open("demofile3", "wb")
a.tofile(f)
f.close()

f = open("demofile3","rb")
b = bitarray()
b.fromfile(f)
lst = b.tolist()
print(lst)
str1 = ''.join(str(e) for e in lst)
print(str1)
# print(''.join(lst))
# str = ''.join(lst)
# print(str)
aa = np.array([11])
print(aa.shape[0])

lst = []
lst.extend(0*[1])
print(lst)

lst = [(1,2),(3,4)]
for a,b in lst:
    print([a,b])

a = bitarray()
print(len(a))

t = ((1,2),(3,4))
print(type(t[0]))

for i in bitarray('10110000'):
    print(type(i))


s='ab'
s.startswith('a')


huffman_dict = {
    (0,0): bitarray('01110'), (0,1): bitarray('01111'),
    (1,0): bitarray('10100'), (1,1): bitarray('10110'),
    (2,0): bitarray('10111')
}

a = bitarray()
a.encode(huffman_dict, [(0,0)])
print(a)

dec = bitarray('011111011101110').decode(huffman_dict)
print(dec)
bb = np.array([[1,2],[3,4]])
for i in bb:
    print(i)



cc = bitarray('111')
dd = bitarray('001')
cc += bitarray('1')
print(cc,dd)
print(ba2int(cc))
print(len(cc))
i = cc.find(dd,0,10)
print(i)

def find_next_ffff_index(b):
    return b.find(bitarray('11111111'),0,len(b))

cc = bitarray('01011010010101010110101111111101010101010101011111111')

next_ff_index = find_next_ffff_index(cc)
part1 = cc[:next_ff_index]
cc = cc[next_ff_index+8:]
next_ff_index = find_next_ffff_index(cc)
part2 = cc[:next_ff_index]
print(part1,part2)


image = Image.open('ti10.png')
ycbcr = image.convert('YCbCr')
npmat = np.array(ycbcr, dtype=np.uint8) - 128
rows,cols = npmat.shape[0],npmat.shape[1]
print(rows,cols)

rows_barr = bitarray(format(rows, '#018b')[2:])
print(rows_barr)
with open('testfile', 'wb') as outFile:
    rows_barr.tofile(outFile)


rle_list = [[2,-4],[0,12]]
res = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(rle_list)
print("encodedResult:",res)

rle_list_restored = All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(res[0],res[1])
print("rle_list_origin:",rle_list)
print("rle_list_restored:",rle_list_restored)



dpcm_arr = [20,1,-1,-2,2,2,2,1,2,1,4]
res = encode_DC_entropy_all(dpcm_arr)
print(res)
dpcm_arr_restored = decode_DC_entropy_all(res[0],res[1])
print("dpcm_arr origin:",dpcm_arr)
print("dpcm_arr_restored from dc entropy decode:",dpcm_arr_restored)

print(decompose_int_to_size_value(0))

npmatt = np.ones((10,10,3))*2 -1
print(npmatt)

lsst= [bitarray(2),bitarray(3),bitarray(4)]

a,b,c = lsst
print(a,b,c)
print(len(lsst))
file_bitarray  = bitarray('1')
# cur_len = 100000
# print(len(file_bitarray))
# file_bitarray = file_bitarray[cur_len:]
print(len(file_bitarray))