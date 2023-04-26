from argparse import ArgumentParser
from cv2 import imread, Canny, GaussianBlur, threshold, namedWindow, drawContours, \
     findContours, minAreaRect, contourArea, boxPoints, medianBlur, waitKey,       \
     imshow, destroyAllWindows, BORDER_WRAP, CHAIN_APPROX_SIMPLE, THRESH_BINARY,   \
     RETR_EXTERNAL, WINDOW_NORMAL
from numpy import ndarray, int0
from math import atan2, cos, sin, sqrt, pi
from operator import methodcaller
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
def measure_single(img_obj: ndarray, param_list: list[int], low_rect_area: int=100000) -> list[float]:
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
            drawContours(img_edges, [int0(boxPoints(d))], 0, (255, 255, 0), 2)

            imshow(f"{param_list[1]} {param_list[0]} Box", img_edges)
            waitKey(0)
            destroyAllWindows()
    
    if len( dat ) == 0: return [0, 0]

    '''
        if there are multiple results, there are a few main reasons:
            Not enough filtering was done, and some interior boxes aroung
                spots are being identified
            The main outline is/was not identified fully, rather it is across
                two or more boxes
            The main outline was not identified at all

        With properly tuned parameters, cases 2 and 3 should not really occur.
            If possible, want to return 0 iff case 2 or 3 is detected...
                case 2 if box endpoints are within a certain tolerance of each
                other, etc

            Other parameter sets should work, so can ignore one or two
                sets without much worry

        Test for areas of bounding boxes that are within a certain tolerance...
            Spots and broken areas should represent relatively similar areas,
                but the overall bounding box should be significantly larger than
                all other boxes.

    '''

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

    # read image & filter for prep
    img: ndarray = GaussianBlur(imread( img_filename ), [0, 0], 3, 0, BORDER_WRAP)
    for i in range(10): img = medianBlur(img, 7)

    
    # process image foreach set of parameters
    for line in params: 
        h, w    = measure_single(img, line, prnt)
        height += (w != 0) * h
        width  += (h != 0) * w
        tot    += ((h != 0) and (w != 0))
    return height / tot, width / tot
    #ENDOF: find_measurements()

