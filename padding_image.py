from PIL import Image
import numpy as np



def matrix_padding(npmat):
    #传进来的npmat包括Y,subsample过的Cb,Cr矩阵
    rows =  npmat.shape[0]
    rows_pad = (rows//8+1)*8

    cols =  npmat.shape[1]
    cols_pad = (cols//8+1)*8

    #used for 3D matrix
    mat_append_col = np.broadcast_to(npmat[:,-1][:,None],(npmat.shape[0],cols_pad-npmat.shape[1]))

    mat_padded_col = np.hstack((npmat,mat_append_col))


    mat_append_row = np.broadcast_to(mat_padded_col[-1,:],(rows_pad - mat_padded_col.shape[0],cols_pad))
    mat_padded_row = np.vstack((mat_padded_col,mat_append_row))
    mat_pad = mat_padded_row

    return mat_pad

def restore_img(Y_padded,Cb_padded,Cr_padded,rows_origin,cols_origin):
    Cb_restored = np.repeat((np.repeat(Cb_padded,2,axis=1)),2,axis=0)
    Cr_restored = np.repeat((np.repeat(Cr_padded,2,axis=1)),2,axis=0)
    npmat_restored = np.empty([rows_origin,cols_origin,3],dtype=np.uint8)
    npmat_restored[:,:,0] = Y_padded[:rows_origin,: cols_origin]
    npmat_restored[:,:,1] = Cb_restored[:rows_origin,:cols_origin]
    npmat_restored[:,:,2] = Cr_restored[:rows_origin,:cols_origin]
    return npmat_restored

image = Image.open('ti10.png')
ycbcr = image.convert('YCbCr')
npmat = np.array(ycbcr, dtype=np.uint8)

rows =  npmat.shape[0]
rows_pad = (rows//100+1)*100

cols =  npmat.shape[1]
cols_pad = (cols//100+1)*100

#used for 3D image, no subsample
mat_append_col = np.broadcast_to(npmat[:,-1][:,None],(npmat.shape[0],cols_pad-npmat.shape[1],3))

mat_padded_col = np.hstack((npmat,mat_append_col))


mat_append_row = np.broadcast_to(mat_padded_col[-1,:,:],(rows_pad - mat_padded_col.shape[0],cols_pad,3))
mat_padded_row = np.vstack((mat_padded_col,mat_append_row))
mat_pad = mat_padded_row
image_padded = Image.fromarray(mat_padded_row,'YCbCr')
image_padded.show()

Y = npmat[:,:,0]
print(Y)
print(Y.shape)
Y_padded = matrix_padding(Y)
print(Y_padded)
print(Y_padded.shape)

Cb = npmat[::2,::2,1]
print(Cb)
print(Cb.shape)
Cb_padded = matrix_padding(Cb)
print(Cb_padded)
print(Cb_padded.shape)

Cr = npmat[::2,::2,2]
Cr_padded = matrix_padding(Cr)


Cb_restored = np.repeat((np.repeat(Cb_padded,2,axis=1)),2,axis=0)
Cr_restored = np.repeat(Cr_padded,2,axis=1)

print(Cb_restored)
print(Cb_restored.shape)

npmatrix_restored = restore_img(Y_padded,Cb_padded,Cr_padded,rows,cols)
image_restored = Image.fromarray(npmatrix_restored,'YCbCr')
image_restored.show()
