#BMP_Test
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import BMP

Picture=BMP.MakeImage(10,10)
Picture=BMP.PaintImage(10,10)

plt.imshow(Picture)
plt.show()
# First 14 bits of a file indicate that this one is a BMP file
Pic2=BMP.PaintImageDynamic(10,10,dtype=np.uint16)
plt.imshow(Pic2)
plt.show()
IMG=cv.imread('Brick.jpg')
BMP.BMP_File('Test.bmp',IMG)
