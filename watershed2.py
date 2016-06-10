# USAGE
# python watershed.py --image images/coins_01.png

# import the necessary packages
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments

# load the image and perform pyramid mean shift filtering
# to aid the thresholding step
imgOriginal = cv2.imread('ImagenesIR/plantCount.jpg')            # read next frame
b, g, r = cv2.split(imgOriginal)


img = (r-b)
cv2.imshow('img',img)
grey = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
value = (35, 35)
_,th1 = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#cv2.imshow('Thresholded', th1)
##############################
kernel = np.ones((4,10),np.uint8)
kernel2 = np.ones((3,3),np.uint8)
kernel3 = np.ones((2,2),np.uint8)
closing = cv2.morphologyEx(th1,cv2.MORPH_CLOSE,kernel3, iterations = 3)
opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel, iterations = 2)#transformacion morfologica para eliminar ruido
#closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel3, iterations = 3)#transformacion morfologica para eliminar ruido
erosion = cv2.erode(opening,kernel2,iterations = 2)
cv2.imshow('Thresholded con MorphologyExopen', closing)
cv2.imshow('Thresholded con morphologyex+open,close', opening)
cv2.imshow('Thresholded con morphologyex+erode', erosion)


#sure_bg = cv2.dilate(erosion,kernel3,iterations=3)

#D = ndimage.distance_transform_edt(erosion)

D = cv2.distanceTransform(erosion,cv2.DIST_L2,3)

localMax = peak_local_max(D, indices=False, min_distance=25,
	labels=erosion)
#cv2.imshow('dist2',D)
cv2.imwrite('dist.jpg',D)
# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]

print markers
labels = watershed(-D, markers, mask=erosion)
print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
# loop over the unique labels returned by the Watershed
# algorithm
for label in np.unique(labels):
	# if the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue

	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mask = np.zeros(grey.shape, dtype="uint8")
	mask[labels == label] = 255

	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)

	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	cv2.circle(imgOriginal, (int(x), int(y)), int(r), (0, 255, 0), 2)
	cv2.putText(imgOriginal, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# show the output image
cv2.imshow("Output", imgOriginal)
cv2.waitKey(0)