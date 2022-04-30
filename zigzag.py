from pickletools import uint8
import numpy as np


def zigzag_sequence_generator(n): #this IS a generator, NOT a function
    point = np.array([0,0])
    MOVING_RIGHT,MOVING_DOWN_LEFT,MOVING_DOWN,MOVING_UP_RIGHT = range(4) #4 states
    state = MOVING_RIGHT
    #不需要判断在不在边界内，因为我们用point[0]和point[1]来判断是不是应该转变状态了
    #n 满足 2^k,例如2,4,8,16
    for i in range(n*n):
        yield (i,point)
        if(state == MOVING_RIGHT):
            point+=[0,1]
            #注意右上角，point[1]==0 的判断要在 point[1]==7之前
            if(point[0]==0):
                state = MOVING_DOWN_LEFT
            elif(point[0]==7):
                state = MOVING_UP_RIGHT
        elif(state == MOVING_DOWN_LEFT):
            point+=[1,-1]
            if(point[0]==7):
                state = MOVING_RIGHT
            elif(point[1]==0):
                state = MOVING_DOWN
        elif(state == MOVING_DOWN):
            point+=[1,0]
            if(point[1]==0):
                state = MOVING_UP_RIGHT
            elif(point[1]==7):
                state = MOVING_DOWN_LEFT
        elif(state == MOVING_UP_RIGHT):
            point+=[-1,1]
            if(point[1]==7):
                state = MOVING_DOWN  
            elif(point[0]==0):
                state = MOVING_RIGHT



n = 8
zigzag_sequence_array = np.empty((64,2),dtype=int)
for point in zigzag_sequence_generator(n):
    print(point)
for (i,point) in zigzag_sequence_generator(n):
    zigzag_sequence_array[i] = point
print(zigzag_sequence_array)

block_quant_known =  np.random.randint(0,100, (8,8))
array_generate = np.empty((64),dtype=int)
for i,point in enumerate(zigzag_sequence_array):
    # print(block_quant_known[tuple(point)])
    array_generate[i] = block_quant_known[tuple(point)]
print("==============")
print("block-->array")
print(block_quant_known)
print(array_generate)


array_known = np.random.randint(0,100,(64))
block_generate = np.empty((8,8),dtype=int)
for i,point in enumerate(zigzag_sequence_array):
    # print(block_quant_known[tuple(point)])
    block_generate[tuple(point)] = array_known[i]

print("==============")
print("array->block")
print(block_quant_known)
print(array_generate)