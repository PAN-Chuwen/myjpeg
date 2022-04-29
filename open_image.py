from PIL import Image
import numpy as np

image = Image.open('cat.png')
ycbcr = image.convert('YCbCr')
npmat = np.array(ycbcr, dtype=np.uint8)
print(npmat.shape)
image_back = Image.fromarray(npmat,'YCbCr')
image_back.show()
