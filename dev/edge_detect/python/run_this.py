import cv2
import detection_functions as funcs
import refine_parameters   as refine
import random

if __name__ == "__main__":
    ls = []
    data = []

    '''
    filename1 = r"/home/wingo/work/capstone_main/dev/edge_detect/python/images/isolated_potato.jpg"
    filename2 = r"./images/isolated_potato2.jpg"
    filename3 = r"./images/isolated_potato3.png"
    '''
    filename1 = r".\images\isolated_potato.jpg"
    filename2 = r".\images\isolated_potato2.jpg"
    filename3 = r".\images\isolated_potato3.png"

    '''
    _, data = refine.refine( [filename1] )

    img = funcs.execute( True, True, 11, 71, False, filename1 )
    #img = cv2.imread(filename1, cv2.IMREAD_GRAYSCALE)
    funcs.orientation( img )

    img = funcs.execute( True, True, 11, 71, False, filename2 )
    #img = cv2.imread(filename2, cv2.IMREAD_GRAYSCALE)
    funcs.orientation( img )

    img = funcs.execute( True, True, 11, 71, False, filename3 )
    #img = cv2.imread(filename3, cv2.IMREAD_GRAYSCALE)
    funcs.orientation( img )
    '''

    params = funcs.compile_param_list("param_refine.txt")

    height, width = funcs.find_measurements(filename1, params)
    print( f"Height: {height}, Width: {width}" )

    height, width = funcs.find_measurements(filename2, params)
    print( f"Height: {height}, Width: {width}" )

    height, width = funcs.find_measurements(filename2, params)
    print( f"Height: {height}, Width: {width}" )

