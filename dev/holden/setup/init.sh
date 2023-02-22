sudo apt update

sudo apt install python3
sudo apt install python3-pip
pip install opencv-python

clear
echo "Initialization process should be complete. Proceed to building."

export BUILD='g++ main_driver.cpp -o edge_detect -I /usr/local/include/opencv4 -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui'
