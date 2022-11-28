from pyzbar import pyzbar
from PIL import Image
import cv2


'''
This function takes an image as input and detects & interprets a barcode
    It has the ability to draw the detected barcode, and will print
    both the type and data stored within
'''
def decode( image ):
    objects = pyzbar.decode( image )
    for obj in objects:
        print( "detected barcode: ", obj )
        image2 = draw_barcode( obj, image )
        print( f"Type: {obj.type}" )
        print( f"Data: {obj.data}" )
        print()
        return image2

    return image
    #ENDOF: func


if __name__ == "__main__":
    fnames = [ "barcode1.png" ]

    for file in fnames:
        image  = cv2.imread( file )

        # preprocessing image
        # ret, bw_im = cv2.threshold( image, 127,255, cv2.THRESH_BINARY )
        
        image2 = decode( image )

        cv2.imshow( "processed image", image2 )

