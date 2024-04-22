![Labeling_Video_Github](https://github.com/sebpar01/AmericanFootballAnalysis/assets/101809039/2bb56ab5-c1e0-45b5-b38a-e95dedf76c15)# Bachelor Thesis - README
This is the Repository for my bachelor's thesis: Automatisierte Nachbereitung von Filmaufnahmen im American Football mittels Deep-Learning-Algorithmus (Automated post-processing of football footage in American Football using a Deep Learning approach)

# Introduction
This repository contains all the code and files which are necessary for my bachelor's thesis. The aim of the thesis is to classify American football plays based on videos. The individual steps will be explained in more detail in the following chapters.

# Labeling 
To conduct classification of the self-recorded videos, they must be appropriately labeled. Based on the one-hot encoding principle, two levels of labeling are performed. Initially, a distinction is made between 'Play' and 'Time Between' to detect relevant playing time. Recordings labeled as 'Play' can subsequently be further categorized into 'Run', 'Pass', 'Punt', 'Kick-Off', and 'Field Goal'. 
The figure below shows the labeling concept.

![Labels](https://github.com/sebpar01/AmericanFootballAnalysis/assets/101809039/75fbd26a-7c68-41ca-ba8e-3cea10f8286a)


## Video Labeling (labeling_tool.py)

To facilitate labeling directly within the video recordings, a Python dashboard is utilized. This dashboard was developed using the PyQt6 package. Within this dashboard, there is a dedicated button for each label. When a specific sequence is detected in the video, the corresponding label can be selected. In this process, the multi-level one-hot encoding principle described above is applied.
By pressing a button, an entry with the timestamp and the corresponding label is created in a YAML file. Consequently, each timestamp in the video can be assigned a label based on this YAML file. This is crucial for further labeling of the frames.
![Uploading Labeling_Video_Github.svg…]()


## Frame Labeling (frame_labeling.py)
For the deep learning approach, it is now crucial to label each individual frame. To achieve this, the video is split into individual frames using OpenCV. The YAML file generated through video labeling is then converted so that the timestamp is converted from seconds to frames.
Subsequently, each individual frame of the video can be labeled according to the YAML file. For this purpose, a separate folder is created for each category, in which the corresponding frames are stored.
All these steps are carried out by the frame_labeling.py script.
