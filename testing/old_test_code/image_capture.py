import cv2

cam1 = cv2.VideoCapture(0)  # Defines which camera is used for recording
cam2 = cv2.VideoCapture(1)

"""
Records with both cameras simultaneously, unsure if this works since I only have one webcam for testing.
If unnecessary, use series_recording function instead.
"""
def parallel_recording():
    try:
        for i in range(10):  # adjust of number frames before recording is finished
            check1, frame1 = cam1.read()  # starts video capture
            check2, frame2 = cam2.read()
            cv2.imshow("camera1", frame1)  # shows video recording output, uncomment for testing
            cv2.imshow("camera2", frame2)
            cv2.waitKey(1)  # time in ms between each frame

        cv2.imwrite('pic1.jpg', frame1)  # writes image to specified location
        cv2.imwrite('pic2.jpg', frame2)
        cam1.release()
        cam2.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(e)

    return


"""
Records with cameras in order, takes twice as long as prior function.
"""
def series_recording():
    try:
        for i in range(10):
            check1, frame1 = cam1.read()  # starts video capture
            #cv2.imshow("camera1", frame1)  # shows video recording output, uncomment for testing
            cv2.waitKey(1)  # time in ms between each frame

        cv2.imwrite('pic1.jpg', frame1)
        cam1.release()
        cv2.destroyAllWindows()

        for i in range(10):
            check2, frame2 = cam2.read()
            cv2.imshow("camera2", frame2)
            cv2.waitKey(1)

        cv2.imwrite('pic2.jpg', frame2)
        cam2.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(e)

    return

def test_recording():
    for i in range(10):
        check1, frame1 = cam1.read()  # starts video capture
        #cv2.imshow("camera1", frame1)  # shows video recording output, uncomment for testing
        cv2.waitKey(1)  # time in ms between each frame

    cv2.imwrite('pic1.jpg', frame1)
    cam1.release()
    cv2.destroyAllWindows()




# parallel_recording()
# series_recording()
test_recording()
