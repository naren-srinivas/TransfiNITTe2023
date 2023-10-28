from modules import *

# Build the AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name
        self.empty = 0
        self.text = ''
        self.username = ''
        self.iterations = []

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            #recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic, 2, 5)
        try:
            self.text = recognizer.recognize_google(audio, language = "en-IN")
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
        return True if 'thank you bhai' in text.lower() else False

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


# Run the AI
if __name__ == "__main__":
    
    ai = ChatBot(name="bhai")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    while True:
        ai.speech_to_text()

        ## wake up
        if ai.sleep(ai.text) or (ai.text == ''):
            res = 'Anything for you Bhai'
            ai.text_to_speech(res)
            break
        elif ai.wake_up(ai.text) is True and ai.empty == 1:
            #res = "Arey Bhai, what can I do for you?"
        
            ## action time
            if "time" in ai.text:
                res = ai.action_time()
            
            ## respond politely
            elif any(i in ai.text for i in ["thank","thanks"]):
                res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","peace out!"])
            
            #username
            elif 'username' in ai.text :
                ai.change_username()
                ai.iterations.append(1)
                continue
            ## conversation
            else:   
                chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find(">> bot ")+6:].strip()
                if 'assistant' in res :
                    res = res[res.find('assistant')+11:].strip()

            ai.text_to_speech(res)
            ai.iterations.append(1)
        
        else :
            pass
        