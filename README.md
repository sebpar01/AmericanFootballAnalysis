# Bachelor Thesis - README
This is the Repository for my bachelor's thesis: Automatisierte Nachbereitung von Filmaufnahmen im American Football mittels Deep-Learning-Algorithmus (Automated post-processing of football footage in American Football using a Deep Learning approach)

# Introduction
This repository contains all the code and files which are necessary for my bachelor's thesis. The aim of the thesis is to classify American football plays based on videos. The individual steps will be explained in more detail in the following chapters.

# Labeling 
To conduct classification of the self-recorded videos, they must be appropriately labeled. Based on the one-hot encoding principle, two levels of labeling are performed. Initially, a distinction is made between 'Play' and 'Time Between' to detect relevant playing time. Recordings labeled as 'Play' can subsequently be further categorized into 'Run', 'Pass', 'Punt', 'Kick-Off', and 'Field Goal'. 
The figure below shows the labeling concept.

## Video Labeling (labeling_tool.py)
To facilitate labeling directly within the video recordings, a Python dashboard is utilized. This dashboard was developed using the PyQt6 package. Within this dashboard, there is a dedicated button for each label. When a specific sequence is detected in the video, the corresponding label can be selected. In this process, the multi-level one-hot encoding principle described above is applied.
By pressing a button, an entry with the timestamp and the corresponding label is created in a YAML file. Consequently, each timestamp in the video can be assigned a label based on this YAML file. This is crucial for further labeling of the frames.


## Frame Labeling (frame_labeling.py)
