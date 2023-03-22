from argparse import ArgumentParser
from cv2 import imread, Canny, GaussianBlur, threshold, namedWindow, drawContours, \
     findContours, minAreaRect, contourArea, boxPoints, medianBlur, waitKey,       \
     imshow, destroyAllWindows, BORDER_WRAP, CHAIN_APPROX_SIMPLE, THRESH_BINARY,   \
     RETR_EXTERNAL, WINDOW_NORMAL
from numpy import ndarray, int0
from math import atan2, cos, sin, sqrt, pi
from operator import methodcaller
from scipy import stats
from multiprocessing import Pool
from functools import partial
# _______________________________________________________ #

'''
This function retrieves the filename of an image from command line
    arguments. This is likely how images will get passed into the
    Python script, unless the final architecture ends up being less modular.

Accepts no parameters, only references shell environment for cmdline args
Returns a string filename pointing to the image to process
'''
def read_filename() -> str:
    args = ArgumentParser()
    args.add_argument( "--image", dest="image", action='store', type=str, required=False, help="path to input image" )
    
    args     = vars(args.parse_args())
    filename =  ""

    if args["image"]: filename = args["image"]

    return filename
    #ENDOF: read_filename()


'''
This function uses its string parameter to open and read a file storing processing
    parameters. Each line in the file stores a single parameter set in the following
    format: <low threshold>, <high threshold>

This function is used to gather the parameter pairs for usage in the processing functions
below. This avoids the need for hardcoding a list into the script somewhere, and allows
for easy training & retraining, etc.

It accepts one parameter, a string filename that is assumed to be valid.
The file referenced is required to be in a specific format:
    - There is no data in the file other than parameter pairs
    - Each line in the file represents one and only one parameter pair
    - The two parameters in each line are separated by a comma
    - The first parameter on each line is the low threshold
    - The second parameter on each line is the second threshold

There is a default parameter that references a known proper file if one is not provided.

It returns a 2D list of integers, with each 1D list being a low/high pair
'''
def compile_param_list( filename: str="param_refine_all3.txt" ) -> list[list[int]]:
    # opens file, makes param pair from each line, converts that line into integers
    with open(filename, "r") as file: return [ [int(line[0]), int(line[1])] for line in list(map(methodcaller("split"), file)) ]
    #ENDOF: compile_param_list()

    
'''
This function is meant to improve accuracy by applying statistical analysis
    to the measured heights and widths from the measurmenet functions. Ideally,
    this will do nothing. It will remove outliers should they exist, and return
    the average of the remaining points (treating height and width differently)

It accepts one parameter, a 2D list of height-width pairs

It returns a pair of floats representing the average of
    the input heights and widths, with z-score based outliers
    disregarded
'''
def filter_measurements( pairs: list[int] ) -> (float, float):
    '''
    TODO: Want to add in high/low thresholds...do this on
        the pixel side or centimeter side? Will be easier
        to put support in for centimeter side
    '''

    # compute zscores of heights and widths to filter outliers
    count:  int = 0
    height: int = 0
    width:  int = 0
    sz:     int = len(pairs)

    heights: list[int] = [0] * sz
    widths:  list[int] = [0] * sz

    for i, pair in enumerate(pairs):
        heights[i] = pair[0]
        widths[i]  = pair[1]

    height_zscore:list[int] = stats.zscore(heights)
    width_zscore: list[int] = stats.zscore(widths)

    for i in range(sz):
        if (abs(height_zscore[i]) < 3) and (abs(width_zscore[i]) < 3):
            count  += 1
            height += heights[i]
            width  += widths[i]

    if count == 0:
        print("no valid data detected")
        return 0, 0

    return (height / count), (width / count)
    #ENDOF: filter_measurements()


'''
This function executes the potato measurement procedure on a single image with a single parameter pair
It simplifies the find_measurements() function below by reducing the amount of code within, and this
allows for clearer testing and debugging.

It requires a prepped image (i.e., Gaussian and median blurs already applied) as an object
it requires a list of 2 integers, namely the low Canny threshold and the high threshold
it has an optional "prnt" parameter to display debug output
it has an optional "low_rect_area" parameter to specify the minimum areas to consider as
    possibly potatoes

It returns a pair of floats (height, width)
'''
def measure_single(img_obj: ndarray, param_list: list[int], low_rect_area: int=1000) -> list[float]:
    # pass prepped image into Canny with the specified threshold params
    img_edges: ndarray = Canny(img_obj, param_list[1], param_list[0], 3, L2gradient=False)
    
    # light blur & re-binarize image to join up broken edge pixels
    img_edges: ndarray = GaussianBlur(img_edges, [3, 5], (1.0/3.0), 0, BORDER_WRAP)
    _, img_edges = threshold(img_edges, 0, 255, THRESH_BINARY)
    
    # use inbuilt contour-locating fxn on input image object
    cnts = findContours(img_edges, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    dat  = [minAreaRect(elem) for elem in cnts if contourArea(elem) > low_rect_area]

    # print outline and bounding box if desired
    if False:
        for d in dat:     
            window = namedWindow(f"{param_list[1]} {param_list[0]} Box", WINDOW_NORMAL)
            drawContours(img_edges, [int0(boxPoints(d))], 0, (255, 255, 255), 2)

            imshow(f"{param_list[1]} {param_list[0]} Box", img_edges)
            waitKey(0)
            destroyAllWindows()
    
    if len( dat ) != 1: return [0, 0]

    return [dat[0][1][0], dat[0][1][1]]
    #ENDOF: measure_single()


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
It allows an optional "prnt" parameter for including debug output

It returns a pair of floats (height, width)
'''
def find_measurements( img_filename: str, params: list[list[int]], prnt: bool=False) -> (float, float):
    # values to return
    height: int = 0
    width:  int = 0
    tot:    int = 0

    # read image & filter for prep. As preprocessing is always the same, do not repeat
    img: ndarray = GaussianBlur(imread( img_filename ), [0, 0], 3, 0, BORDER_WRAP)
    for i in range(10): img = medianBlur(img, 7)

    '''
    # process image foreach set of parameters
    for line in params: 
        h, w    = measure_single(img, line, prnt)
        height += h
        width  += w
        tot    += ((h != 0) and (w != 0))
    '''
    return filter_measurements( [ measure_single(img, line) for line in params ] )
    #ENDOF: find_measurements()


def find_measurements2( img_filename: str, params: list[list[int]], prnt: bool=False ) -> (float, float):
    height: int = 0
    width:  int = 0
    tot:    int = 0

    # read image & filter for prep. As preprocessing is always the same, do not repeat
    img: ndarray = GaussianBlur(imread( img_filename ), [0, 0], 3, 0, BORDER_WRAP)
    for i in range(10): img = medianBlur(img, 7)
    with Pool() as p: return filter_measurements( list(p.imap(partial(measure_single, img), params)) )
