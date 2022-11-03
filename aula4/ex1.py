# ---------------------------------------------------------
# Python script to open images using OpenCV
# Daniel Sousa Oliveira nº 89208
# PSR, October 2022.
# ---------------------------------------------------------

import cv2
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-path', '--image_path', help="Path to image directory")
    args = vars(parser.parse_args())

    image_path = args['image_path']    
    if not args['image_path']:
        image_path = 'images/atlascar.png'

    image_path2 = 'images/atlascar2.png'

    image = cv2.imread(image_path, cv2.IMREAD_COLOR) # Load an image
    image2 = cv2.imread(image_path2, cv2.IMREAD_COLOR)

    
    while True:
        for img in [image,image2]:
            cv2.imshow('window', img) 
            key = cv2.waitKey(3000) # 3 second pause before switching images
            if key == 32:           # define space bar as a key to exit loop
                cv2.destroyAllWindows()
                break
        else:
            continue
        break


if __name__ == '__main__':
    main()