#ifndef EDGE_DETECTION_FUNCTIONS
#define EDGE_DETECTION_FUNCTIONS

#include <iostream>
#include "opencv2/opencv.hpp"
#include <string.h>
#include <fstream>

using namespace cv;

void get_filename(const int num_args, const char *strings[], std::string& filename) {
    std::cout << "Running " << strings[0] << std::endl << std::endl;

    for(int i = 1; i < num_args; ++i) {
        if( (strcmp(strings[i], "-f")     == 0) || 
            (strcmp(strings[i], "-file")  == 0) )  { filename = strings[++i]; return; }
        else                                       { std::cout << "argument " << strings[i] << " unrecognized" << std::endl; }
    }
}

Mat process_image(const std::string filename, const bool gauss_filter, const bool median_filter, const int low_edge_threshold, const int high_edge_threshold) {
    // load image in, exit if reading process failed
    Mat img;
    try         { cvtColor( imread(filename), img, COLOR_BGR2GRAY); }
    catch (...) {
        std::cout << "image read failed for image at location " << filename << std::endl;
        return img;
    }

    // apply desired image filters
    if (gauss_filter)  { GaussianBlur(img, img, Size(7,7), 0); }
    if (median_filter) { medianBlur(img, img, 7); }


    // Perform edge detection using the opencv implemenetation of the Canny algorithm
    Canny(img, img, low_edge_threshold, high_edge_threshold, 3, false);
    return img;
}

Mat voting_process(const std::string filename, const uint32_t parameters[], const int num_params) {
    Mat img;



    return img;
}

#endif
