import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    #coloca en la imagen el rectangulo
    #cv2.imshow('add rectangle',img)
    crop_img = img[100:300, 100:300]
    #extrae parte de la imagen
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)  
    #cv2.imshow('filtrado gausiano',blurred)
    #escala de grises y filtrado
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cv2.namedWindow("Thresholded", cv2.WINDOW_NORMAL) 
    cv2.imshow('Thresholded', thresh1)
    im2,contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) # se encuentran los contornos

    max_area = -1
    #print len(contours)
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        #print area
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci] # se selecciona el contorno mas grande
    cv2.namedWindow("contours", cv2.WINDOW_NORMAL) 
    cv2.imshow('contours',im2)
    x,y,w,h = cv2.boundingRect(cnt)# medidas para los contornos
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)# se dibuja un rectangulo al objeto detectado
    hull = cv2.convexHull(cnt)#se detecta los convex hull a los objetos detectados
    drawing = np.zeros(crop_img.shape,np.uint8)#se crea una imagen de ceros osea negra
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0) #se dibuja esos contornos en la imagen negra
    cv2.drawContours(drawing,[hull],0,(255,0,0),0) # se dibuja los convexhull en la imagen negra
    cv2.namedWindow("drawing", cv2.WINDOW_NORMAL) 
    cv2.imshow('drawing', drawing) # se muestra la imagen negra
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)# se calculan los defectos para el analisis de gestos
    count_defects = 0


    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects == 1:
        cv2.putText(img,"I am Vipul", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 2:
        str = "This is a basic hand gesture recognizer"
        cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img,"This is 4 :P", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 4:
        cv2.putText(img,"Hi!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    else:
        cv2.putText(img,"Hello World!!!", (50,50),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    #cv2.imshow('drawing', drawing)
    #cv2.imshow('end', crop_img)
    cv2.namedWindow("Gesture", cv2.WINDOW_NORMAL) 
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))# se combina la imagen para mostrar
    cv2.namedWindow("Contours", cv2.WINDOW_NORMAL) 
    cv2.imshow('Contours', all_img)
    k = cv2.waitKey(10)
    if k == 27:
        break
