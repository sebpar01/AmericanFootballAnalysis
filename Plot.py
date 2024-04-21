import matplotlib.pyplot as plt
import yaml

# Load data from the YAML file
with open('GX020053.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Function to create the plots
def create_plots(data):
    # Define the labels to be used
    labels = ["Play", "Time_Between", "Pass", "Run", "Punt", "Field Goal", "Kick-Off"]

    # Create subplots based on the number of labels
    fig, axs = plt.subplots(len(labels), figsize=(10, 8), sharex=True)

    # Iterate over each label
    for i, label in enumerate(labels):
        y = []
        x = []
        # Extract the data points for the current label
        for entry in data:
            if label in entry['labels']:
                y.append(1)  # Label is active
            else:
                y.append(0)  # Label is inactive
            x.append(entry['time'])  # Time associated with the label
        # Create step plot for the current label
        axs[i].step(x, y, where='post')
        # Set y-axis ticks and labels
        axs[i].set_yticks([0, 1])
        axs[i].set_yticklabels(['0', '1'])
        # Set x-axis limit based on the time range
        axs[i].set_xlim([0, x[-1]])
        # Set title for the subplot with appropriate padding
        axs[i].set_title(label, loc='center', pad=20)

    # Set common x-label for all subplots
    plt.xlabel('Time')
    # Adjust layout to prevent overlapping of subplots
    plt.tight_layout()
    # Display the plots
    plt.show()

# Main program
if __name__ == "__main__":
    file_path = "your_file.yaml"  # Replace with the actual file path
    create_plots(data)
