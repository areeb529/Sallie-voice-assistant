import speech_recognition as sr
import pyttsx3
from time import ctime
import webbrowser
import time
import random
import os
from googletrans import Translator

r = sr.Recognizer()
translator = Translator()

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
            
        except sr.UnknownValueError:
            sallie_speak('Sorry, I did not get that')
        except sr.RequestError:
            # error: recognizer is not connected
            sallie_speak('Sorry, I cannot process your request at the moment')
        print(f"Me: {voice_data.lower()}")  # print what user said
        return voice_data.lower()


def sallie_speak(audio_string):
    print('Sallie: ' + audio_string)
    speaker.say(audio_string)
    speaker.runAndWait()


def there_exists(list_of_words):
    for word in list_of_words:
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
        person_obj.set_name(person_name)  # remember name in person object

    if there_exists(["no that's wrong name"]):
        sallie_speak("what should I call you?")
        person_name = record_audio()
        sallie_speak(f"Nice to meet you {person_name}")

    # 4: time
    if there_exists(["what time is it", "tell me the time","what's the time"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = "12"
        else:
            hours = time[0]
        minutes = time[1]
        time = f"{hours} {minutes}"
        sallie_speak(time)
    
    # 5: search google - ask: search for mountains
    if there_exists(["search for"]) and ('youtube' not in voice_data):
        search_term = voice_data.split("for")[-1].strip()
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        sallie_speak(f'Here is what I found for {search_term} on google')
        
    # 6: search youtube - ask: search for python programming on youtube
    if there_exists(["youtube"]):
        search = voice_data.split("for")[-1].strip()
        search_term = search.split("on")[0].strip()
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        sallie_speak(f'Here is what I found for {search_term} on youtube')
        
    # 7: search location - ask: find location, search for location etc
    if there_exists(["location"]):
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        sallie_speak('Here is the location for ' + location)
    
    # 8: Translator
    if there_exists(["translate"]):
        to_translate_text = record_audio('What do you want to translate')
        translated_text = translator.translate(to_translate_text,dest="en")
        sallie_speak(translated_text.text)

    # 9: Exit    
    if there_exists(["exit", "quit", "goodbye", "bye"]):
        sallie_speak("going offline")
        exit()


person_obj = Person()
time.sleep(1)
sallie_speak('How can I help you?')
while 1:
    voice_data = record_audio()     # get the voice input
    respond(voice_data)     # respond
