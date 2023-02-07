# Capstone
This repo will store the drivers written for all embedded systems used for the 2022/23 Capstone project
	The code will be loaded onto a raspberry pi 4, which serves as the computation hub and uses a
	derivative of the Debian Linux distribution.

A customized .bashrc file is written to automate some processes when the shell is initiated.
A customized .bash_aliases file is referenced by the .bashrc file to ease shell navigation.

The Raspberry Pi's startup procedures will have our code attached at the end so that the user
	will not have to do anything other than turn the device on.

The structure of the code will be mainly written in Python to ease understanding, development, and debugging.
	C++ functions are used for image processing to speed things along.

In order to use this repo successfully, clone the repository onto your host machine. If using a Windows machine,
	enable and use a Debian distro on WSL, and do all development through the command line, otherwise the 
	building process will not work.

Sourcing the init.sh script in the shell_scripts folder should download and compile the needed
	opencv files.

Updates will be posted to the Github periodically (aiming for about once a week).

