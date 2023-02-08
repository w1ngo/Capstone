import subprocess
import ctypes


def process_img( c_obj, filename, lthresh, hthresh, gauss, median ):
    return c_obj.process_image( filename, gauss, median, lthresh, hthresh )


if __name__ == "__main__":
#    subprocess.call( "g++ -fPIC -shared main_driver.cpp -o edge_detect.so -I /usr/local/include/opencv4 -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui", shell=True )
#    subprocess.call( "g++ -fPIC -shared edge_detection_functions.h -o edge_detect.so -I /usr/local/include/opencv4 -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui", shell=True )
    print( "compiled successfully" )

    clib = ctypes.CDLL( "./edge_detect.so" )
    print( "referenced shared library" )
    
    print( type(clib) )
    print( clib )
    
    clib.process_image.argtypes = [ ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.c_int, ctypes.c_int ]
    
    mat = process_img( clib, "./images/isolated_potato.jpg", 75, 200, True, True )

    print( "Sucessfully called cpp function from python handler" )

