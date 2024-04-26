import tkinter as tk
from tkinter import filedialog
import yaml

def read_yaml_file(filename):
    # Open and read a YAML file, returning the data
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def write_yaml_file(filename, data):
    # Write data to a YAML file.
    with open(filename, 'w') as file:
        yaml.safe_dump(data, file)

def calculate_statistics(labels):
    # Initialize statistics counters
    stats = {
        'Total Frames': 0,
        'Frames Time_Between': 0,
        'Frames Play': 0,
        'Frames Pass': 0,
        'Frames Run': 0,
        'Frames Punt': 0,
        'Frames Kick-Off': 0,
        'Frames Field_Goal': 0,
        'Total Number of Plays': 0,
        'Number of Pass': 0,
        'Number of Run': 0,
        'Number of Punt': 0,
        'Number of Kick-Off': 0,
        'Number of Field_Goal': 0
    }
    # Store the last timestamp
    last_time = 0  

    # Track whether a "Play" sequence is ongoing
    play_started = False  

    for entry in labels:
        time = entry['time']

        # Calculate frame count since last timestamp
        frame_count = time - last_time  
        new_labels = entry['labels']

        if 'Play' in new_labels:
            if not play_started:

                # If a new "Play" starts, increment the play count and set play_started to True
                play_started = True
                stats['Total Number of Plays'] += 1
            stats['Frames Play'] += frame_count
            
            # Count frames and occurrences for specific play types
            for label in new_labels:
                if label != 'Play':
                    stats['Frames '+ label] += frame_count
                    stats['Number of ' + label] += 1
        else:
            # Reset play_started when the current label sequence is not "Play"
            play_started = False
            if 'Time_Between' in new_labels:
                stats['Frames Time_Between'] += frame_count
        
        # Update last_time to the current timestamp
        last_time = time  

    # Total frames up to the last timestamp
    stats['Total Frames'] = last_time  
    return stats

def main():
    root = tk.Tk()
    root.withdraw()  
    filename = filedialog.askopenfilename(title="Select a YAML file", filetypes=[("YAML files", "*.yaml *.yml")])
    if filename:

        # Process the selected YAML file.
        labels = read_yaml_file(filename)
        stats = calculate_statistics(labels)

        # Generate output filename by appending "_stats" before the file extension.
        output_filename = filename.replace('.yaml', '_stats.yaml').replace('.yml', '_stats.yml')
        write_yaml_file(output_filename, stats)
        print(f"Statistics written to {output_filename}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
