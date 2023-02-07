import cv2 as
import numpy as np
from matplotlib import pyplot as plt

'''
This function is meant to take in a 2D list of pixels representing the decompressed
	image data to be evaluated. It converts this list of pixels to intensities, or
	a greyscale representation using integers rather than tuples.

**If needed, camera angle corrections can be inserted in this function as well
'''
def prep_image( pixels ):
	# Return value
	converted = [ ]

	# convert to greyscale
	for row in pixels:
		converted.append( [ (sum(pixel) / 3) for pixel in row ] )

	''' This is where camera deviation angle transforms would go '''

	return converted
	#ENDOF: prep_image(pixels)


'''
This function is the primary workhorse for the measurement procedure. This is the
	first in a series of manual computer vision functions meant to gain precision
	over the generic libraries

	It accepts a 2D list of pixel intensities, and returns x-dim, y-dim, and total
		edge values as 2D arrays
___________________________________________________________________________________

Steps needed:
	- Light Gaussian blur to remove high-frequency noise
	- select a pair of kernels (e.g. Sobel kernels) for convolution
		- use these kernels to:
			- create a horizontal edge 2D list
			- create a vertical edge 2D list
	- combine the horizontal and vertical edges for an absolute edge list.
		- Retain vertical and horizontal edge lists for angle of change computation
	- Return those three lists for use in the refine_edges() function
'''
def find_edges( arr ):
    kernel = []
	return
	#ENDOF: find_horizontal_edges(arr)


'''
This function is meant to be called with edge information as input parameters
	That is, it is meant to be called on the output of the find_edges() function

	It performs some analysis on the edges found in the previous step in order to
		clear up the image, and make the process of measuring the potato much simpler.

	It takes as input a 2D list of absolute edge values, and 2D lists of the
		horizontal and vertical edges as well. It outputs a single 2D list of
		refined edges.

- Slim edges to as close to single-pixel widths as possible:
		- Can implement some interpolation, linear or cubic, here if needed
	- Apply and rejection hueristics devised
	- Apply a test-driven set of thresholds for a hysterisis thresholding step
'''
def refine_edges( arr ):

	return
	#ENDOF: refine_edges(arr)


''''
This function is the second main functional block for the computer vision. 
    Analysis has already been done on the edges to refine the locations as 
    much as possible, so the next step is to use those edges in order to 
    measure the potato to the required precision.
    
    Initially, an assumption will be made that the axes of the potato will
    match up with 
'''
def compute_measurements( arr ):

	return
	#ENDOF: compute_measurements(arr)
