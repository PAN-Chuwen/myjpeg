import numpy as np
from scipy import fftpack

#From padding_image.py we have Y_padded, Cr_padded, Cb_padded
#return Y_DCT->Y_quant, Cr_DCT->Cr_quant,...

def DCT_2D(block):
    #norm = 'ortho' makes every basis of DCT matrix of distance 1
    DCT_matrix = fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')
    return DCT_matrix

def iDCT_2D(DCT_block):
    block = fftpack.idct(fftpack.idct(DCT_block.T,norm='ortho').T,norm='ortho')
    return block

def get_quantization_table(type):
    #JPEG standard quantization table, reference: https://www.sciencedirect.com/topics/engineering/quantization-table
    if(type=='lum'):
        table = np.array(
                      [[16,	11,	10,	16,	24,	40,	51,	61],
                      [12,	12,	14,	19,	26,	58,	60,	55],
                      [14,	13,	16,	24,	40,	57,	69,	56],
                      [14,	17,	22,	29,	51,	87,	80,	62],
                      [18,	22,	37,	56,	68,	109,103,77],
                      [24,	35,	55,	64,	81,	104,113,92],
                      [49,	64,	78,	87,	103,121,120,101],
                      [72,	92,	95,	98,	112,100,103,99]]
    )
    elif(type=='chrom'):
        table =  np.array(
                    [[ 17,	18,	24,	47,	99,	99,	99,99],
                    [18,21,	26,	66,	99	,99,99,99],
                    [24	,26	,56	,99	,99	,99	,99	,99],
                    [47,66,	99,	99,	99	,99,99,	99],
                    [99	,99	,99	,99	,99	,99,99,	99],
                    [99	,99	,99	,99	,99	,99	,99	,99],
                    [99	,99	,99	,99	,99	,99	,99	,99],
                    [99,99,	99,	99,	99,	99,	99,	99]]
    )
    return table

def quant_block(block,type):
    quant_table = get_quantization_table(type)
    quanted_block = (block/quant_table).round().astype(np.int32)
    return quanted_block

def dequant_block(block,type):
    quant_table = get_quantization_table(type)
    dequanted_block = block*quant_table.astype(np.int32)
    return dequanted_block

# block = np.ones((8,8))

# print(block)
# DCT_block = fftpack.dct(block)
# print(DCT_block)
# DCT_block_2 = fftpack.dct(DCT_block.T)
# print(DCT_block_2)

# block_rand = np.random.randint(0,100,(8,8)).astype(float)
# #problem: dtype int not supported, check https://stackoverflow.com/questions/12307429/scipy-fftpack-and-float64

# DCT_block_rand = DCT_2D(block_rand)

# block_rand_restored_from_DCT = iDCT_2D(DCT_block_rand)
# print("original block:",block_rand)
# print("after DCT:",DCT_block_rand.astype(int))
# print("restored directly from DCT",block_rand_restored_from_DCT.astype(int))

# block_quanted = quant_block(DCT_block_rand,'lum')
# block_dequanted = dequant_block(block_quanted,'lum')
# print("after DCT:",DCT_block_rand.astype(int))
# print("quanted block",block_quanted)
# print("dequanted block",block_dequanted)

