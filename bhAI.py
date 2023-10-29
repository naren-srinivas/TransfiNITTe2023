import speech_recognition as sr
from gtts import gTTS 
import os
import time
from playsound import playsound

class ChatBot():
    def __init__(self, lang):
        print(f"---starting up {lang} bhAI---")
        self.lang = lang
        self.success = False
        self.transcription = ''

    def speak(myText):
        print(f"Bhai: {myText}")

        file = "temp.mp3"
        myobj = gTTS(text=myText, lang='en', slow=False) 
        myobj.save(file)

        playsound(file)
        time.sleep(5)
        os.remove(file)

    def listen(self):
        '''
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic, 3, 5)
        try:
            self.transcription = recognizer.recognize_google(audio, language = "en-IN")
            self.success = 1
            print("You: ", self.transcription)
        except:
            if not self.transcription == '' :
                print("Could not get you, repeat louder")
                self.success = 0
        '''
        self.success = True
        self.transcription = input("You: ")
        print("You: ", self.transcription)

    def wakeUp(self, query):
        if "are bhai" in query:
            self.speak("How may I help you, bhai?")

    def sleep(self, query):
        if ("thanks" or "thank") in query:
            self.speak("See you later bhai. You will not be missed.")

#set of all languages
languages = {"tamil","english","hindi","german","french","russian","marathi","gujarati"}

#Bot whichever is requested by the user, essentially the language
activeBhai = ChatBot(lang="English")

if __name__ == "__main__":

    while 1:
        activeBhai.listen()
        speech = activeBhai.transcription
        activeBhai.speak("how the fuck are you this dumb")
        if activeBhai.success:
            activeBhai.wakeUp(query = speech)
            activeBhai.sleep(query = speech)

            for lang in languages:
                if lang in speech and lang in ("tamil", "english", "hindi"):
                    activeBhai.speak(f"Do you want to switch to {lang}?")

                    activeBhai.listen()



