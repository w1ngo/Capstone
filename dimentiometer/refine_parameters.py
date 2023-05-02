import cv2
import detection_functions as funcs
import random

'''
This serves to perform the refining process with multiple images
    rather than a single image. This was attempted before, but
    after the initial pass, parameters were compared based on
    their performance on a single image only. This will allow
    each param set to be used on each image, and rejected if
    they fail on ANY.
'''
def multi_refine(filename_ls):
    param_file = "param_refine.txt"
    
    for idx, img_filename in enumerate(filename_ls):
        with open(param_file, "r") as file:
            params = [ [int(line[0]), int(line[1])] for line in list(map(methodcaller("split"), file)) ]

        # open a new file to track accepted param pairs
        file = open( f"param_refine_{idx}.txt", "w" )
        file.close()

        # using each set of parameters read from the master file,
            # find the edges of the image at <filename> and determine
            # if the parameter pair is good or not (write to file iff yes)
        for pair in params:
            img = funcs.edge_detect( True, True, pair[0], pair[1], False, img_filename )
            cv2.namedWindow( f"{pair[0]} {pair[1]}", cv2.WINDOW_NORMAL )
            cv2.imshow( f"{pair[0]} {pair[1]}", img )
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

            # If this param pair is accepted, open current file and record
            if input("y for yes, n for no: ") == 'y':
                file = open( f"param_refine_{idx}.txt", "a+" )
                file.write( f"{pair[0]} {pair[1]}\n" )
                file.close()

        param_file = f"param_refine_{idx}.txt"
        print( f"Pass with image at {img_filename} complete.\n\n" )
    print( "Refining completed" )
