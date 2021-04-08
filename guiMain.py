from __future__ import print_function
import sys
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
import requests
from gtts import gTTS
from time import ctime
from time import strftime
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGroupBox,
                             QHBoxLayout, QLabel, QMainWindow, QPushButton,
                             QRadioButton, QSizePolicy, QSlider, QStyle,
                             QVBoxLayout, QWidget)

r = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            Assistant_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            Assistant_speak('Sorry, I did not get that')
        except sr.RequestError:
            Assistant_speak('Sorry, my speech service is down')
        return voice_data


def Assistant_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Voice Assistant"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 600

        self.recWindow = QWidget() # separate record window for when record button pressed
        self.impWindow = QWidget() # import window
        self.liveWindow = QWidget() # live window

        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("MainIcon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        vbox.addWidget(self.genBox)
        vbox.addWidget(self.webBox)
        vbox.addWidget(self.exitButton)
        self.setLayout(vbox)

        self.show()

    def createLayout(self):
        # transcribe section
        self.groupBox = QGroupBox("Transcribe")
        hBoxLayout = QVBoxLayout()

        recButton = QPushButton("Record", self)
        hBoxLayout.addWidget(recButton)
        recButton.setToolTip("Click to record from your mic")
        recButton.clicked.connect(self.recordClicked)

        impButton = QPushButton("Import", self)
        hBoxLayout.addWidget(impButton)
        impButton.setToolTip("Click to import an audio file")
        impButton.clicked.connect(self.importClicked)
        
        liveButton = QPushButton("Live Transcribe", self)
        hBoxLayout.addWidget(liveButton)
        liveButton.setToolTip("Click to live transcribe your words")
        liveButton.clicked.connect(self.liveClicked)

        self.groupBox.setLayout(hBoxLayout)

        # general assistant section
        self.genBox = QGroupBox("General assistant")
        gBoxLayout = QVBoxLayout()

        generalAssistantButton = QPushButton("Ask something", self)
        gBoxLayout.addWidget(generalAssistantButton)
        generalAssistantButton.setToolTip("Click to ask the assistant something")
        generalAssistantButton.clicked.connect(self.generalAssistantClicked)

        self.genBox.setLayout(gBoxLayout)

        # web assistant section
        self.webBox = QGroupBox("Web assistant")
        wBoxLayout = QVBoxLayout()

        # google search
        gSearchButton = QPushButton("Search Google", self)
        wBoxLayout.addWidget(gSearchButton)
        gSearchButton.setToolTip("Click to search Google with your voice")
        gSearchButton.clicked.connect(self.googleSearchClicked)

        # find location
        locationButton = QPushButton("Find a location", self)
        wBoxLayout.addWidget(locationButton)
        locationButton.setToolTip("Click to find a location on Google Maps")
        locationButton.clicked.connect(self.findLocationClicked)

        # play music
        playMusicButton = QPushButton("Play music on Spotify", self)
        wBoxLayout.addWidget(playMusicButton)
        playMusicButton.setToolTip("Click to play music from Spotify")
        playMusicButton.clicked.connect(self.playMusicClicked)

        self.webBox.setLayout(wBoxLayout)

        # exit section
        self.exitButton = QPushButton("Exit", self)
        self.exitButton.setToolTip("Click to exit the application")
        self.exitButton.setStyleSheet("background: darkred; color: white")
        self.exitButton.clicked.connect(self.exitClicked)

    def recordClicked(self):
        # code for record button
        self.recWindow = RecordWindow() # open record window (RecordWindow class)

    def importClicked(self):
        # code for import button
        self.impWindow = ImportWindow() # open import window (ImportWindow class)

    def liveClicked(self):
        # code for live button
        self.liveWindow = LiveWindow() # open live window (LiveWindow class)

    def generalAssistantClicked(self):
        # code to activate general assistant
        Assistant_speak("How can I help?")
        time.sleep(1)
        while 1:
            voice_data = record_audio()
            respond(voice_data)

    def respond(voice_data):
        # pre-programmed responses
        if 'name' in voice_data:
            Assistant_speak('My name is Barry')
        elif 'what are you' in voice_data:
            Assistant_speak('I am your personal voice assistant. How may i help?')
        elif 'heads or tails' in voice_data:
            Assistant_speak('Huh, it landed on the side')
        elif 'date' in voice_data:
            Assistant_speak(ctime())
        elif 'reminders' in voice_data:
            service = authenticate_google()
            service = get_events(5, service)
        elif 'joke' in voice_data:
            Assistant_speak('knock knock... oh wait how did it go again')
        elif 'story' in voice_data:
            Assistant_speak('A long time ago, in a galaxy far, far away...')
        elif 'who made you' in voice_data or 'who built you' in voice_data or 'who created you' in voice_data:
            Assistant_speak('I was built by Owen')
            print('I was built by Owen')
        elif 'features' in voice_data:
            Assistant_speak('Here is a list of my features')
            print(
                'Google search, Location finder, Youtube, Weather, Event manager, time/date, flip a coin, tell a joke ')
        elif 'hello' in voice_data:
            day_time = int(strftime('%H'))
            if day_time < 12:
                Assistant_speak('Hello, Good morning')
            elif 12 <= day_time < 18:
                Assistant_speak('Hello, Good afternoon')
            else:
                Assistant_speak('Hello, Good evening')




    def googleSearchClicked(self):
        # code to search on google
        a = 1

    def findLocationClicked(self):
        # code to find a location
        a = 1

    def playMusicClicked(self):
        # code to play music
        a = 1

    def exitClicked(self):
        sys.exit(App.exec()) # exit the application

class RecordWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Record"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 200

        self.startRecButton = QPushButton()
        self.stopRecButton = QPushButton()
        self.transcribeButton = QPushButton()

        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("RecordIcon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.radioBox)
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.show()

    def createLayout(self):
        # radio buttons
        self.radioBox = QGroupBox("Choose file type")
        rBoxLayout = QVBoxLayout()

        self.r0 = QRadioButton("docx")
        self.r0.setText("Microsoft Word")
        self.r0.toggled.connect(lambda:self.radioState(self.r0))

        self.r1 = QRadioButton("pdf")
        self.r1.setText("PDF")
        self.r1.toggled.connect(lambda:self.radioState(self.r1))

        self.r2 = QRadioButton("txt")
        self.r2.setText("Text file")
        self.r2.toggled.connect(lambda:self.radioState(self.r2))

        rBoxLayout.addWidget(self.r0)
        rBoxLayout.addWidget(self.r1)
        rBoxLayout.addWidget(self.r2)

        self.radioBox.setLayout(rBoxLayout)

        # other buttons
        self.groupBox = QGroupBox("Recording")
        hBoxLayout = QVBoxLayout()

        self.startRecButton = QPushButton("START RECORDING", self)
        hBoxLayout.addWidget(self.startRecButton)
        self.startRecButton.setToolTip("Click to start recording")
        self.startRecButton.clicked.connect(self.record)
        self.startRecButton.setEnabled(False) # user cannot click this button until they select a radio button

        self.stopRecButton = QPushButton("STOP RECORDING", self)
        hBoxLayout.addWidget(self.stopRecButton)
        self.stopRecButton.setToolTip("Click to stop recording")
        self.stopRecButton.clicked.connect(self.stopRecording)
        self.stopRecButton.setEnabled(False) # user cannot click this button until they are recording
        
        self.transcribeButton = QPushButton("TRANSCRIBE", self)
        hBoxLayout.addWidget(self.transcribeButton)
        self.transcribeButton.setToolTip("Click to transcribe your recording")
        self.transcribeButton.clicked.connect(self.transcribe)
        self.transcribeButton.setEnabled(False) # user cannot click this button until they are done recording

        self.groupBox.setLayout(hBoxLayout)

    def radioState(self, b):
        if b.isChecked() == True:
            self.startRecButton.setEnabled(True)

    def record(self):
        self.startRecButton.setEnabled(False)
        self.stopRecButton.setEnabled(True)
        self.transcribeButton.setEnabled(False)

        # code to record

    def stopRecording(self):
        self.startRecButton.setEnabled(True)
        self.stopRecButton.setEnabled(False)
        self.transcribeButton.setEnabled(True)

    def transcribe(self):
        # code to transcribe
        a = 1

class ImportWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Import"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 200

        self.transcribeButton = QPushButton()
        self.startImpButton = QPushButton()

        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("ImportIcon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.show()

    def createLayout(self):
        self.groupBox = QGroupBox("Importing")
        hBoxLayout = QVBoxLayout()

        self.startImpButton = QPushButton("IMPORT", self)
        hBoxLayout.addWidget(self.startImpButton)
        self.startImpButton.setToolTip("Click to import a sound file")
        self.startImpButton.clicked.connect(self.imp)

        self.transcribeButton = QPushButton("TRANSCRIBE", self)
        hBoxLayout.addWidget(self.transcribeButton)
        self.transcribeButton.setToolTip("Click to transcribe an imported sound file")
        self.transcribeButton.clicked.connect(self.imp)
        self.transcribeButton.setEnabled(False) # user cannot click this button until they have imported something

        self.groupBox.setLayout(hBoxLayout)

    def imp(self):
        # code to import
        importSuccess = True
        
        # code here to import and check its successful
        # if not, set importSuccess to false

        if(importSuccess):
            self.transcribeButton.setEnabled(True)

    def transcribe(self):
        # code to transcribe imported file
        a = 1

class LiveWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Live Transcription"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 200

        self.liveTranscribeButton = QPushButton()

        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("LiveIcon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.show()

    def createLayout(self):
        self.groupBox = QGroupBox("Transcribe your speech live")
        hBoxLayout = QVBoxLayout()

        self.liveTranscribeButton = QPushButton("LIVE TRANSCRIBE", self)
        hBoxLayout.addWidget(self.liveTranscribeButton)
        self.liveTranscribeButton.setToolTip("Click to start live transcribing")
        self.liveTranscribeButton.clicked.connect(self.liveTranscribe)

        self.groupBox.setLayout(hBoxLayout)

    def liveTranscribe(self):
        # code to live transcribe
        a = 1

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec())

