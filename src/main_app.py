import cv2
from .line_tracking.naive_line_detect_per_frame import detect_lines

# (Generally) useful information for developers.
# The Open Computer Vision Library (OpenCV) is natively implemented in C/C++.
# However, due to Python's popularity, an API wrapper has been created.
# A centralized source which contains the API signatures is the official documentation of CV2 Python.
# To be precise, the most updated version which does so is version 4.5.5 (https://docs.opencv.org/4.5.5/),
# just below the correspnding C/C++ signatures.


def run():

    # Define one video capturing object (i.e. camera) of the system.
    camera = cv2.VideoCapture(0)

    while True:
        capture_success, frame = camera.read()
        # NOTE: By default, `cv2.imread` reads images in a BGR (Blue-Green-Red) format. 

        if not capture_success:
            raise RuntimeError('No frame was captured from camera device.\nCheck connection of camera device.')
        
        # TODO: Here is where our algorithm will be called on the captured image.
        frame = detect_lines(frame)
        
        # Display the resulting frame 
        cv2.imshow('frame', frame) 
        
        # The 'q' button is set as the quitting button.
        # It may be changed to any desired button (if any). 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        # Developer details: explanation of the above `if` condition.
        # 1. `cv2.waitKey()` returns 32-bit integer value;
        #   the return type in C is `int`, as can be seen from the official documentation
        #   (https://docs.opencv.org/4.5.5/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7)
        # 2. `& 0xFF`` extracts the last 8 bits of the LHS of the expression, i.e. of `cv2.waitKey()`.
        # 3. The `ord` command return the ASCII (integer) representation
        #   of the argument. 
    
    # After the loop release the camera object 
    camera.release() 
    # Destroy all the windows.
    cv2.destroyAllWindows()


    # # By default, `cv2.imread` reads images in a BGR (Blue-Green-Red) format. 
    # img_bgr = cv2.imread('./test.jpg')
    # img_grayscale = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # print(f'img = {img_grayscale}, img.shape = {img_grayscale.shape}')
    # segments, scores = pyelsed.detect(img_grayscale)

    # dbg = cv2.cvtColor(img_grayscale, cv2.COLOR_GRAY2RGB)
    # for s in segments.astype(np.int32):
    #     cv2.line(img_bgr, (s[0], s[1]), (s[2], s[3]), (255, 0, 0), 1, cv2.LINE_AA)
    # cv2.imshow('test', img_bgr)
    # cv2.waitKey(0)