#!/bin/bash

# This script is written in bash, tested on a Debian VM hosted on WSL 2 for Windows 10 Pro
#   on a 64-bit machine. It is meant to run on a Raspberry Pi 4 with a Raspbian OS, which
#   resembles a stripped-down version of the Debian Linux distribution.
# 
# This script may one day be replaced by Python script(s) entirely, however it currently
#   is meant to be the main environment from which all operations originate for our
#   specific project. Python functions are referenced from within this shell script
#   to perform different operations and give values, while this script handles the
#   user interface and basic file operations.
# 
# This script is meant to ease the process of using the bash terminal for an operator
#   uninterested in learning and remembering bash commands to navigate the file
#   system and the terminal. It is for this reason that basic commands, such as 
#   ls, are offered as functions to select.

echo "Initializing terminal interface..."
echo ""
echo ""
echo "  Press Ctrl and C simultaneously at any time to exit this interface forcefully."

# Environment variable. Stores the function that the user currently wants to implement
# Options are:
#	- Display contents of a file
#	- Delete a file
#	- Open a new file to log data
FUNCTION=0

# Environment variable. Stores the modules currently in use
# 	- Bit 0 set if the gravitometer is in use
#	- Bit 1 set if the gravitometer is in use
#	- Both bits set if both are in use
MODULES=0

# Environment variables. Used to keep track of user inputs and control execution
FILENAME=""
FILETYPE=""
UTILITY=""

# ____________________________________________________________________________ #

echo    "Which modules are in use? The options are:"
echo    "    1 for gravitometer"
echo    "    2 for dimentiometer"
echo    "    3 for both"
echo -n "--> "
read FUNCTION
echo ""
echo ""
clear

while [ true ]; do
	echo    "Enter the number of a function to run"
	echo    "The options are:"
	echo    "    - 1 = display the contents of a file"
	echo    "    - 2 = delete a file"
	echo    "    - 3 = create a file"
	echo    "    - 4 = display list of files in memory"
	echo    "    - 5 = make new directory"
	echo    "    - 6 = delete a directory (only if empty)"
	echo    "    - 7 = delete a directory and all files within"
	echo -n "--> "
	read FUNCTION

	case $FUNCTION in

	# Display specific file
		1 | display | disp)
			clear
			echo ""
			echo    "Display file function selected"
			echo    "Enter the filename to print. The following lines show visible filenames"
			echo $(ls)
			echo -n "--> "
			read FILENAME

			clear
			echo "    < START OF FILE >"
			cat $FILENAME
			echo "     < END OF FILE >"
			echo ""
			echo ""
			;;
		
		
		# Delete specific file
		2 | delete | del)
			clear
			echo ""
			echo    "Delete file function selected"
			echo "File list:"
			echo "  $(ls)"
			echo -n "Enter the filename of the file to remove: "
			read FILENAME

			echo    "Deleting file $FILENAME..."
			rm $FILENAME
			clear

			echo    "Deletion complete"
			echo    "    Updated file list:"
			echo $(ls --color=auto)
			echo ""
			echo ""
			;;


		# Create a new file
		3 | create | new)
			clear
			echo -n "Enter your desired filename: "
			read FILENAME
			if [[ $FILENAME == *"."* ]]; then
				echo "Creating file $FILENAME..."
				touch $FILENAME

			else
				echo -n "No filetype detected. Please input extension (e.g., .csv or .txt): "
				read FILETYPE
				FILENAME=$FILENAME$FILETYPE
				echo "Creating file $FILENAME..."
				touch $FILENAME
			fi
			clear

			echo "File created"
			echo "    Updated file list:"
			echo $(ls --color=auto)
			echo ""
			echo ""
			;;


		# Display files in current directory
		4 | list | ls | files)
			clear
			ls --color=auto
			echo ""
			echo ""
			;;


		# Create a new directory
		5)
			clear
			echo -n "Enter your desired directory name: "
			read FILENAME

			mkdir $FILENAME

			echo "Would you like to navigate to the new directory, $FILENAME? [Y/n] "
			read UTILITY
			if [ $UTILITY == "Y" ]; then
				cd $FILENAME
			elif [ $UTILITY == "y" ]; then
				cd $FILENAME
			fi
			
			;;


		# Delete a directory iff empty
		6)
			clear
			echo -n "Enter the name of the directory you would like to delete: "
			read FILENAME

			echo -n "Attempting to remove directory $FILENAME, command will fail if directory is not empty"
			rmdir $FILENAME
			clear

			echo "Updated contents of the current directory: "
			echo $(ls --color=auto)
			echo ""
			;;


		# Delete a directory and all of its files
		7)
			echo -n "Enter the name of the directory you would like to delete: "
			read FILENAME
		
			echo -n "Are you sure that you want to forcefully delete folder $FILENAME and any files within? [Y/n]: "
			read UTILITY
			if [[ $UTILITY	== "Y" || $UTILITY == "y" ]]; then
				echo "Issuing removal command..."
				rm -r $FILENAME
			
			else
				echo "Aborting delete procedure..."
			fi
			clear
			;;

	
		?)
			# Statements for unrecognized input
			echo ""
			clear
			echo "Unrecognized case"
			echo ""
			echo ""
			break
			;;
	esac

done


