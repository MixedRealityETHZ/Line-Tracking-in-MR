import cv2
import os

def save_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Save frame as an image
            frame_name = f"frame_{frame_count}.jpg"  # Change extension if needed
            frame_path = os.path.join(output_folder, frame_name)
            cv2.imwrite(frame_path, frame)

            frame_count += 1
        else:
            break

    # Release the VideoCapture object and close any open windows
    cap.release()

# Specify the path to your video file
video_path = 'output_video.avi'

# Specify the output folder where frames will be saved
output_folder = 'frames'

save_frames(video_path, output_folder)
