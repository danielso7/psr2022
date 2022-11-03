# ---------------------------------------------------------
# Python script to transform images using OpenCV
# Daniel Sousa Oliveira nº 89208
# PSR, October 2022.
# ---------------------------------------------------------

import cv2
import numpy as np

def alineaA(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # Load an image

    retval, image_thresholded = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    print(type(image_thresholded))
    print(image_thresholded.shape)
    print(image_thresholded.dtype)

    cv2.imshow('Alínea A', image_thresholded)
    cv2.waitKey(0)

def alineaB(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # Load an image

    image_thresholded = image > 128

    print(type(image_thresholded))
    print(image_thresholded.shape)
    print(image_thresholded.dtype)

def alineaC(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    b, g, r = cv2.split(image)
    
    retval, b = cv2.threshold(b, 50, 255, cv2.THRESH_BINARY)
    retval, g = cv2.threshold(g, 100, 255, cv2.THRESH_BINARY)
    retval, r = cv2.threshold(r, 150, 255, cv2.THRESH_BINARY)
  
    cv2.imshow("Model Blue Image", b)
    cv2.waitKey(0)
    cv2.imshow("Model Green Image", g)
    cv2.waitKey(0)
    cv2.imshow("Model Red Image", r)
    cv2.waitKey(0)
  
    image_merge = cv2.merge((r, g, b))
  
    cv2.imshow("RGB_Image", image_merge)
    cv2.waitKey(0)   

def alineaD(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    lower_bound = np.array([0,60, 0])
    upper_bound = np.array([50,256,50])

    image_mask = cv2.inRange(image, lower_bound, upper_bound)


    cv2.imshow('RGB Image', image)  
    cv2.imshow('GRAY Image', image_gray)  
    cv2.imshow('Mask Image', image_mask) 
    cv2.waitKey(0)

def alineaE(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow('RGB Image', image_hsv)
    cv2.waitKey(0) 

def alineaF(image_path):

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    lower_bound = np.array([0,60, 0])
    upper_bound = np.array([50,256,50])

    image_mask = cv2.inRange(image, lower_bound, upper_bound)

    cv2.imshow("Mask Image", image_mask)
    cv2.waitKey(0)
    image_mask = image_mask.astype(bool)


    b, g, r = cv2.split(image)
    
    b[image_mask] = b[image_mask] + 170
    g[image_mask] = g[image_mask] + 170
    r[image_mask] = r[image_mask] + 170

    image_mask2 = np.logical_not(image_mask)

    b[image_mask2] = b[image_mask2] * 0.5
    g[image_mask2] = g[image_mask2] * 0.5
    r[image_mask2] = r[image_mask2] * 0.5

    image_merge = cv2.merge((r, g, b))
  
    cv2.imshow("RGB Image", image)
    cv2.waitKey(0)
    cv2.imshow("R Channel", r)
    cv2.waitKey(0)
    cv2.imshow("Merge", image_merge)
    cv2.waitKey(0)
  


def main():

    image_path = 'images/atlascar.png'
    image_path2 = 'images/atlascar2.png'
    image_path3 = 'images/atlas2000_e_atlasmv.png'

    alineaA(image_path)

    alineaB(image_path)

    alineaC(image_path2)

    alineaD(image_path3)

    alineaE(image_path3)

    alineaF(image_path3)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()