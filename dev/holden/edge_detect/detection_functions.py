import argparse
import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi
import multiprocessing as mp
# _______________________________________________________ #

'''
This function retrieves the filename of an image from command line
    arguments. This is likely how images will get passed into the
    Python script, unless the final architecture ends up being less modular.

Accepts no parameters, only references shell environment for cmdline args
Returns a string filename pointing to the image to process
'''
def read_filename():
    args = argparse.ArgumentParser()
    args.add_argument( "--image", dest="image", action='store', type=str, required=False, help="path to input image" )
    
    args     = vars(args.parse_args())
    filename =  ""

    if args["image"]:
        filename = args["image"]

    return filename
    #ENDOF: read_filename()


'''
This function uses its string parameter to open and read a file storing processing
    parameters. Each line in the file stores a single parameter set in the following
    format:
        <gauss state>, <median state>, <low threshold>, <high threshold>

It needs only the valid string filename, and returns a 2D list, with each elem being
    a set of parameters for processing
'''
def compile_param_list( filename="param_refine_all3.txt" ):
    params = []

    with open(filename, "r") as file:
        for line in file:
            tmp = line.split()
            params.append( [int(tmp[0]), int(tmp[1])] )

    return params
    #ENDOF: compile_param_list()


'''
This function combines many other functions in this file. It accepts a filename
    pointing to an image to be processed, and preps it. This is then passed to
    a Canny edge detector with the specified thresholds. This output is then
    LIGHTLY blurred once more to join up individual edge contours that appear
    disjoint incorrectly. It is recast into a binary output (as the Gaussian blur
    will make it shades of grey), and returned.

It accepts the following parameters:
    lthresh  - int     - The low hysterisis threshold to use for Canny
    hthresh  - int     - The high hysterisis threshold to use for Canny
    L2       - boolean - L2 gradient for Canny...leave False
    filename - string  - path to image filename
'''


'''
This function implements edge detection and dimension measurement with a set of 
    processing parameters. Rather than taking one processed image in and running
    operations on it, it accepts a list of parameters (such as the result of 
    compile_param_list) along with an image filename. It then performs the image
    prep, the processing based on the passed-in parameters, and then measures 
    those outputs. It finally averages those results of measuring and returns.

Requires a string image filename parameter
Requires a 2D list of parameters with each element being a list formatted:
    <low thresh>, <high thresh>
'''
def find_measurements( img_filename, params ):
    # values to return
    height  = 0
    width   = 0
    tot     = 0

    # index constants
    LTHRESH    = 0
    HTHRESH    = 1
    HEIGHT_IND = 0
    WIDTH_IND  = 1

    # read image & filter for prep. As preprocessing is always the same, do not repeat
    img = cv2.GaussianBlur(cv2.imread( img_filename, cv2.IMREAD_GRAYSCALE ), [0, 0], 3, 0, cv2.BORDER_WRAP)
    for i in range(10):
        img = cv2.medianBlur(img, 7)

    # process image foreach set of parameters
    for line in params: 
        img_edges = cv2.Canny(img, line[HTHRESH], line[LTHRESH], 3, L2gradient=False)
        
        # light blur & re-binarize image to join up broken edge pixels
        img    = cv2.GaussianBlur(img, [3, 5], (1.0/3.0), 0, cv2.BORDER_WRAP)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
        
        # use inbuilt contour-locating fxn on input image object
        cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        dat  = [cv2.minAreaRect(elem) for elem in cnts if cv2.contourArea(elem) > 100]
        
        # if did not receive clear information, or multiple boxes found
            # could implement box combination, but not worth it as of right now
        if len( dat ) != 1:
            continue

        # retrieve bounding rect data from the list returned by orientation() and store
        height += dat[0][1][HEIGHT_IND]
        width  += dat[0][1][WIDTH_IND]
        tot    += 1

    # compute averages based on number of used param combinations
    height /= tot
    width  /= tot

    return height, width
    #ENDOF: find_measurements