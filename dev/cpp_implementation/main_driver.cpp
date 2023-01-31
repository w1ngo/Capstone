
#include "edge_detection_functions.h"
#include "refine_parameters.h"

int main(int argc, char *argv[]) {
    char               filename[] = "./images/isolated_potato.jpg";
    int                highs[]    = { 100, 115, 130, 145, 160, 175, 200 };
    int                lows[]     = { 5,   20,  45,  60,  75,  90,  100};
    std::vector<data>  data_vec;

//    exec(filename, highs, lows, data_vec);

    Mat one = process_image( filename, true, true, 200, 20 );
    Mat two = process_image( filename, true, false, 175, 60 );

    namedWindow( "Image 1", WINDOW_NORMAL ); imshow("Image 1", one); waitKey(0);
    namedWindow( "Image 2", WINDOW_NORMAL ); imshow("Image 2", two); waitKey(0);
    destroyAllWindows();

    namedWindow( "Combined", WINDOW_NORMAL ); imshow( "Combined", one ^ two ); waitKey(0);
    namedWindow( "1 - diff", WINDOW_NORMAL ); imshow( "1 - diff", one - (one ^ two)); waitKey(0);
    namedWindow( "2 - diff", WINDOW_NORMAL ); imshow( "2 - diff", two - (one ^ two)); waitKey(0);
    destroyAllWindows();

    return 0;
}

