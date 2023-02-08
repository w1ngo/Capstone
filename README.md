# Capstone
This repo will store the drivers written for all embedded systems used for the 
	2022/23 Capstone project. The code will be loaded onto a raspberry pi 4,
	which serves as the computation hub and uses a derivative of the Debian 
	Linux distribution.

Customized .bashrc and .bash_aliases files are written to automate some processes 
	when the shell is initiated. The custom .bashrc (startup procedure) will
	have our code attached, so the user should only have to open a shell or
	command line and login to start the program.

The structure of the code will be mainly written in Python to ease understanding, 
	development, and debugging. C++ was originally being used for image 
	processing and accessed through a dynamically linked library, but
	the opencv library for Python has proved to be quick enough.

In order to use this repo successfully, clone the repository onto your host machine. 
	If using a Windows machine, enable and use a Debian distro on WSL, and do all 
	development through the command line, otherwise the building process will not 
	work.

Sourcing the init.sh script in the shell_scripts folder should download and compile 
	the needed opencv files.

Updates will be posted to the Github periodically (aiming for about once a week).
________________________________________________________________________________________
Conceptual/Info on software:

The edge detection portion of this software is based entirely on opencv. It uses their
	implementations of data structures, blurring functions, and the Canny edge 
	detection algorithm.

For our specific application, a light Gaussian blur was all that was needed, but several
	passes of a median filter have proven to be extremely useful. The output of a
	greyscale, blurred potato image shows a lot of spot noise (due to things such
	as spots on the interior of the potato). This leads to several edges being
	detecting in places undesired. Tweaking the parameters for hysterisis
	thresholding cleans a respectable amount of this noise up, but repeated passes
	of a median filter have proven to be the most effective and reliable approach.

Rather than having a single, finely-tuned edge detection function based on sample data,
	a more general approach has been chosen. Several sets of parameters that
	generally perform well will be used, and they will be used in conjunction
	with one another to arrive at a single, final result. It is unclear
	whether or not this will be in an "average the final answer" or 
	"vote on edge pixels" context, and that decision will be made during
	testing.

In order to determine LWH measurements, the orientation of the potato must be
	derived from its outline. Without getting an angle/axes, the measurements
	can only be max x-spread and max y-spread, which will yield inaccurate
	results for potatoes that are placed askew from the axes of the camera's
	focal plane. The algorithm used to determine the orientation of an object is
	based in trigonometry.

Alternatively, another approach has been identified that uses something called the
	minimum rectangle. In short, once the edges have been detected, an algorithm
	can be applied to identify the rectangle with the smallest area that bounds
	all of the edge points. As we only need the x and y dimensions, the dimensions
	of this rectangle will give the exact dimensions that we are looking for. This
	solves some potential issues with noise on the interior of the potato, should
	the noise-reduction solutions hinted at above not work as consistently as
	expected.

After identifying the edges and the orientation of the potato, all that is left is
	the conversion from pixel spread to SI units for each dimension. Reasearch
	has been done into linalg conversions for slight inaccuracies (due to 
	camera angle, relative closeness to the subject of the image, etc.),
	but these will not be applied unless testing shows our precision is lacking.

Data storage is done using a .csv filetype and written to a flashdrive connected to
	the Raspberry Pi. In order to prevent corruption, two main techniques will
	be used: For times when a file must be held open for an extended period of
	time, a .swp file will be used to avoid corrupting the main file, and 
	files will be kept closed as much as possible.


