import ctypes
import os

def fun1():
    print("Hello world -- Python")

if __name__ == "__main__":
    # create a library from the referenced C-file to be accessed in the script
    os.system( "cc -fPIC -shared -o mixedCython.so mixedCython.c" )

    fun1()

    func = ctypes.CDLL( "./mixedCython.so" )
    
    func.add.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    func.greater.argtypes = [ctypes.c_int, ctypes.c_int]

    print( func.add(1, 2, 3) )
    print( func.greater( 3, 7) )


    
