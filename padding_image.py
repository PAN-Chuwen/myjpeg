from PIL import Image
import numpy as np

image = Image.open('ti10.png')
ycbcr = image.convert('YCbCr')
npmat = np.array(ycbcr, dtype=np.uint8)

rows =  npmat.shape[0]
rows_pad = (rows//100+1)*100

cols =  npmat.shape[1]
cols_pad = (cols//100+1)*100

mat_append_col = np.broadcast_to(npmat[:,-1][:,None],(npmat.shape[0],cols_pad-npmat.shape[1],3))

mat_padded_col = np.hstack((npmat,mat_append_col))


mat_append_row = np.broadcast_to(mat_padded_col[-1,:,:],(rows_pad - mat_padded_col.shape[0],cols_pad,3))
mat_padded_row = np.vstack((mat_padded_col,mat_append_row))
mat_pad = mat_padded_row
image_padded = Image.fromarray(mat_padded_row,'YCbCr')
image_padded.show()