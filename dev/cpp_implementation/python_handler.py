
import ctypes
import os

def fun1():
    print( "Hello World -- Python" )

if __name__ == "__main__":
    os.system( "g++ -fPIC -shared main_driver.cpp -o edge_detect -I /usr/local/include/opencv4 -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui" )
    fun1()

    func = ctypes.CDLL( "./edge_detect.so" )

