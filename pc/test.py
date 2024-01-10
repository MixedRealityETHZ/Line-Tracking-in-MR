import line_tracker
import cv2
import numpy as np
VIS_TRACK = False

if __name__ == '__main__':
    cap = cv2.VideoCapture("tests/testvideo.mp4")

    if not cap.isOpened():
        print("Error opening video file")
        exit()
    
    ret, frame = cap.read()
    if not ret:
        print("Error reading the first frame")
        exit()

    output_video = cv2.VideoWriter("output_video.avi", cv2.VideoWriter_fourcc(*'MJPG'), 30, (frame.shape[1], frame.shape[0]))
    trackerData = line_tracker.LineFeatureTracker()
    
    # Read and display frames until the video ends
    elsed = 0

    while True:
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

            lineRec = cur_img.lineRec

            for m in range(len(lineRec)):
                lines = lineRec[m]
                
                if len(lines) > 20:
                    lines = lines[-20:]
                
                for j in range(len(lines)):
                    start = lines[j]["start"]
                    end = lines[j]["end"]

                    if j == len(lines) - 1:
                        cv2.line(detect_img, start, end, (0, 255, 0), 2, cv2.LINE_AA)
                    else:
                        cv2.line(detect_img, start, end, (0, 0, 55 + 10 * j), 1, cv2.LINE_AA)
            
            cv2.imshow("img", detect_img)
            cv2.waitKey(20)
            output_video.write(detect_img)
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