# Bachelor Thesis - README
This is the Repository for my bachelor's thesis: Automatisierte Nachbereitung von Filmaufnahmen im American Football mittels Deep-Learning-Algorithmus (Automated post-processing of football footage in American Football using a Deep Learning approach)

# Introduction
This repository contains all the code and files which are necessary for my bachelor's thesis. The aim of the thesis is to classify American football plays based on videos. This repository includes a brief explanation of each file. More detailed information about the methodology has been documented in my bachelor's thesis. In the future, this repository will also include an overview of the methodology.

More to come soon...
Stay tuned.
# Labeling 

## Video Labeling (labeling_tool.py)
PyQt6 dashboard to assign labels to a running video. An existing dashboard was adapted for this purpose. Assigned labels are saved (timestamps in seconds) in a YAML file.

## Frame Labeling (frame_labeling.py)

Code to convert the previously conducted labeling of an entire video to individual frames. The existing YAML file is converted from seconds to frames by calculating the fps. Then, a separate folder is created for each label, in which the corresponding frames are stored.

# Dataset

## Statistics (statistics.py)
Code for generating statistics to capture the frequency and distribution of the classes.

# Development of the Neural Network

## Binary Classification (Binary_Classification.ipynb)
Code that includes data processing, the data loader, and the neural network architecture for binary classification. The network consists of a CNN (ResNet50) combined with an LSTM. The validation of the network is also performed in this code.

## Multiclass Classification (Play_Type_Classification.ipynb)
This code includes the same steps as the one for binary classification. The network architecture is also similar. The difference here is that it distinguishes between 5 classes instead of just two, hence the name multiclass classification.

# Additional Code

## plot.py
 Code to creat plots to visualize results and processes; a plot for labeling is presented here.

## Citation.cff
This cff file is used to store all the information needed to enable the citation of this repository

## Further Research 
This is the further research section 
