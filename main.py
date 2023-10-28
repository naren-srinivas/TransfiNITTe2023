from modules import *

# Build the AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name
        self.empty = 0
        self.text = ''
        self.username = ''
        self.onchecker = 0
        self.language = 'en'

    def speech_to_text(self):
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


    @staticmethod
    def text_to_speech(text):
        print("bhAI --> ", text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        

    def wake_up(self, text):
        return True if self.name in text.lower() else False
    
    def sleep(self, text):
        return True if ('thank you' or 'thanks' or 'thank') in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')
    
    def change_username(self) :
        while True :
            self.text_to_speech('Bhai, tell your username')
            self.speech_to_text()
            if self.empty != 0 :
                self.username = self.text 
                self.text_to_speech('Welcome ' + self.username + ' Bhai')
                break
            else :
                pass
    def change_language(self) :
        while True :
            self.text_to_speech('Bhai, what is your preferred language')
            self.speech_to_text()
            if self.empty != 0 :
                    if 'tamil' in self.text.lower() :
                        self.language = 'ta'
                    elif 'hindi' in self.text.lower() :
                        self.language = 'hi'
                    elif 'english' in self.text.lower() :
                        self.language = 'en'
                    else :
                        self.text_to_speech('The language mentioned is not available')
                        break
                    self.text_to_speech('You can talk in your prefered language now bhai')
                    break
            else :
                pass

# Run the AI
if __name__ == "__main__":
    
    ai = ChatBot(name="bhai")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    while True:
        ai.speech_to_text()

        if ai.onchecker > 2 :
            ai.text_to_speech('Bhai, I am drowsy... Going to sleep')
            break
        elif ai.sleep(ai.text):
            res = 'Anything for you Bhai'
            ai.text_to_speech(res)
            break
        elif ai.empty == 1:
            #res = "Arey Bhai, what can I do for you?"
        
            ## action time
            if "time" in ai.text:
                res = ai.action_time()
                ai.onchecker = 0
            
            ## respond politely
            elif any(i in ai.text for i in ["thank","thanks"]):
                res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","peace out!"])
                ai.onchecker = 0
            
            #username
            elif ('username' or 'user name') in ai.text.lower() :
                ai.change_username()
                ai.onchecker = 0
                continue
            elif 'change language' in ai.text.lower() :
                ai.change_language()
                ai.onchecker = 0
                continue
                
            ## conversation
            else:   
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find(">> bot ")+6:].strip()
                if 'assistant' in res :
                    res = res[res.find('assistant')+11:].strip()
                    

            ai.text_to_speech(res)
            ai.onchecker = 0

        
        else :
            ai.onchecker += 1
            pass
        print(ai.onchecker)
        