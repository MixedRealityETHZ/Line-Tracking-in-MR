import cv2
import os
import pyelsed
import numpy as np

# Path to input video
video_path = '../tests/test_video3.mp4'

# Create a folder to save processed frames
output_folder = 'frames'
os.makedirs(output_folder, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect lines using pyelsed
    segments, scores = pyelsed.detect(gray_frame, minLineLen=90, gradientThreshold=32)

    #dbg = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    for s in segments.astype(np.int32):
        cv2.line(frame, (s[0], s[1]), (s[2], s[3]), (0, 255, 0), 2, cv2.LINE_AA)

    # Save the processed frame
    output_frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(output_frame_path, frame)

    frame_count += 1

# Release the video capture and close the window
cap.release()
