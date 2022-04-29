import numpy as np
from PIL import Image

from repeatCol import B_padded




B = np.random.randint(0,100, (5,6,3))
print(B)

B_last_row = B[-1,:,:]
print(B_last_row)

B_append = np.broadcast_to(B_last_row, (8-B.shape[0],B.shape[1],3))

B_padded = np.vstack((B,B_append))
