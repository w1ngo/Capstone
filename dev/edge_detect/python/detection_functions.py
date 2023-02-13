import argparse
import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi
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
    args = vars(args.parse_args())

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
def compile_param_list( filename ):
    params = []

    with open("param_refine.txt", "r") as file:
        for line in file:
            tmp = line.split()
            params.append( [True, True, int(tmp[0]), int(tmp[1])] )

    return params
    #ENDOF: compile_param_list()


'''
This function preps an image for processing using an image object, as well as two
    state variables. The gauss param directs whether or not to use a Gaussian blur
    (should likely always be true), and the median param directs whether or not to
    use a median filter (for our potato application, this is vital).

It returns an image object that has been properly filtered and can be passed for edge
    detection
'''
def prep_img( img, gauss, median ):
    if gauss:
        img = cv2.GaussianBlur( img, [0, 0], 3, 0, cv2.BORDER_WRAP )

    if median:
        for i in range(10):
            img = cv2.medianBlur( img, 7 )

    return img
    #ENDOF: prep_img()


'''
This function combines many other functions in this file. It accepts a filename
    pointing to an image to be processed, and preps it. This is then passed to
    a Canny edge detector with the specified thresholds. This output is then
    LIGHTLY blurred once more to join up individual edge contours that appear
    disjoint incorrectly. It is recast into a binary output (as the Gaussian blur
    will make it shades of grey), and returned.

It accepts the following parameters:
    gauss    - boolean - Whether or not to prep with a gaussian filter
    median   - boolean - Whether or not to prep with a median filter
    lthresh  - int     - The low hysterisis threshold to use for Canny
    hthresh  - int     - The high hysterisis threshold to use for Canny
    L2       - boolean - L2 gradient for Canny...leave False
    filename - string  - path to image filename
'''
def edge_detect( gauss, median, lthresh, hthresh, L2, filename ):
    img = prep_img( cv2.imread( filename, cv2.IMREAD_GRAYSCALE ), gauss, median )
    img = cv2.Canny( img, hthresh, lthresh, 3, L2gradient=L2 )
    
    # an additional GaussianBlur joins together edge separations
    img = cv2.GaussianBlur(img, [3, 5], (1.0/3.0), 0, cv2.BORDER_WRAP)
    
    # applying a threshold puts the picture back into a binary pixel domain
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return img
    #ENDOF: edge_detect()


'''
Function used to detect the orientation & measurements for an edge-detected
    image.

It accepts one edge-detected image object as a parameter.

It returns a 2D list, with each element being a 3-elem list
    of information on each contour detected.
        Elem one is a pair of coordinates for the centerpoint of the bounding rect.
        Elem two is a pair of measurements for height & width of the bounding rect.
        Elem three is the angle to which the bounding rect is askew.
'''
def orientation( img, debug_print=False ):        
    data = []
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    ret = []
    
    for cnt in cnts:
        if cv2.contourArea(cnt) < 10000:
            continue
           
        rect = cv2.minAreaRect(cnt)

        if debug_print:
            box = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(img, [box], 0, (255,255,255), 3)
            cv2.namedWindow("Box drawn", cv2.WINDOW_NORMAL)
            cv2.imshow( "Box drawn", img )
            cv2.waitKey(0)
            
        ret.append( rect )

    return ret
    #ENDOF: orientation()


'''
This function uses the orientation function with a set of processing parameters.
    Rather than taking one processed image in and running orientation on it,
    it accepts a list of parameters (such as the result of compile_param_list)
    along with an image filename. It then averages the results of measuring
    the image edges produced as output from each set of parameters, and returns
    both the average height and average width

Requires a string image filename parameter
Requires a 2D list of parameters with each element being a list formatted:
    <gauss>, <median>, <low thresh>, <high thresh>
'''
def find_measurements( img_filename, params ):
    height  = 0
    width   = 0
    
    GAUSS   = 0
    MEDIAN  = 1
    LTHRESH = 2
    HTHRESH = 3

    HEIGHT_IND = 0
    WIDTH_IND  = 1

    for line in params:
        img = edge_detect( line[GAUSS], line[MEDIAN], line[LTHRESH], line[HTHRESH], False, img_filename )
        dat = orientation( img )

        if len( dat ) == 0:
            continue

        if len( dat ) > 1:
            print( "Multiple bounding boxes located, handle separately..." )
            return 0, 0

        print( dat )
        dat = dat[0]
        print( dat )
        height += dat[1][HEIGHT_IND]
        width  += dat[1][WIDTH_IND]

    height /= len(params)
    width  /= len(params)

    return height, width
    #ENDOF: find_measurements
