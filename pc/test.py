import line_tracker
import cv2
import numpy as np
VIS_TRACK = True

numLinesToShow = 15
lengthDiff = 0.4 / numLinesToShow
colors = [
    # (0, 0, 255),
    (21, 0, 234),
    (42, 0, 213),
    (64, 0, 191),
    (85, 0, 170),
    (106, 0, 149),
    (128, 0, 128),
    (149, 0, 106),
    (170, 0, 85),
    (191, 0, 64),
    (213, 0, 42),
    (234, 0, 21),
    (255, 0, 0),
    (234, 21, 0),
    (213, 42, 0),
    (191, 64, 0),
    (170, 85, 0),
    (149, 106, 0),
    (128, 128, 0),
    (106, 149, 0)
]
colors = colors[:numLinesToShow]

if __name__ == '__main__':
    cap = cv2.VideoCapture("tests/test_video.mp4")

    if not cap.isOpened():
        print("Error opening video file")
        exit()
    
    ret, frame = cap.read()
    if not ret:
        print("Error reading the first frame")
        exit()

    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (width*2, height))
    # output_video = cv2.VideoWriter("output_video.avi", cv2.VideoWriter_fourcc(*'MJPG'), 30, (frame.shape[1], frame.shape[0]))
    trackerData = line_tracker.LineFeatureTracker()
    
    elsed = 0
    # Read and display frames until the video ends
    while True:
        #print(frame)
        trackerData.readImage(frame, elsed)
        cur_img = trackerData.getCurImg()
        img = cur_img.img

        tmp_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        un_lines = cur_img.vecLine

        lineIDs = cur_img.lineID

        successes = cur_img.success

        for j in range(len(un_lines)):
            if successes[j] != -1:
                continue
            
            start = un_lines[j]["keyPoint"][1]
            end = un_lines[j]["keyPoint"][-1]
            start1 = un_lines[j]["StartPt"]
            end1 = un_lines[j]["EndPt"]

            cv2.line(tmp_img, start, end, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.line(tmp_img, start1, end1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(tmp_img, str(lineIDs[j]), un_lines[j]["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)
        
        un_lines = cur_img.vecLine
        for m in range(len(un_lines)):
            if successes[m] == -1:
                break

            start = un_lines[m]["keyPoint"][1]
            end = un_lines[m]["keyPoint"][-1]
            start1 = un_lines[m]["StartPt"]
            end1 = un_lines[m]["EndPt"]

            cv2.line(tmp_img, start, end, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.line(tmp_img, start1, end1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(tmp_img, str(lineIDs[m]), un_lines[m]["keyPoint"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 230, 0), 1, cv2.LINE_AA)
        
        if VIS_TRACK:
            detect_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            # Tracker
            lineRec = cur_img.lineRec
            for m in range(len(lineRec)):
                lines = lineRec[m]
                lines = lines[::-1]

                if len(lines) > numLinesToShow:
                    lines = lines[:numLinesToShow]
                
                for j in range(len(lines)):
                    start = lines[j]["start"]
                    end = lines[j]["end"]
                    s = int((1 - lengthDiff * j) * start[0] + lengthDiff * j * end[0]), int((1 - lengthDiff * j) * start[1] + lengthDiff * j * end[1])
                    e = int((1 - lengthDiff * j) * end[0] + lengthDiff * j * start[0]), int((1 - lengthDiff * j) * end[1] + lengthDiff * j * start[1])
                    if j == 0:
                        cv2.line(detect_img, s, e, (0, 0, 255), 2, cv2.LINE_AA)
                    else:
                        cv2.line(detect_img, s, e, colors[j], 1, cv2.LINE_AA)

            # Gradient map
            gray = img
            # Compute gradients using Sobel operators
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            # Compute the magnitude of the gradient
            magnitude = np.sqrt(grad_x**2 + grad_y**2)
            # Normalize the magnitude to the range [0, 255]
            magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
            # Convert the gradient map to uint8
            gradient_map = np.uint8(magnitude)
            gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            gradient_map = cv2.cvtColor(gradient_map, cv2.COLOR_GRAY2RGB)

            combined = np.hstack((detect_img, gradient_map))
            cv2.imshow("img", combined)
            cv2.waitKey(20)
            output_video.write(combined)
        else:            
            cv2.imshow("img", tmp_img)
            cv2.waitKey(20)
            output_video.write(tmp_img)
        
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break
    
    output_video.release()
    cv2.destroyAllWindows()