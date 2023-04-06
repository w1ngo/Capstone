#!/bin/bash

fswebcam --device /dev/video2  \
	 --quiet               \
	 --resolution 640x480  \
	 -s sharpness=15       \
	 --frame 10            \
	 --no-timestamp        \
	 --no-banner           \
	 --no-info             \
	 --greyscale           \
	 --save                \
         image_cam2.jpg

# line below prints controls that can be applied to the camera
# fswebcam -d /dev/video0 --list-controls
 


