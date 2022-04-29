import numpy as np
A = np.arange(4)
B = A[np.newaxis, :]
print(B)
C = A[: ,np.newaxis]
print(C)
