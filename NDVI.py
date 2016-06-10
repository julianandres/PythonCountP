import time
import numpy as np
from matplotlib import pyplot as plt

import cv2



def disp_multiple(im1=None, im2=None, im3=None, im4=None):
    """
    Combines four images for display.
    """
    height, width = im1.shape

    combined = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)

    combined[0:height, 0:width, :] = cv2.cvtColor(im1, cv2.COLOR_GRAY2RGB)
    combined[height:, 0:width, :] = cv2.cvtColor(im2, cv2.COLOR_GRAY2RGB)
    combined[0:height, width:, :] = cv2.cvtColor(im3, cv2.COLOR_GRAY2RGB)
    combined[height:, width:, :] = cv2.cvtColor(im4, cv2.COLOR_GRAY2RGB)

    return combined


def label(image, text):
    """
    Labels the given image with the given text
    """
    return cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    print in_min
    in_max = np.percentile(im, 95)
    print in_max
    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


def run():
    
    imgOriginal = cv2.imread('ImagenesIR/planta21.jpg')            # read next frame
    b, g, r = cv2.split(imgOriginal)

    # Calculate the NDVI

    # Bottom of fraction
    bottom = (r.astype(float) + b)
    bottom[bottom == 0] = 0.01  # Make sure we don't divide by zero!

    ndvi = (r - b) / bottom
   # print ndvi
    columnacero=0
    filacero=0
    rows, cols = ndvi.shape
   # print rows
   # print cols
    #print ndvi[2,3]
    drawing = np.zeros(ndvi.shape,np.uint8)
    for i in range(rows): 
        for j in range(cols):
            if (ndvi[i,j]<=0):
                drawing[i,j]=ndvi[i,j]
               #print ndvi[i,j]
               #ndvi[i,j]=0   

    #drawing = contrast_stretch(drawing)
    #drawing = drawing.astype(np.uint8)
    ndvi = contrast_stretch(ndvi)
    ndvi = ndvi.astype(np.uint8) #unsigned integer

    # Do the labelling
    label(b, 'Blue')
    label(g, 'Green')
    label(r, 'NIR')
    label(ndvi, 'NDVI')

    # Combine ready for display
    combined = disp_multiple(b, g, r, ndvi)

    
    # Display

    cv2.imwrite('resultado.jpg',combined)
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL) 
    cv2.imshow('Result',combined)
    #cv2.imshow('IMGZeros',drawing)
    # stream.truncate(0)

    # If we press ESC then break out of the loop
    c = cv2.waitKey(7) % 0x100
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Important cleanup here!
        

if __name__ == '__main__':
    run()