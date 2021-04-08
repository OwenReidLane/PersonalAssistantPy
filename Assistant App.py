from __future__ import print_function
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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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


def respond(voice_data):
    #pre-programmed responses
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
        print('Google search, Location finder, Youtube, Weather, Event manager, time/date, flip a coin, tell a joke ')
    elif 'hello' in voice_data:
        day_time = int(strftime('%H'))
        if day_time < 12:
            Assistant_speak('Hello, Good morning')
        elif 12 <= day_time < 18:
            Assistant_speak('Hello, Good afternoon')
        else:
            Assistant_speak('Hello, Good evening')

       #webCommands
    elif 'search' in voice_data:
        #Say search followed by what you want to search
        search = record_audio('')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        Assistant_speak('Is this the thing your looking for?' + search)

    elif 'Maps' in voice_data:
        #in maps search" followed by location
        location = record_audio('')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        Assistant_speak('lets go' + location)

    elif 'Youtube' in voice_data:
        url = 'https://www.youtube.com'
        webbrowser.get().open(url)
        Assistant_speak('Opening Youtube')
        time.sleep(3)

    elif "weather" in voice_data:
        api_key = "8ef61edcf1c576d65d836254e11ea420"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        Assistant_speak("whats the city name")
        city_name = record_audio()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]
            Assistant_speak(" Temperature in kelvin unit is " +
                  str(current_temperature) +
                 "\n description  " +
                  str(weather_description))
            print(" Temperature in kelvin unit = " +
                  str(current_temperature) +
                  "\n description = " +
                  str(weather_description))
        else:
            speak(" City Not Found ")

    if 'exit' in voice_data or 'quit' in voice_data:
        Assistant_speak('Good bye, Have a nice day')
        exit()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        Assistant_speak(f'You have {n} upcoming events')
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':

    time.sleep(1)
    Assistant_speak('How Can I Help')
    while 1:
        voice_data = record_audio()
        respond(voice_data)
