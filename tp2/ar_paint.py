# ---------------------------------------------------------
# TP2 - Augmented Reality Paint
# Python script to draw in AR
# Daniel Sousa Oliveira nº 89208
# PSR, November 2022.
# ---------------------------------------------------------

from time import *
from pprint import *
from copy import *
from math import *
from colorama import *
import numpy as np
import cv2
import argparse
import json

"""Define global variables for mouse coordinates and movement"""
mouse = False
fx,fy = -1,-1

def mouseHandler(event, x, y, flags, param):
    """Function to handle mouse clicks and movements
    Gathers mouse coordinates and handles events
    https://docs.opencv.org/4.x/db/d5b/tutorial_py_mouse_handling.html
    """

    global fx, fy, mouse

    if event == cv2.EVENT_MOUSEMOVE and mouse:

        fx = x
        fy = y

    elif event == cv2.EVENT_LBUTTONDOWN:

        mouse = True

    elif event == cv2.EVENT_LBUTTONUP:

        mouse = False

def getRanges(ranges, image_capture):
    """Function that uses RBG limits defined from color_segmentation.py
    Process image again to create a segmentation mask

    Parameters
    ----------
    ranges : dict
        RGB limits from color_segmentation.py
    image_capture : cv2.image
        Image collected from camera

    Returns
    -------
    image_processed : cv2.image
        Result of segmentation
    """

    mins = np.array([ranges['limits']['B']['min'], ranges['limits']['G']['min'], ranges['limits']['R']['min']])
    maxs = np.array([ranges['limits']['B']['max'], ranges['limits']['G']['max'], ranges['limits']['R']['max']])
    mask = cv2.inRange(image_capture, mins, maxs)
    mask = mask.astype(np.bool_)

    image_processed = deepcopy(image_capture)
    image_processed[np.logical_not(mask)] = 0

    return image_processed

def connectComponents(image_processed, image_capture):
    """Uses cv2 function connectedComponentsWithStats to label image objects
    Finds object with the biggest area, given the segmentation mask
    https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga107a78bf7cd25dec05fb4dfc5c9e765f

    Parameters
    ----------
    image_processed : cv2.image
        Result of segmentation
    image_capture : cv2.image
        Image collected from camera

    Returns
    -------
    image_capture : cv2.image
        New segmentation mask only with the greater area object
    """

    global fx, fy, mouse

    image_grey = cv2.cvtColor(image_processed, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image_grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)

    if num_labels > 1:
       
        max_area_Label = sorted([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(num_labels)], 
                                key=lambda x: x[1])[-2][0]

        mask = cv2.inRange(labels, max_area_Label, max_area_Label)
        mask = mask.astype(np.bool_)
        image_capture[mask] = (0, 255, 0)

        if not mouse:
            fx = int(centroids[max_area_Label, 0])
            fy = int(centroids[max_area_Label, 1])

    return image_capture

def drawLines(shake, video, painting, image_capture, color, thickness, current, ix, iy):
    """Function to draw lines on the white board
    Has shake detection feature that prevents wrong lines to be drawn
    Also has the feature to use captured images to draw, instead of the white board


    Parameters
    ----------
    shake : bool
        Flag to implement shake detection or not
    video : bool
        Flag to implement usage of captured images
    painting : np.array
        White board to draw in or captured image
    image_capture : cv2.image
        Captured image
    color : tuple
        Color to be used when drawing
    thickness : int
        Value of thickness to be used when drawing
    current : bool
        Flag to identify if the user is currently drawing
    ix : int
        Last mouse x coordinate saved when the mouse was pressed
    iy : int
        Last mouse y coordinate saved when the mouse was pressed

    Returns
    -------
    copy : np.array
        This copy of the white board will be gathering all the objects drawn
    image_capture : cv2.image
        Same captured image or result of the draw in the same image
    ix : int
        Last mouse x coordinate saved when the mouse was pressed
    iy : int
        Last mouse y coordinate saved when the mouse was pressed
    """
    
    global fx, fy, mouse

    if not current and ix != None and iy != None:
        
        if shake:
         
            dist = ((fx - ix) ** 2 + (fy - iy) ** 2) ** (1 / 2)
            
            if dist < 50:
                cv2.line(painting, (fx, fy), (ix, iy), color, thickness, cv2.LINE_4)
            else:
                cv2.line(painting, (fx, iy), (fx, fy), color, thickness, cv2.LINE_4)
        
        else:
            cv2.line(painting, (fx, fy), (ix, iy), color, thickness, cv2.LINE_4)

    ix = fx
    iy = fy
    copy = painting.copy()
    mask = None

    if video:
        
        mask = deepcopy(copy)
        mask = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
        mask = mask.astype(np.bool_)
        image_capture[mask] = (0, 0, 0)
        copy = cv2.add(image_capture.astype(np.uint8), copy.astype(np.uint8))

    return copy, image_capture, ix, iy

def drawFigures(char, painting, color, thickness, current, ellipsquare, vertices):
    """Function to draw ellipses or squares, depending on the key pressed

    Parameters
    ----------
    char : char
        Identify if the user wants to draw a ellipse or a square
    painting : np.array
        White board to draw in or captured image
    color : tuple
        Color to be used when drawing
    thickness : int
        Value of thickness to be used when drawing
    current : bool
        Flag to identify if the user is currently drawing
    ellipsquare : bool
        Flag to define if a ellipse or a square is being drawn
    vertices : array
        Vertices of square or diameter points of ellipse, to draw

    Returns
    -------
    painting : np.array
        Result of the draw on the white board or captured image
    current : bool
        Flag to identify if the user is currently drawing
    ellipsquare : bool
        Flag to define if a ellipse or a square is being drawn
    vertices : array
        Vertices of square or diameter points of ellipse, to draw
    """

    global fx, fy

    if not current:

        vertices[0] = fx
        vertices[1] = fy
        current = True

    elif char == 'e':

        current = False
        vertices = [0,0,0,0]
        ellipsquare = False

        print(Style.BRIGHT + Fore.YELLOW + 'Selected Ellipse' + Style.RESET_ALL)
        cv2.circle( painting, (int((fx + vertices[0]) / 2), 
                    int((fy + vertices[1]) / 2)),
                    int(sqrt((pow(((vertices[0]-fx) / 2), 2)) + 
                    pow(((vertices[1]-fy) / 2), 2))), color, thickness)

    elif char == 's':

        current = False
        vertices = [0,0,0,0]
        ellipsquare = True

        print(Style.BRIGHT + Fore.YELLOW + 'Selected Rectangle' + Style.RESET_ALL)
        cv2.rectangle(painting, (vertices[0],vertices[1]), (fx, fy), color, thickness)

    return ellipsquare, current, vertices, painting

def visualizeDrawing(current, ellipsquare, copy, vertices, color, thickness):
    """Function to make a visual representation of the possible figures to draw,
    before actually drawing them

    Parameters
    ----------
    current : bool
        Flag to identify if the user is currently drawing
    ellipsquare : bool
        Flag to define if a ellipse or a square is being drawn
    copy : np.array
        Copy of the white board with all the objects drawn
    vertices : array
        Vertices of square or diameter points of ellipse, to draw
    color : tuple
        Color to be used when drawing
    thickness : int
        Value of thickness to be used when drawing

    Returns
    -------
    copy : np.array
        Copy of the white board with all the objects drawn
    vertices : array
        Vertices of square or diameter points of ellipse, to draw
    """

    global fx, fy

    if current:
        vertices[2] = fx
        vertices[3] = fy

        if ellipsquare:
            cv2.rectangle(copy, (vertices[0],vertices[1]), 
                                (vertices[2],vertices[3]), color, thickness)
        else:
            cv2.circle(copy, (int((vertices[0]+vertices[2]) / 2), 
                              int((vertices[1]+vertices[3]) / 2)),
                              int(sqrt((pow(((vertices[2]-vertices[0]) / 2), 2)) 
                              + pow(((vertices[3]-vertices[1]) / 2), 2))), color, thickness)

    return copy, vertices

def changeColor(char):
    """Function to change the color to be used when drawing

    Parameters
    ----------
    char : char
        Represents the color to use

    Returns
    -------
    color : tuple
        New color to draw with
    """

    color = (0,0,0)

    if char == 'r':
        color = (0, 0, 255)
        print(Style.BRIGHT + Fore.RED + 'Selected red color' + Style.RESET_ALL)

    if char == 'g':
        color = (0, 255, 0)
        print(Style.BRIGHT + Fore.GREEN + 'Selected green color' + Style.RESET_ALL)

    if char == 'b':
        color = (255, 0, 0)
        print(Style.BRIGHT + Fore.BLUE + 'Selected blue color' + Style.RESET_ALL)
    

    return color

def changeThickness(char, thickness):
    """Function to change the thickness to be used when drawing
    Has max and min values for thickness

    Parameters
    ----------
    char : char
        Represents increase or decrease action
    thickness : int
        Current value of thickness

    Returns
    -------
    thickness: int
        New value of thickness
    """

    if char == '+' and thickness < 25:
        print(Style.BRIGHT + Fore.WHITE +
        'Decreasing thickness' + Style.RESET_ALL)
        thickness += 1

    if char == '-' and thickness > 0:
        print(Style.BRIGHT + Fore.WHITE +
        'Increasing thickness' + Style.RESET_ALL)
        thickness -= 1

    print(Style.BRIGHT + Fore.RED + 
    'Limit of thickness reached' 
    + Style.RESET_ALL)

    return thickness

def writeImage(image):
    """Function to save the image on a .jpg file

    Parameters
    ----------
    image : cv2.image
        Final result of the drawing to be saved
    """

    name = str(ctime(time()))
    cv2.imwrite(name + '.jpg', image)

    print(Style.BRIGHT + Fore.WHITE + 'Saved image' + Style.RESET_ALL)

def boardCleaner(flag, height, width):
    """Function to clean the white board or image capture

    Parameters
    ----------
    flag : bool
        Flag to identify if a white board or a capture is being used
    height : int
        Board/Capture height
    width : int
        Board/Capture height

    Returns
    -------
    painting : np.array
        Result of the draw on the white board or captured image
    """

    if flag:
        painting = np.zeros((height, width, 3))
    else:
        painting = np.ones((height, width, 3)) * 255

    print(Style.BRIGHT + Fore.WHITE + 'Cleared image' + Style.RESET_ALL)
    
    return painting

def main():
    """Initialization of neeeded variables
    Define argument parser to open the file as usage: ar_paint.py [-h] -j -usp -uvs
    Opens opencv windows and starts capturing images
    """

    global fx, fy, mouse
    color = (255,0,0)
    thickness = 1
    current = False
    ix, iy = None, None
    vertices = [0,0,0,0]
    ellipsquare = False


    parser = argparse.ArgumentParser(description='Definition of test mode')
    parser.add_argument('-j', '--json', type=str, 
    help='Full path to json file.')
    parser.add_argument('-usp', '--use_shake_prevention', action='store_true', 
    help='Detects significant fluctuations while finding the segment centroid')
    parser.add_argument('-uvs', '--use_video_stream', action='store_true',
    help='Uses images captured periodically by the camera')
    args = vars(parser.parse_args())

    file_name = args['json']    
    if not args['json']:
        file_name = 'limits.json'

    video = args['use_video_stream']  
    if not args['use_video_stream']:
        video = False
    
    shake = args['use_shake_prevention']  
    if not args['use_shake_prevention']:
        shake = True

    with open(file_name) as f:
        ranges = json.load(f)

    print(Style.BRIGHT + Fore.GREEN + "PSR TP2 - Augmented Reality Paint \n" + Style.RESET_ALL)
    print(Fore.RED + "  Red line color (press r)" + Style.RESET_ALL)
    print(Fore.GREEN + "  Green line color (press g)" + Style.RESET_ALL)
    print(Fore.CYAN + "  Blue line color (press b)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Increase line thickness (press +)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Decrease line thickness (press -)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Clear board (press c)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Capture image (press w)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Draw square (press s)" + Style.RESET_ALL)
    print(Fore.YELLOW + "  Draw ellipse (press e)" + Style.RESET_ALL)
    print(Fore.RED + "  Quit program (press q)" + Style.RESET_ALL)

    window1 = "Augmented Reality Paint"
    window2 = "Mask"
    window3 = "Video Capture"

    cv2.namedWindow(window1, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window3, cv2.WINDOW_NORMAL)

    cv2.resizeWindow(window1, (800, 800))
    cv2.resizeWindow(window2, (800, 800))
    cv2.resizeWindow(window3, (800, 800))

    capture = cv2.VideoCapture(0)
    _, image_capture = capture.read()
    height, width, _ = image_capture.shape

    if video:
        painting = np.zeros((height, width, 3))
        cv2.imshow(window1, image_capture)
    else:
        painting = np.ones((height, width, 3)) * 255
        cv2.imshow(window1, painting)
        
    cv2.setMouseCallback(window1, mouseHandler)
    cv2.imshow(window2, image_capture)

    """Execution will constantly update the board/image with drawing
    "Switch" used to handle key pressing and define actions
    """

    while True:

        if video:
            cv2.imshow(window1, image_capture)
        else:
            cv2.imshow(window1, painting)

        _, image_capture = capture.read()
        image_capture = cv2.flip(image_capture, 1)
        

        image_processed = getRanges(ranges, image_capture)

        cv2.imshow(window3, image_processed)

        image_capture = connectComponents(image_processed, image_capture)

        cv2.imshow(window2, image_capture)

        copy, image_capture, ix, iy = drawLines(shake, 
                                            video, painting, image_capture, 
                                            color, thickness, current, ix, iy)
       
        copy, vertices = visualizeDrawing(current, ellipsquare, copy, vertices, color, thickness)
        
        cv2.imshow(window1, copy)

        key = cv2.waitKey(20)

        if key != -1:

            print(Style.BRIGHT + Fore.YELLOW + "Key:" + chr(key) + Style.RESET_ALL)
            
            if key == ord('r'):
                
                color = changeColor('r')

            elif key == ord('g'):
                
                color = changeColor('g')

            elif key == ord('b'):
                
                color = changeColor('b')
            
            elif key == ord('w'):

                writeImage(painting)  
            
            elif key == ord('c'):

                painting = boardCleaner(video, height, width)
            
            elif key == ord('+'):

                thickness = changeThickness('+', thickness)
          
            elif key == ord('-'):

                thickness = changeThickness('-', thickness)

            elif key == ord('e'):

                ellipsquare, current, vertices, painting = drawFigures('e', 
                painting, color, thickness, current, ellipsquare, vertices)

            elif key == ord('s'):

                ellipsquare, current, vertices, painting = drawFigures('s', 
                painting, color, thickness, current, ellipsquare, vertices)
      
            elif key == ord('q'):

                print(Style.BRIGHT + Fore.RED + " \n End of session" + Style.RESET_ALL)
                break

    cv2.destroyAllWindows()
    capture.release()

if __name__ == '__main__':
    main()