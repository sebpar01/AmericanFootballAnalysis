# Script to change timestamp from seconds to frames

import yaml
import os
import cv2
import tkinter as tk
from tkinter import filedialog

# Function to load the YAML file
def load_yaml_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show the file selection dialog and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")])

    if file_path:
        try:
            with open(file_path, 'r') as file:
                yaml_data = yaml.load(file, Loader=yaml.FullLoader)
            print("YAML file loaded successfully.")
            return yaml_data, file_path
        except Exception as e:
            print("Error loading YAML file:", e)
            return None, None
    else:
        print("No YAML file selected.")
        return None, None

# Function to load the video using OpenCV and detect the frame rate
def load_video():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show the file selection dialog and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])

    if file_path:
        video_capture = cv2.VideoCapture(file_path)
        if not video_capture.isOpened():
            print("Error: Unable to load the video.")
            return None, None
        else:
            framerate = video_capture.get(cv2.CAP_PROP_FPS)
            if framerate == 0.0:
                print("Warning: Unable to detect the frame rate of the video.")
            else:
                print("Frame rate of the video:", framerate)

           # Extract video name (without file extension) from file path
            video_name = os.path.splitext(os.path.basename(file_path))[0]

            print("The video was loaded successfully.")
            return video_capture, framerate, file_path, video_name
    else:
        print("No video selected.")
        return None, None, None, None 

# Function to convert seconds to frames
def seconds_to_frames(seconds, framerate):
    return int(seconds * framerate)

# Function to convert YAML file timestamps to frames and save the new YAML file
def convert_yaml_to_frames(yaml_data, framerate, yaml_file_path):
    for entry in yaml_data:
        time_seconds = entry["time"]
        frame_number = seconds_to_frames(time_seconds, framerate)
        entry["time"] = frame_number

    new_yaml_file_path = yaml_file_path.split(".")[0] + "_frames.yaml"
    try:
        with open(new_yaml_file_path, 'w') as file:
            yaml.dump(yaml_data, file)
        print("New YAML file with frame timestamps saved successfully.")
        return new_yaml_file_path
    except Exception as e:
        print("Error saving the new YAML file:", e)
        return None

# Main function
def main():
    # Load the YAML file
    yaml_data, yaml_file_path = load_yaml_file()
    if yaml_data is None:
        return

    # Load the video and detect the framerate
    video_capture, framerate, video_file_path, video_name = load_video()
    if video_capture is None:
        return

    # Create a new YAML file with frame timestamps
    new_yaml_file_path = convert_yaml_to_frames(yaml_data, framerate, yaml_file_path)
    if new_yaml_file_path is None:
        return

if __name__ == "__main__":
    main()