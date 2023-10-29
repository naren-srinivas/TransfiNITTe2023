from modules import *

# Build the AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name
        self.empty = 0
        self.text = ''
        self.res = ''
        self.username = ''
        self.onchecker = 0
        self.language = 'en'
        self.waken = False
        self.loopbreak = False
        self.nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
        os.environ["TOKENIZERS_PARALLELISM"] = "true"

    def listen(self):
        recognizer = sr.Recognizer()
        trans = Translator()
        with sr.Microphone() as mic:
            print("listening...")
            #recognizer.adjust_for_ambient_noise(mic)
            try :
                audio = recognizer.listen(mic, 2, 5)
            except : 
                print('No signal')
        try:
            self.untranstext = recognizer.recognize_google(audio, language = self.language + "-IN")
            if self.language in ('ta','hi'):
                print(self.untranstext)
                output = trans.translate(self.untranstext,src=self.language,dest = 'en')
                self.text = output.text
            else :
                self.text = self.untranstext
            self.empty = 1
            print("me --> ", self.text) 
        except:
            if not self.text == '' :
                print("me -->  ERROR")
                self.empty = 0


    def speak(self,text):
        print("bhAI --> ", text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

        '''file = "temp.mp3"
        myobj = gTTS(text=text, lang=self.language, slow=False) 
        myobj.save(file)

        playsound(file)
        print('playing sound using playsound')
        time.sleep(5)
        os.remove(file)'''

        

    def wake_up(self, text):
        return True if self.name in text.lower() else False
    
    def sleep(self, text):
        return True if 'thank you bhai' in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
    
    def change_username(self) :
        while True :
            self.res = 'Bhai, tell your username'
            self.speak(self.res)
            self.listen()
            if self.empty != 0 :
                self.username = self.text 
                self.res = 'Welcome ' + self.username + ' Bhai'
                self.speak(self.res)
                break
            else :
                pass
    def change_language(self) :
        while True :
            self.res = 'Bhai, what is your preferred language'
            self.speak(self.res)
            self.listen()
            if self.empty != 0 :
                    if 'tamil' in self.text.lower() :
                        self.language = 'ta'
                    elif 'hindi' in self.text.lower() :
                        self.language = 'hi'
                    elif 'english' in self.text.lower() :
                        self.language = 'en'
                    else :
                        self.res = 'The language mentioned is not available'
                        self.speak(self.res)
                        continue
                    self.res = 'You can talk in your prefered language now bhai'
                    self.speak(self.res)
                    break
            else :
                pass
    def SpotiBhai(self, songName):
            username = 'z6za498eyl7wcwpubtphuoxt3'
            clientID = '07248fdd5d3e42a581d51bbbfbce4e24'
            clientSecret = 'd5bb458e3909486283715cca2f21073b'
            redirectURI = 'http://google.com/'

            oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
            token_dict = oauth_object.get_access_token()
            token = token_dict['access_token']
            spotifyObject = spotipy.Spotify(auth=token)
            user = spotifyObject.current_user()
            # To print the response in readable format.
            print(json.dumps(user,sort_keys=True, indent=4))

            print("Welcome to the project, " + user['display_name']) 
            results = spotifyObject.search(songName, 1, 0, "track") 
            songs_dict = results['tracks'] 
            song_items = songs_dict['items'] 
            song = song_items[0]['external_urls']['spotify'] 
            webbrowser.open(song) 
            self.res = 'Song has opened in your browser.'
            self.speak(self.res)

    def initsession(self) :
        self.listen()
        if self.wake_up(self.text) :
            self.waken = True
            self.res = "Welcome Bhai, what can i call you"
            self.speak(self.res)
            while True :
                self.listen()
                if self.empty != 0 :
                    self.username = self.text 
                    self.res = 'Welcome ' + self.username
                    self.speak(self.res)
                    break
               
    def replyiter(self) :
        self.listen()   

        if self.onchecker > 2 :
            self.res = 'Bhai, I am drowsy... Going to sleep'
            self.speak(self.res)
            self.loopbreak = True
        elif self.sleep(self.text):
            self.res = 'Anything for you Bhai'
            self.speak(self.res)
            self.loopbreak = True
        elif self.empty == 1:
        
            ## action time
            if "time " in self.text:
                self.res = "The time now is " + self.action_time()
                self.onchecker = 0
            
            ## respond politely
            elif any(i in self.text for i in ["thank","thanks"]):
                self.res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","peace out!"])
                self.onchecker = 0
            
            #username
            elif ('username' or 'user name') in self.text.lower() :
                self.change_username()
                self.onchecker = 0
                
            elif ('change' in self.text.lower() and 'language' in self.text.lower()) :
                self.change_language()
                self.onchecker = 0
                
            elif ("music" or "song" or "spotify") in self.text.lower():
                self.res = "Which song do you want to play?"
                self.speak(self.res)
                while True :
                    self.listen()
                    if self.empty != 0 :
                        self.SpotiBhai(self.text)
                        break
                    else :
                        pass
            ## conversation
            else:   
                chat = self.nlp(transformers.Conversation(self.text), pad_token_id=50256)
                self.res = str(chat)
                self.res = self.res[self.res.find(">> bot ")+6:].strip()
                if 'assistant' in self.res :
                    self.res = self.res[self.res.find('assistant')+11:].strip()
                self.speak(self.res)
                self.onchecker = 0

        
        else :
            self.onchecker += 1
            pass     

# Run the AI
'''if __name__ == "__main__":
    
    ai = ChatBot(name="bhai")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
 
    ai.initsession()

    while ai.waken:
        ai.replyiter()'''
        
        