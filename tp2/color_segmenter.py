# ---------------------------------------------------------
# TP2 - Augmented Reality Paint
# Python script to configure color detection
# Daniel Sousa Oliveira nº 89208
# PSR, November 2022.
# ---------------------------------------------------------

from colorama import *
import copy
import json
import cv2
import numpy as np


def onTrackbar(value):
    pass

def processImage(capture, ranges, window_name):
    """Capture images from camera
    Define maximum and minimum values for R,G,B values
    Process camera images using the same max and min values
    Segment image pixels by color

    Parameters
    ----------
    capture : cv2.VideoCapture
        Used to capture images from camera
    ranges : dict
        Format to store maximum and minimum RGB values
    window_name : str
        Same window name to match cv2.imshow

    Returns
    -------
    image_processed: cv2.image
        Result of the segmentation process
    """

    _, image = capture.read()

    ranges['limits']['B']['min'] = cv2.getTrackbarPos('MinB', window_name)
    ranges['limits']['B']['max'] = cv2.getTrackbarPos('MaxB', window_name)
    ranges['limits']['G']['min'] = cv2.getTrackbarPos('MinG', window_name)
    ranges['limits']['G']['max'] = cv2.getTrackbarPos('MaxG', window_name)
    ranges['limits']['R']['min'] = cv2.getTrackbarPos('MinR', window_name)
    ranges['limits']['R']['max'] = cv2.getTrackbarPos('MaxR', window_name)

    mins = np.array([ranges['limits']['B']['min'], ranges['limits']['G']['min'], ranges['limits']['R']['min']])
    maxs = np.array([ranges['limits']['B']['max'], ranges['limits']['G']['max'], ranges['limits']['R']['max']])
    mask = cv2.inRange(image, mins, maxs)
    mask = mask.astype(np.bool_)

    image_processed = copy.deepcopy(image)
    image_processed[np.logical_not(mask)] = 0

    return image_processed
    


def processSegmentation(capture, ranges, window_name):
    """Continuously gather images from camera and save parameters
    from trackbars using 'w' key.

    Parameters
    ----------
    capture : cv2.VideoCapture
        Used to capture images from camera
    ranges : dict
        Format to store maximum and minimum RGB values
    window_name : str
        Same window name to match cv2.imshow
    """

    while True:

        image_processed = processImage(capture, ranges, window_name)

        if image_processed is None:
            print('Not possible to capture image, breaking!')
            break

        cv2.imshow(window_name, image_processed)

        key = cv2.waitKey(50)

        if key == ord('w'):

            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                json.dump(ranges, file_handle)

        elif key == ord('q'):

            print('Closing program')
            break


def main():
    """Define dictionary format to save data
    Initialize cv2 windows and trackbars
    Start segmentation process
    """

    ranges = {'limits': {'B': {'max': 255, 'min': 0},
                         'G': {'max': 255, 'min': 0},
                         'R': {'max': 255, 'min': 229}}}

    capture = cv2.VideoCapture(0)

    window_name = 'Color Segmentation'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, (600,600))

    cv2.createTrackbar('MinB', window_name, 0, 256, onTrackbar)
    cv2.createTrackbar('MaxB', window_name, 256, 256, onTrackbar)
    cv2.createTrackbar('MinG', window_name, 0, 256, onTrackbar)
    cv2.createTrackbar('MaxG', window_name, 256, 256, onTrackbar)
    cv2.createTrackbar('MinR', window_name, 0, 256, onTrackbar)
    cv2.createTrackbar('MaxR', window_name, 256, 256, onTrackbar)

    processSegmentation(capture, ranges, window_name)

    cv2.destroyAllWindows()
    capture.release()

if __name__ == '__main__':
    main()