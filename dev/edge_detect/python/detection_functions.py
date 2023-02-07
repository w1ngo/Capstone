import argparse
import cv2
import numpy as np
from math import atan2, cos, sin, sqrt, pi

def read_filename():
    args = argparse.ArgumentParser()
    args.add_argument( "--image", dest="image", action='store', type=str, required=False, help="path to input image" )
    args = vars(args.parse_args())

    if args["image"]:
        filename = args["image"]

    return filename

def prep_img( img, gauss, median ):
    if gauss:
        img = cv2.GaussianBlur( img, [0, 0], 3, 0, cv2.BORDER_WRAP )

    if median:
        for i in range(10):
            img = cv2.medianBlur( img, 7 )

    return img


def execute( gauss, median, lthresh, hthresh, L2, filename ):
    img = prep_img( cv2.imread( filename, cv2.IMREAD_GRAYSCALE ), gauss, median )
    return cv2.Canny( img, hthresh, lthresh, 3, L2gradient=L2 )


def draw_axis(img, p_, q_, color, scale):
    p = list(p_)
    q = list(q_)

    angle = atan2( p[1] - q[1], p[0] - p[0] )
    hypo  = sqrt( (p[1] - q[1]) ** 2 + (p[0] - q[0]) ** 2 )

    # lengthen hypotenuse
    q[0] = p[0] - scale * hypo * cos(angle)
    q[1] = p[1] - scale * hypo * sin(angle)
    cv.line(img, (int(p[0])), (int(p[1])), (int(q[0])), (int(q[1])), color, 3, cv.LINE_AA)
'''
    # create arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv.line(img, (int(p[0])), (int(p[1])), (int(q[0])), (int(q[1])), color, 3, cv.LINE_AA)
    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
   cv.line(img, (int(p[0])), (int(p[1])), (int(q[0])), (int(q[1])), color, 3, cv.LINE_AA)
'''


def orientation( img, technique ):
    if technique == 1:
        coords = np.column_stack( np.where( img > 0 ) )
        angle = cv2.minAreaRect(coords)[-1]
        angle = (-1 * (90 - angle)) if (angle < -45) else (-1 * angle)
        print( f"angle computed: {angle}" )

    elif technique == 2:
        print( "test using technique one, technique two not complete yet" )

    else:
        print( "Unrecognized orientation technique requested" )
