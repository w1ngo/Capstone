#ifndef REFINE_PARAMETERS
#define REFINE_PARAMETERS

#include <iostream>
#include "edge_detection_functions.h"
#include <vector>
#include <algorithm>

struct data {
    Mat image;
    int hthresh;
    int lthresh;
    bool gauss;
    bool median;

    data() {
        this->hthresh = 0;
        this->lthresh = 0;
        this->gauss = 0;
        this->median = 0;
    }

    data(Mat img, int high, int low, bool gauss_state, bool median_state):
        image   (img),
        hthresh (high),
        lthresh (low),
        gauss   (gauss_state),
        median  (median_state)
        {}

    data(int high, int low, bool gauss_state, bool median_state):
        hthresh (high),
        lthresh (low),
        gauss   (gauss_state),
        median  (median_state)
        {}
};


void store_data(std::ofstream &fstream, std::vector<data> &vec) {
    fstream << "high,low,gauss status,median status\n\n";

    for(int i = 0; i < vec.size(); ++i) {
        fstream << vec[i].hthresh << ",";
        fstream << vec[i].lthresh << ",";
        fstream << vec[i].gauss   << ",";
        fstream << vec[i].median  << "\n";
    }
    std::cout << "vector written to memory\n";
}


void build_dataset(const char filename[], const int hthresh[], const int lthresh[], std::vector<data> &data_struct) {
    const int hSize = 7;
    const int lSize = 7;

    for(int l = 0; l < lSize; ++l) {
        for(int h = 0; h < hSize; ++h) {
            data_struct.push_back( data( process_image(filename, true,  true,  lthresh[l], hthresh[h]), 
                                         hthresh[h],
                                         lthresh[l],
                                         true,
                                         true
                                       )
                                 );
            data_struct.push_back( data( process_image(filename, true,  false,  lthresh[l], hthresh[h]), 
                                         hthresh[h],
                                         lthresh[l],
                                         true,
                                         false
                                       )
                                 );
        }
    }
}


void traverse_img(Mat img) {
    for(int i = 0; i < img.rows; i++) {
        for(int j = 0; j < img.cols; j++) {
            std::cout << img.at<Vec3b>(i,j) << " ";
        }
        std::cout << std::endl;
    }
}


void optimize_parameters(std::vector<data> &local_maxes) {
    // if the number of high-performing param sets is sufficiently minimized, abort
    if( local_maxes.size() <= 10 ) { return; }
    traverse_img( local_maxes[0].image );

    // run through the entire vector in pairs
    for(int i = 0; i < local_maxes.size() - 1; i += 2) {

        // show a pair of images
        namedWindow( "Image 1", WINDOW_NORMAL ); imshow("Image 1", local_maxes[i    ].image); waitKey(0);
        namedWindow( "Image 2", WINDOW_NORMAL ); imshow("Image 2", local_maxes[i + 1].image); waitKey(0);
        
        // ask user which image is more accurately outlined
        char response;
        std::cout << "Which image is better? \n\t1 for image 1\n\t2 for image 2\n\t0 for neither\n\tany other character for undecided: ";
        std::cin >> response;
        destroyAllWindows();

        // process response and adjust accordingly
        switch(response) {
            case '1': local_maxes.erase( local_maxes.begin() + i + 1 ); break; // erase 2 if 1 was better

            case '2': local_maxes.erase( local_maxes.begin() + i + 0 ); break; // erase 1 if 2 was better

            case '0': local_maxes.erase( local_maxes.begin() + i + 0 );        // erase both if this pair is bad
                      local_maxes.erase( local_maxes.begin() + i + 1 );
                      break;
        };
    }

    // shuffle the vector so that the next iteration can be more effectively performed, report new size
    std::random_shuffle( local_maxes.begin(), local_maxes.end() );
    std::cout << local_maxes.size() << " combinations remaining\n\n";
    
    // store parameter contents in a csv
    std::string filename = std::string() + "param_data" + std::to_string(local_maxes.size()) + ".csv";
    std::ofstream intermediate_files(filename);
    intermediate_files << "high,low,gauss status,median status\n\n";

    for(int i = 0; i < local_maxes.size(); ++i) {
        intermediate_files << local_maxes[i].hthresh << ",";
        intermediate_files << local_maxes[i].lthresh << ",";
        intermediate_files << local_maxes[i].gauss   << ",";
        intermediate_files << local_maxes[i].median  << "\n";
    }
    std::cout << "vector written to memory\n";
    intermediate_files.close();

    // recursive call
    optimize_parameters( local_maxes );
}


void exec(const char filename[], const int hthresh[], const int lthresh[], std::vector<data> &data_struct) {
    build_dataset(filename, hthresh,lthresh, data_struct);
    optimize_parameters( data_struct );
}

void voting(const char filename[], const int hthresh[], const int lthresh[], std::vector<data> &data_struct) {
	Mat arr[ data_struct.size() ];
	for( int i = 0; i < data_struct.size(); ++i ) { arr[i] = process_image( filename, data_struct[i].gauss, data_struct[i].median, data_struct[i].lthresh, data_struct[i].hthresh); }
}

#endif
