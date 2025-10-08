"""
python video2images.py <video_path> <output_dir> <frames_per_second>
python video2images.py D:/Research/ZZB/AssetGenerator/data/demo1/chair.mp4 D:/Research/ZZB/AssetGenerator/data/demo1/images 2
"""

import cv2
import os
import argparse

def video_to_images(video_path, output_dir, frames_per_second):
    """
    Extract frames from a video at a specified rate and save them as images.

    :param video_path: Path to the input video file.
    :param output_dir: Directory to save the extracted images.
    :param frames_per_second: Number of frames to extract per second.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # Get the video's frame rate
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / frames_per_second)

    frame_count = 0
    saved_count = 0

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Save the frame if it matches the interval
        if frame_count % frame_interval == 0:
            image_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(image_path, frame)
            saved_count += 1

        frame_count += 1

    video_capture.release()
    print(f"Extraction complete. {saved_count} frames saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video.")
    parser.add_argument("video_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_dir", type=str, help="Directory to save the extracted images.")
    parser.add_argument("frames_per_second", type=int, help="Number of frames to extract per second.")

    args = parser.parse_args()

    video_to_images(args.video_path, args.output_dir, args.frames_per_second)