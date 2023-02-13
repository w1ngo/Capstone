import cv2
import detection_functions as funcs
import random


'''
This function is meant to train a dataset of useful parameters. There are a large
    number of possible param combos to use for edge detection, but most are not
    useful. The process of paring down potential candidate sets is time-intensive
    but useful.

It can accept a list of filenames, or a single filename, meant to point at an image
    of a potato.

The initial pass is a simple yes/no. It shows the result of the image processed under
    a specific set of parameters, and either stores the param pair or skips it.

After that, it moves onto comparisons between two sets. The better pair can be chosen,
    or both pairs can be stored if they perform well (additionally both can be removed,
    but this should not occur after the initial pass)
    
    This process happens recursively, shuffling the order after each pass, until
    the total # of param sets falls at or below 10.
'''
def refine(filenames, init_param_file="param_refine.txt"):
    ls     = []
    data   = []
    params = []

    # read in desired parameters from the master file
    # one pair (low, high) is located on each line of the file
    with open(init_param_file, "r") as file:
        for line in file:
            tmp = line.split()
            params.append( [int(tmp[0]), int(tmp[1])] )

    if type(filenames) is list:
        # using each set of parameters read from the master file,
            # find the edges of the images at <filenames> and determine
            # if the parameter pair is good or not (write to file iff yes)
        for pair in params:
            for filename in filenames:
                img = funcs.edge_detect( True, True, pair[0], pair[1], False, filename )
                cv2.namedWindow( f"{pair[0]} {pair[1]}", cv2.WINDOW_NORMAL )
                cv2.imshow( f"{pair[0]} {pair[1]}", img )
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

            if input("y for yes, n for no: ") == 'y':
                ls.append( img )
                data.append( [pair[0], pair[1]] )
                
                file = open( f"param_refine_1.txt", "a+" )
                file.write( f"{pair[0]} {pair[1]}\n" )
                file.close()
            
    else:

        # open a new file, and put the path to the image being used on
            # the top line, then close
        file = open( f"param_refine_1_{filename}.txt", "w" )
        file.write(f"Image processed: {filename}\n")
        file.close()

        # using each set of parameters read from the master file,
            # find the edges of the image at <filename> and determine
            # if the parameter pair is good or not (write to file iff yes)
        for pair in params:
            img = funcs.edge_detect( True, True, pair[0], pair[1], False, filename )
            cv2.namedWindow( f"{pair[0]} {pair[1]}", cv2.WINDOW_NORMAL )
            cv2.imshow( f"{pair[0]} {pair[1]}", img )
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

            if input("y for yes, n for no: ") == 'y':
                ls.append( img )
                data.append( [pair[0], pair[1]] )
                file = open( f"param_refine_1_{filename}.txt", "a+" )
                file.write( f"{pair[0]} {pair[1]}\n" )
                file.close()

    print( "\tInitial pass complete, running through again now" )

    # shuffle the order of elements in the list for the comparison stage
    tmp = list( zip(ls, data) )
    random.shuffle( tmp )
    ls, data = zip( *tmp )
    ls = list(ls)
    data = list(data)

    # send to the recursive function to compare param sets 1-on-1
    return refine_recurs( ls, data )

'''
This is the recursvie stage of the main refine() function
'''
def refine_recurs(ls = [], data = []):
    # base case
    if len(ls) <= 10:
        return ls, data

    # open a new file, labeled with the number of parameter pairs present
        # at the time of the fxn call, in order to track process instead of
        # simply overwriting
    file = open( f"param_refine_len{len(ls)}.txt", "w" )
    file.close()
    
    for idx in range( len(ls) - 1 ):
        # this line prevents out-of-bounds caused by the list shrinking during
            # operation
        if idx == len(ls):
            break

        # show two images to the user for visual comparison, close on keypress
        cv2.namedWindow( "1", cv2.WINDOW_NORMAL )
        cv2.namedWindow( "2", cv2.WINDOW_NORMAL )
        cv2.imshow( "1", ls[idx    ] )
        cv2.imshow( "2", ls[idx + 1] )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        choice = int(input("1 is better, 2 is better, 3 undecided, 4 neither: "))

        # have to check for removing second list item first due to re-indexing after pop
        if choice & 2 == 0:
            ls.pop( idx + 1 )
            data.remove( data[idx + 1] )
        else:
            file = open( f"param_refine_len{len(ls)}.txt", "a+" )
            file.write( f"{data[idx][0]} {data[idx][1]}\n" )
            file.close()

        if choice & 1 == 0:
            ls.pop( idx )
            data.remove( data[idx] )
        else:
            file = open( f"param_refine_len{len(ls)}.txt", "a+" )
            file.write(f"{data[idx + 1][0]} {data[idx][1]}\n")
            file.close()

        print( f"\t{idx}/{len(ls)}" )
    
    # shuffle the order of elements in the list before recursive call
    tmp = list( zip(ls, data) )
    random.shuffle( tmp )
    ls, data = zip( *tmp )
    
    return refine( ls, data )

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
        params = []

        # read in desired parameters from the master file
            # one pair (low, high) is located on each line of the file
        with open(param_file, "r") as file:
            for line in file:
                tmp = line.split()
                params.append( [int(tmp[0]), int(tmp[1])] )

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
