from PIL import Image
import numpy as np

A = np.array([[1,2],[3,4],[5,6]])
print(A)
B = A[0:2]
print(B)
B[1][1] = 99
print(B)
print(A)