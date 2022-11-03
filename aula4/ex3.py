import argparse
import cv2
import copy
import numpy as np

# Global variables
window_name = 'Segmentation'
image_gray = None
image = None

ranges = {  'b' : {'min': 0, 'max': 100},
            'g' : {'min': 80, 'max': 256},
            'r' : {'min': 0, 'max': 100}}

def onTrackbarMin(threshold):
    global ranges
    ranges['r']['min'] = threshold
    onTrackbar()

def onTrackbarMax(threshold):
    global ranges
    ranges['r']['max'] = threshold
    onTrackbar()

def onTrackbar():
    global image, ranges

    mins = np.array([ranges['b']['min'], ranges['g']['min'], ranges['r']['min']])
    maxs = np.array([ranges['b']['max'], ranges['g']['max'], ranges['r']['max']])
    mask = cv2.inRange(image,mins,maxs)
    mask = mask.astype(np.bool_)

    image_processed = copy.deepcopy(image)
    image_processed[np.logical_not(mask)] = 0

    cv2.imshow(window_name, image_processed)
    cv2.waitKey(0)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help='Full path to image file.')
    args = vars(parser.parse_args())

    global image

    image_path = args['image']    
    if not args['image']:
        image_path = 'images/atlas2000_e_atlasmv.png'
    
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Load an image
    global image_gray # use global var
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert bgr to gray image (single channel)
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image_gray)

    cv2.createTrackbar('minR', window_name, 0, 256, onTrackbarMin)
    cv2.createTrackbar('minR', window_name, 0, 256, onTrackbarMax)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()