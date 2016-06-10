import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('coins.jpg')#lectura imagen
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#escala de grises
#ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) # se saca la mascara de las monedas

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')#se muestra la imagen utilziando a gray como mascara
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

#cv2.imshow('detected circles',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
