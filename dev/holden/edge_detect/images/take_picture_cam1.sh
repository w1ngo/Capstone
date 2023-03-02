#!/bin/bash

fswebcam --device /dev/video0  \
	 --quiet               \
	 --resolution 640x480  \
	 -s sharpness=15       \
	 --frame 10            \
	 --no-timestamp        \
	 --no-banner           \
	 --no-info             \
	 --greyscale           \
	 --png 0               \
	 --save                \
         image.png

# line below prints controls that can be applied to the camera
# fswebcam -d /dev/video0 --list-controls
 


