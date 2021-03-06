    
import time
import numpy as np
from matplotlib import pyplot as plt
import cv2

imgOriginal = cv2.imread('ImagenesIR/plantCount.jpg')            # read next frame
b, g, r = cv2.split(imgOriginal)


img = (r-b)
cv2.imshow('img',img)
grey = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
value = (35, 35)
_,th1 = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#cv2.imshow('imgRed',r)
kernel = np.ones((4,6),np.uint8)
kernel2 = np.ones((3,5),np.uint8)
kernel3 = np.ones((2,2),np.uint8)

cv2.imshow('Thresholded', th1)
##############################

#closing = cv2.morphologyEx(th1,cv2.MORPH_CLOSE,kernel3, iterations = 3)
opening = cv2.morphologyEx(th1,cv2.MORPH_OPEN,kernel, iterations = 3)#transformacion morfologica para eliminar ruido
#opening = cv2.GaussianBlur(opening,(5,5),0)
closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel3, iterations = 4)#transformacion morfologica para eliminar ruido
erosion = cv2.erode(closing,kernel2,iterations = 2)
cv2.imshow('Thresholded con MorphologyExopen', opening)
cv2.imwrite('thwmopen.jpg',opening)
cv2.imshow('Thresholded con morphologyex close', closing)
cv2.imshow('Thresholded con morphologyex erode', erosion)
#######################################

sure_bg = cv2.dilate(erosion,kernel3,iterations=3)
dist_transform = cv2.distanceTransform(erosion,cv2.DIST_L2,5)
#ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#cv2.imshow('dist', dist_transform)
#cv2.imwrite('dist.jpg', dist_transform)
ret, sure_fg = cv2.threshold(dist_transform,0.09*dist_transform.max(),255,0)
#cv2.imshow('sure_fg', sure_fg)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
#cv2.imshow('unknown',unknown)
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
markers = cv2.watershed(imgOriginal,markers)

print("[INFO] {} unique segments found".format(len(np.unique(markers)) - 1))
####################################################################3
radios = np.zeros(len(np.unique(markers)),dtype='Float64')
print radios.shape
i=0
for label in np.unique(markers):
	# if the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue
	
	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mascara1 = np.zeros(grey.shape, dtype="uint8")
	mascara1[markers == label] = 255
        #print i
        #print str(i)+"i"
 	#print str(label)+"label"
        # print radio
	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mascara1.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)
	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
        if label>0 and label!=1 :
	   radios[i]= r
 	i=i+1

print radios
acumulado=0
denominador=0
for item in radios:
    acumulado=acumulado+item
    denominador = denominador +1

print len(radios)
print denominador
promedio = acumulado/denominador
print promedio
     

mascaraSuperior = np.zeros(grey.shape, dtype="uint8")
mascaraInferior = np.zeros(grey.shape, dtype="uint8")

for label in np.unique(markers):
	# if the label is zero, we are examining the 'background'
	# so simply ignore it

	if label == 0:
		continue
	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mascara = np.zeros(grey.shape, dtype="uint8")
	
        mascara[markers == label] = 255
        #print mascara
	
        #print radio
	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]

	c = max(cnts, key=cv2.contourArea)

	
	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.imwrite('mascara'+str(label)+'.jpg',mascara)
        if label>0 and label!=1 and r>promedio:
            print ('el valor de' +str(r)+ 'es superior al promedio '+str(promedio))
            mascaraSuperior = mascara + mascaraSuperior
	    #cv2.imwrite('mask.jpg',mascara)
	if label>0 and label!=1 and r<=promedio:
            print ('el valor de' +str(r)+ 'es inferior al promedio '+str(promedio))
            mascaraInferior = mascara + mascaraInferior


cv2.imshow('maskSuperior',mascaraSuperior)
cv2.imshow('maskInferior',mascaraInferior)
kernel4 = np.ones((1,8),np.uint8)
################################################################################################################
opening1 = cv2.morphologyEx(mascaraSuperior,cv2.MORPH_OPEN,kernel4, iterations = 2)#transformacion morfologica para eliminar ruido
#opening = cv2.GaussianBlur(opening,(5,5),0)
#closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel3, iterations = 3)#transformacion morfologica para eliminar ruido
erosion1 = cv2.erode(opening1,kernel2,iterations = 2)
cv2.imshow('posProcessed con MorphologyExopen', opening1)
#cv2.imshow('Thresholded con morphologyex+open,close', opening)
cv2.imshow('post processed con morphologyex+erode', erosion1)
##################################################################################################################


sure_bg1 = cv2.dilate(erosion1,kernel3,iterations=3)
dist_transform1 = cv2.distanceTransform(erosion1,cv2.DIST_L2,5)
#ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#cv2.imshow('dist', dist_transform1)
#cv2.imwrite('dist.jpg', dist_transform)
ret, sure_fg1 = cv2.threshold(dist_transform1,0.08*dist_transform1.max(),255,0)
cv2.imshow('sure_fg', sure_fg1)
# Finding unknown region
sure_fg1 = np.uint8(sure_fg1)
unknown1 = cv2.subtract(sure_bg1,sure_fg1)
#cv2.imshow('unknown',unknown1)
# Marker labelling

ret, markers1 = cv2.connectedComponents(sure_fg1)

# Add one to all labels so that sure background is not 0, but 1
markers1 = markers1+1
# Now, mark the region of unknown with zero
markers1[unknown1==255] = 0
markers1 = cv2.watershed(imgOriginal,markers1)

print("[INFO] {} unique segments found".format(len(np.unique(markers1)) - 1))
for label in np.unique(markers1):
	# if the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue
	
	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mascara1 = np.zeros(grey.shape, dtype="uint8")
	mascara1[markers1 == label] = 255
        #print i
        #print str(i)+"i"
 	#print str(label)+"label"
        # print radio
	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mascara1.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)
	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(imgOriginal, (int(x), int(y)), int(r), (0, 255, 0), 2)
	cv2.putText(imgOriginal, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow('result',imgOriginal)
#cv2.imshow('fg', sure_fg)
#########################
#erosion2 = cv2.erode(th1,kernel,iterations = 2)
#opening2 = cv2.morphologyEx(erosion2,cv2.MORPH_OPEN,kernel2, iterations = 2)
#cv2.imshow('Thresholded con erosion', erosion2)
#cv2.imshow('Thresholded con erosion+morphology', opening2)
######################################
#cv2.imshow('Thresholded2', th2)
#cv2.imshow('Thresholded3', th3)



# Display

#cv2.imshow('IMGZeros',drawing)
# stream.truncate(0)

# If we press ESC then break out of the loop
c = cv2.waitKey(7) % 0x100
cv2.waitKey(0)
cv2.destroyAllWindows()
