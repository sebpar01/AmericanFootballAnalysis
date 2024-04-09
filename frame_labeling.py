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

# Function to create the folder structure and save frames according to labels in the YAML file
def save_frames_to_folders(video_capture, yaml_data, output_folder, video_name):
    for i, entry in enumerate(yaml_data):
        labels = entry["labels"]
        start_frame = entry["time"]
        end_frame = yaml_data[i + 1]["time"] if i + 1 < len(yaml_data) else None

        # Jump to the desired frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        while True:
            ret, frame = video_capture.read()
            
            if ret:
                # Save the frame in the corresponding label folder
                for label in labels:
                    label_folder = os.path.join(output_folder, label)
                    if not os.path.exists(label_folder):
                        os.makedirs(label_folder)
                    
                    frame_filename = f"{video_name}_frame_{start_frame}.jpg"
                    frame_path = os.path.join(label_folder, frame_filename)
                    cv2.imwrite(frame_path, frame)
                    print(f"Frame {start_frame} saved in the '{label}' folder.")
                
                start_frame += 1
                
                if end_frame is not None and start_frame >= end_frame:
                    break
            else:
                print(f"Error reading frame {start_frame} from the video.")
                next_frame_number = start_frame + 1
                while True:
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, next_frame_number)
                    ret, _ = video_capture.read()
                    if ret:
                        print(f"Frame {next_frame_number} successfully read again.")
                        start_frame = next_frame_number
                        break
                    else:
                        print(f"Error reading frame {next_frame_number} from the video.")
                        next_frame_number += 1

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

    # Create output folder
    output_folder = os.path.splitext(video_file_path)[0] + "_frames"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save frames according to labels in the YAML file
    save_frames_to_folders(video_capture, yaml_data, output_folder, video_name)

    # Release the VideoCapture object
    video_capture.release()

if __name__ == "__main__":
    main()
