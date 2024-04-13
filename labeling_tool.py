##################### Imports for the processing of the data ###########################
########################################################################################


import time
import csv
import os
import sys
import re
import serial
import glob
import numpy as np
import pandas as pd
import pyqtgraph as pg
import tkinter as tk
import yaml
from scipy import signal
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression
from tkinter import filedialog, ttk
from moviepy.editor import *
from moviepy.video.io.preview import preview
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.editor import VideoFileClip
from PyQt6.QtGui import *
from PyQt6.QtCore import QDir, Qt, QUrl, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtWidgets, QtGui
from pyqtgraph import LegendItem
from IPython.display import clear_output


################################### Labeling Tool ######################################
########################################################################################
##Description: 
# This tool is getting used to asign the labels to the indivual datapoints. This step
# is crucial for the Machine Learning. The technique used here is one hot encoding.
#
############################ by Sandro Tobias Müller ###################################
#Information to the used documentation: 
# https://www.pythonguis.com/pyqt6-tutorial/

############ Adjusted by Sebastian Pareiss to label American Football Plays ############

# Label multiple labels at same time 
# Save labels as yaml-file 

################################## Processing #############################################

previous_button_label = None

class VideoPlayer(QWidget):
    ## Done only has to be included into whole main window
    progressUpdated = pyqtSignal(float)
    currentFrameChanged = pyqtSignal(int)
    framePositionChanged = pyqtSignal(float)
    stateChanged = pyqtSignal(int)
    

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer()
        

        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()
        videoWidget.setFixedSize(1000, 750)
        self.mediaPlayer.setVideoOutput(videoWidget)

        #Open video button 
        openButton = QPushButton("Open Video")   
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(btnSize)
        openButton.setFont(QFont("Noto Sans", 8))
        openButton.setIcon(QIcon.fromTheme("document-open", QIcon("D:/_Qt/img/open.png")))
        openButton.clicked.connect(self.abrir)

        #Play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        #Playback speed button
        self.speedButton = QPushButton('1.0x')
        self.speedButton.setEnabled(True)
        self.speedButton.setFixedHeight(24)
        self.speedButton.setIconSize(btnSize)
        self.speedButton.setFont(QFont("Noto Sans", 8))
        self.speedButton.clicked.connect(self.changePlaybackSpeed)

        #Video slider
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        #layout control 
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.speedButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        #help(self.mediaPlayer)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorChanged.connect(self.handleError)
        self.statusBar.showMessage("Ready")


        

    def abrir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Media",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.mediaPlayer.pause()

    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.stateChanged.emit(state)

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.currentFrameChanged.emit(position)
        self.framePositionChanged.emit(position)
        

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())

    def changePlaybackSpeed(self): 
        speed = self.mediaPlayer.playbackRate()
        if speed == 1.0:
            self.mediaPlayer.setPlaybackRate(0.5)
            self.speedButton.setText('0.5x')
        elif speed == 0.5:
            self.mediaPlayer.setPlaybackRate(0.10)
            self.speedButton.setText('0.10x') 
        else:
            self.mediaPlayer.setPlaybackRate(1.0)
            self.speedButton.setText('1.0x')
    
    def updateVLinePosition(self, position):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            seconds = position / 1000  # convert position from milliseconds to seconds
            self.framePositionChanged.emit(seconds)
            

class LabelingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels = ["Play", "Time_Between", "Run", "Pass", "Punt", "Kick-Off", "Field_Goal", "Other4", "Other5", "Other6"]
        self.labelButtons = []
        self.selectedButton = None
        self.labels_data_list = []

        layout = QGridLayout()

        # Add buttons in the top row
        for idx, label in enumerate(self.labels[:5]):
            button = QPushButton(label)
            button.setCheckable(True)  # Make the button toggleable
            button.clicked.connect(self.labelButtonClicked)
            self.labelButtons.append(button)
            layout.addWidget(button, 0, idx)

        # Add buttons in the bottom row
        for idx, label in enumerate(self.labels[5:]):
            button = QPushButton(label)
            button.setCheckable(True)  # Make the button toggleable
            button.clicked.connect(self.labelButtonClicked)
            self.labelButtons.append(button)
            layout.addWidget(button, 1, idx)

        self.setLayout(layout)

    def labelButtonClicked(self):
        button = self.sender()
        label = button.text()
        current_time = self.parent().videoPlayer.mediaPlayer.position() / 1000

        # If the button is already selected, deselect it
        if button.isChecked():
            # If "Time_Between" is selected, deselect all other buttons
            if label == "Time_Between":
                for btn in self.labelButtons:
                    if btn != button:
                        btn.setChecked(False)
            else:
                # If "Time_Between" button is selected, deselect it
                for btn in self.labelButtons:
                    if btn.text() == "Time_Between":
                        btn.setChecked(False)

            # Update the labels_data dictionary with a list of labels for the current time
            labels = [btn.text() for btn in self.labelButtons if btn.isChecked()]
            labels_data = {"labels": labels, "time": current_time}

            # Write the labels_data dictionary to the YAML file
            with open("GX030047.yaml", "a") as yaml_file:
                # Write the labels_data dictionary to the YAML file with proper indentation
                yaml_file.write("- labels:\n")
                for label in labels:
                    yaml_file.write("  - {}\n".format(label))
                yaml_file.write("  time: {}\n".format(current_time))
                yaml_file.write("\n")
        else:
            # If the button is being unchecked, reset the selectedButton variable
            if button == self.selectedButton:
                self.selectedButton = None



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Labeling Tool")
        self.setGeometry(100, 100, 600, 400)

        self.videoPlayer = VideoPlayer()
        self.labelingWidget = LabelingWidget()

        layout = QHBoxLayout(self)
        layout.addWidget(self.videoPlayer)
        layout.addWidget(self.labelingWidget)


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()