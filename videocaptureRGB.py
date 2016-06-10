import numpy as np
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret,frame = cap.read()
    b,g,r = cv2.split(frame)
    img2 = cv2.merge([b,g,r])
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the resulting frame
    #cv2.imshow('color gray',gray)
    cv2.imshow('R',r)
    cv2.imshow('G',g)
    cv2.imshow('B',b)
    cv2.imshow('img2',img2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
