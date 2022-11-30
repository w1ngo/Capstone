'''
This script stores the functions needed to operate the gravitometer-related functions
    for the overall project. This includes motor control, load cell input interpretation, etc
'''


'''
The purpose of this function is to control a motor associated with the gravitometer.
    It takes as input a specification as to which motor is to be controlled. This is
    handled by referencing a helper function for each possible motor. It returns True
    if no exceptions were encountered and false if an error occured.

This function assumes valid input, or that the referenced motor is a proper option
'''
def motor_control( motor ):

    return
    #ENDOF: motor_control(motor)


'''
The purpose of this function is to read in an input from the load cell and convert
    it to a usable form. This requires conversion from the input to a value with units,
    which requires the calibrated value for zero from the load cell. The return value
    is the mass detected, in grams, converted according to the calibrated zero value.

This function assumes valid parameter input, e.g. that it is a positive number
'''
def read_load_cell( calibrated_zero ):

    return
    #ENDOF: read_load_cell()


