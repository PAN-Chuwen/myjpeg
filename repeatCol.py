import numpy as np
from PIL import Image
# 2D version
# A = np.random.randint(0, 100, (15, 14))
# print(A)
# # np.hstack((A, np.broadcast_to(A[:, -1][:, None], (A.shape[1], n))))
# print(A[:,-1])
# print(A[:,-1][:,None])
# A_append = np.broadcast_to(A[:, -1][:, None],(A.shape[0],16-A.shape[1]))
# print(A_append)

# A_padded = np.hstack((A,A_append))
# print(A_padded)

#3D version
B = np.random.randint(0,100, (5,6,3))
print(B)

B_append = np.broadcast_to(B[:,-1][:,None],(B.shape[0],8-B.shape[1],3))
print(B_append)

B_padded = np.hstack((B,B_append))
print(B_padded)
#DONE!!! YES!

#convert 3D npmatrix to Image
print(B_padded.shape)
image = Image.fromarray(B_padded,'YCbCr')
image.show()