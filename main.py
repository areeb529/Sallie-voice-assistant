import speech_recognition as sr
import webbrowser
import time
import os
import random
import pyttsx3
from time import ctime

r = sr.Recognizer()

speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
rate = speaker.getProperty('rate')
speaker.setProperty('rate', 173)

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            sallie_speak(ask)
            print(ask)
        # Capture mic data
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            sallie_speak('Sorry, I did not get that')
        except sr.RequestError:
            sallie_speak('Sorry, I cannot process your request at the moment')
        return voice_data


def sallie_speak(audio_string):
    print('Computer: ' + audio_string)
    speaker.say(audio_string)
    speaker.runAndWait()


def respond(voice_data):
    if 'what is your name' in voice_data:
        sallie_speak('My name is Sallie')
        print('My name is Sallie')
    if 'what time is it' in voice_data:
        sallie_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        sallie_speak('Here is what I found for ' + search + '...')
        print('Here is what I found for ' + search + '...')
    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        sallie_speak('Here is the location for ' + location)
        print('Here is the location for ' + location)
    if 'exit' in voice_data:
        sallie_speak('Thank You')
        print('Thank you!')
        exit()


time.sleep(1)
sallie_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)

