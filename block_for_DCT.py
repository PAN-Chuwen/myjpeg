from PIL import Image
import numpy as np

image = Image.open('cat.png')
ycbcr = image.convert('YCbCr')
npmat = np.array(ycbcr, dtype=np.uint8)
#假设padding已经做过了，我们接下来操作的都是对padding后的npmat进行操作
block = npmat[0:8,0:8,2]
print(npmat)
print(block)