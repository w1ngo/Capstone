import detection_functions  as detect
import peripheral_functions as periph
import refine_parameters    as refine
from sys import platform
from time import perf_counter

if __name__ == "__main__":
    
    if platform == "linux" or platform == "linux2":
        filenames = [ r"./images/isolated_potato.jpg",  \
                      r"./images/isolated_potato2.jpg", \
                      r"./images/isolated_potato3.png", \
                      r"./images/IMG_4011.jpg",         \
                      r"./images/IMG_4012.jpg",         \
                      r"./images/IMG_4013.jpg" ]

    inp = input("Enter r to refine parameter options, t test edge detection as-is, or f for a full trial: ")

    if inp in ("R", "r"):
        _, data = refine.multi_refine( [filename1, filename2, filename3] )

    elif inp in ("T", "t"):
        params = detect.compile_param_list()
        [print(f"Potato at <{filenames[i]:<29}> pixel dims: {elem[0]:<18} x {elem[1]:<18}") \
         for i, elem in enumerate( list(map(lambda file : detect.find_measurements(file, params, disp), filenames)) )  \
         if elem[0] != 0]

    else:
        params = detect.compile_param_list()
        if input( "Mount USB? [Y/n]: " ) in ("Y", "y"): periph.mount_usb()

        if input( "Load in an existing spreadsheet (1) or create a new one (2)" ) == "1":
            pass

        if input("Press enter when ready to capture images"):
            periph.take_pic(1)
            periph.take_pic(2)
            
            print("Images stored at img1.jpg and img2.jpg" )

            meas_1 = detect.find_measurements("img1.jpg", params, False)
            meas_2 = detect.find_measurements("img2.jpg", params, False)
            
            '''
            subprocess.Popen( "feh img1.jpg".split() )
            subprocess.Popen( "feh img2.jpg".split() )
            '''

            print( "Measurements from one camera: {meas_1[0]} x {meas_1[1]}" )
            print( "Measurements from other cam : {meas_2[0]} x {meas_2[1]}" )

            h = int(input( "What is the height (cm) of the potato? "))
            w = int(input( "What is the width (cm) of the potato? "))
            l = int(input( "What is the length (cm) of the potato? "))

            # match the shared param between each cam (or ID, and choose longest)
            # generate conversion factor from pixels to cm
                # sample over a number of trials...record data to a .csv for analysis
            # so this needs to turn into a for-loop
            # also, add in ability to say yes/no for proper analysis

