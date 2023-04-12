#!/bin/bash

# More frames brings more light into the image.
# Want at least 5 with current settings
# should also play with brighness/exposure
# also consider dropping saturation? No need
# To inflate saturation when we jump to greyscale
# anyway

# Also, python script is currently converting to
# greyscale...can take this out since this script
# does that on input.


# line below prints controls that can be applied to the camera
# fswebcam -d /dev/video0 --list-controls


fswebcam --device /dev/video0  \
	 --quiet               \
	 --resolution 640x480  \
	 -s sharpness=15       \
	 --frame 5             \
	 --no-timestamp        \
	 --no-banner           \
	 --no-info             \
	 --greyscale           \
	 --save                \
         image_cam1_5frames.jpg

