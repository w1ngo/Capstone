# Capstone
This repo will store the drivers written for all embedded systems used for the 
	2022/23 Capstone project. The code will be loaded onto a raspberry pi 4,
	which serves as the computation hub and uses a derivative of the Debian 
	Linux distribution

________________________________________________________________________________________
Customized files are written to automate some processes when the shell is 
    initiated. The custom .bashrc (startup procedure) will have our code attached,
    so the user should only have to open a shell or command line and login to start 
    the program.

**In order to use this repo successfully, clone the repository onto your host machine. 
Sourcing the init.sh script will update the device and install the required packages. 
It will print a message about how to install the one package that cannot be auto-installed.
After that, your device should be configured properly. **
________________________________________________________________________________________
Info on Gravitometer software:

The Gravitometer software is mainly comprised of motor controls and ADC readings. There 
	is not much data processing or computationally heavy operations to do, relative
	to the Dimentiometer section. Functions have been written to handle motor controls,
	load cell controls, file reading and writing, and terminal I/O. Should this project
	be built upon or modified later, usage of these functions should reduce the amount
	of time needed to make changes due to their modular nature.

________________________________________________________________________________________
Conceptual/Info on Camera software:

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
	with one another to arrive at a single, final result. The specific way that
	this will occur is described below.

The approach taken to find the orientation/measurements uses something called the
	minimum rectangle. In short, once the edges have been detected, an algorithm
	can be applied to identify the rectangle with the smallest area that bounds
	all of the edge points. As we only need the x and y dimensions, the dimensions
	of this rectangle will give the exact dimensions that we are looking for. This
	solves some potential issues with noise on the interior of the potato, should
	the noise-reduction solutions hinted at above not work as consistently as
	expected. **NOTE** this is extremely sensitive to contours that are not fully
	joined, and the output of the edge detection stage alone is clear to the 
	human eye, but not the computer. Therefore, a light Gaussian Blur is
	applied once more in order to join edges together when small numbers of 
	pixels are missing.

The above step is applied to the edge detector outputs (for each set of parameters).
	The minimum rectangles are then compiled using a basic averaging technique. There 
	is another statistical approach that has been researched and can be taken should
	more accuracy be needed in the future using an intersection of confidence regions,
	however averaging the outputs of tested parameters is the approach taken currently.

After identifying the bounds of the potato as described above, all that is left is
	the conversion from pixel spread to SI units for each dimension. Reasearch
	has been done into linalg conversions for slight inaccuracies (due to 
	camera angle, relative closeness to the subject of the image, etc.),
	but these will not be applied unless testing shows our precision is lacking.

Data storage is done using a .csv filetype and written to a flashdrive connected to
	the Raspberry Pi. In order to prevent corruption, two main techniques will
	be used: For times when a file must be held open for an extended period of
	time, a .swp file will be used to avoid corrupting the main file, and 
	files will be kept closed as much as possible.

________________________________________________________________________________________
Things to keep in mind

Due to the highly specified application of the edge detection software, deviations in
	application will have noteably adverse effects on performance. For example,
	inconsistent lighting resulting in large or notable shadows will cause
	reliably inaccurate readings.

The edge detection functionality is built with several assumptions, and usage of it
	should keep this in mind. Things such as large shadows, in its current state,
	can drastically affect the performance of it. With this in mind, it should
	be used only in a configuration where lighting can be controlled/moderated
	if possible. Fixes can certainly be applied, but will not if proven
	unnecessary.

Testing was done on .jpg and .png filetypes. For some reason, .png files took
	noticeably longer to process, at no noteable increase in accuracy. It
	was not a long wait, simply longer than the time needed for .jpgs. For
	that reason, .jpg will likely be the desired filetype for processing images.
	UPDATE: The cameras natively export .jpgs, and cannot be reconfigured to
	output a lossless or raw format. Camera parameters, such as contrast,
	brightness, sharpness, etc., can be controlled through the shell. Commands
	have been configured to automate the image-taking process, from detecting
	the USB-camera detection to sending the command to take a picture.

Speed has not been an issue after basic optimization techniques were implemented.
	Charts were made to identify "hot spots," and one major loop was reduced 
	significantly, cutting the single-image full processing stage from over 
	thirty seconds to mere fractions of a second. This confirms our initial
	assumption that the code can run serially, and should not need to get
	around Python's GIL for multithreading.
