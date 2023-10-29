import pygame as pg
import sys
from main import *
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
class App :
    #nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    def __init__(self) :
        pg.init()
        pg.font.init()
        self.info=pg.display.Info()

        self.screen = pg.display.set_mode((self.info.current_w*0.6,self.info.current_h*0.6),pg.RESIZABLE)

        pg.display.set_caption('bhAI')
        self.screen.fill((20,20,20))
        pg.display.flip()
        self.metext = '23'
        self.aitext = '43'
        self.font = pg.font.Font('freesansbold.ttf',32)
        self.text1 = self.font.render(self.metext, True, white, blue)
        self.text2 = self.font.render(self.aitext,True,white,blue)
        self.textRect1 = self.text1.get_rect()
        self.textRect2 = self.text2.get_rect()
        self.textRect1.center = (100,220)
        self.textRect2.center = (100,330)
        self.img = pg.image.load('mansoorbhAI.png')
        self.img = pg.transform.smoothscale(self.img, (150, 150)) 
        self.bgimg = pg.image.load('mansoorbg.jpg')
        self.size=self.screen.get_size()

        
        
        self.clock = pg.time.Clock()

    def update(self,waken) :
        if waken == False :
            ai.initsession()
        else :
            ai.replyiter()
        self.metext = 'You : ' + ai.text
        self.aitext = 'bhAI : ' + ai.res
        self.screen.fill(pg.Color(20,20,20))
        self.text1 = self.font.render(self.metext, True, white, (18,18,18))
        self.text2 = self.font.render(self.aitext, True, white, (18,18,18))
        self.screen.blit(pg.transform.scale(self.bgimg,self.size),(0,0))
        self.screen.blit(self.text1,self.textRect1)
        self.screen.blit(self.text2,self.textRect2)
        self.screen.blit(self.img,(370,0))
        pg.display.update()

        pass

    def get_time(self) :
        self.time = pg.time.get_ticks()*0.001

    def check_event(self) :
        for i in pg.event.get() :
            if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    def run(self) :
        while True and not ai.loopbreak :
            self.check_event()
            self.get_time()
            self.update(ai.waken)
            

if __name__ == '__main__' :
    ai = ChatBot(name="bhai")
    #nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    #os.environ["TOKENIZERS_PARALLELISM"] = "true"


    app = App()
    app.run()