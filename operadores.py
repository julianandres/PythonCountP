import numpy as np
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('raspberrypi.png')
img2 = cv2.imread('coins.jpg')

# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
print rows
print cols
roi = img1[0+20:rows+20, 0+20:cols+20 ] # se saca la region de interes usando el tamanio de la imagen original para insertarla

# Now create a mask of logo and create its inverse mask also #se saca una mascara para llevar a cabo el proceso
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) #escala de grises
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #mascara binaria usando threshold
mask_inv = cv2.bitwise_not(mask) # se invierte la maskara usando el operador not
cv2.namedWindow("mascara", cv2.WINDOW_NORMAL) 
cv2.namedWindow("mascara invertida", cv2.WINDOW_NORMAL) 
cv2.imshow('mascara',mask)
cv2.imshow('mascara invertida',mask_inv) 
# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv) # se realiza la operacion AND entre la ROI de la imagen original y la mascara invertida de la img2
cv2.namedWindow("black out bg", cv2.WINDOW_NORMAL) 
cv2.imshow('black out bg',img1_bg)
# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img2,img2,mask = mask)#coge solo lo que tiene la  mascara y se elimina el fondo
cv2.namedWindow("tomar solo el logo--fg", cv2.WINDOW_NORMAL) 
cv2.imshow('tomar solo el logo--fg',img2_fg) 
# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg) # se suma las dos imagenes para formar la nueva ROI

img1[0+20:rows+20, 0+20:cols+20 ] = dst # se incrusta el resultado en la imagen original
cv2.namedWindow("res", cv2.WINDOW_NORMAL) 
cv2.imshow('res',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
