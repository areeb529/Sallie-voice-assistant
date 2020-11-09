import speech_recognition as sr
import pyttsx3
from time import ctime
import webbrowser
import time
import random
import os

r = sr.Recognizer()

speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)
rate = speaker.getProperty('rate')
speaker.setProperty('rate', 150)


class Person:
    name = ''

    def set_name(self, name):
        self.name = name


def record_audio(query=False):
    with sr.Microphone() as source:     # microphone as source
        if query:
            sallie_speak(query)
        audio = r.listen(source)    # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            sallie_speak('Sorry, I did not get that')
        except sr.RequestError:
            # error: recognizer is not connected
            sallie_speak('Sorry, I cannot process your request at the moment')
        print(f"Me: {voice_data.lower()}")  # print what user said
        return voice_data


def sallie_speak(audio_string):
    print('Saillie: ' + audio_string)
    speaker.say(audio_string)
    speaker.runAndWait()


def there_exists(words):
    for word in words:
        if word in voice_data:
            return True


def respond(voice_data):
    # 1: greeting
    if there_exists(['hello', 'hi', 'hey']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                     f"I'm listening {person_obj.name}", f"hello {person_obj.name}", f"It's really good to hear from you {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        sallie_speak(greet)

    if there_exists(["how are you", "how are you doing"]):
        sallie_speak(f"I'm very well, thanks for asking {person_obj.name}")

    if there_exists(["what's up"]):
        sallie_speak(
            "Not much! Just been looking into ways to stay healthy. I learned that wearing a mask in public saves lives")
        sallie_speak("Hope you are rocking one!")

    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            sallie_speak("my name is Sallie")
        else:
            sallie_speak("my name is Sallie. what's your name?")

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        sallie_speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object

    if there_exists(["No thats wrong name"]):
        sallie_speak("what should I call you?")
        person_name = record_audio()
        sallie_speak(f"Nice to meet you {person_name}")

    # 4: time
    if there_exists(["what's the time", "tell me the time", "what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = "12"
        else:
            hours = time[0]
        minutes = time[1]
        time = f"{hours} {minutes}"
        sallie_speak(time)

    if there_exists(["exit", "quit", "goodbye"]):
        sallie_speak("going offline")
        exit()
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


person_obj = Person()
time.sleep(1)
sallie_speak('How can I help you?')
while 1:
    voice_data = record_audio()     # get the voice input
    respond(voice_data)     # respond
