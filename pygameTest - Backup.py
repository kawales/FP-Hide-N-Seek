import pygame
from pygame.sprite import Group
import os
import random
#from typing import Any


class GameManager():
    def __init__(self) -> None:
        self.startTime=0
        self.gameLength=0
        self.playing=False
        pass

    def start(self,gameLength=100):
        self.playing=True
        self.startTime=0
        self.gameLength=gameLength
        
    def stop(self):
        self.startTime=self.gameLength
        
    def update(self):
        if(self.startTime>=self.gameLength and self.playing==True):
            global phase
            self.playing=False
            phase+=1
            pass
        self.startTime+=1
        draw_text(screen,"Time left:"+str(round((self.gameLength-self.startTime)/10)),30,120,20)



class Finder(pygame.sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.sprites = list()
        self.sprites.append(pygame.transform.scale(pygame.image.load("pointer.png"),(40,40)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("pointer2.png"),(40,40)))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.left+=600
        self.rect.top+=400
        self.timer = 0
        self.hidden=True
    
    def update(self):
        global phase
        if(phase!=6):
            return
        self.timer+=1
        if(self.timer%20==0):
            self.image=self.sprites[0]
        elif(self.timer%10==0):
            self.image=self.sprites[1]
        for e in pygame.event.get():
            if(e.type==pygame.KEYDOWN and e.key==pygame.K_d):
                self.rect.left+=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_a):
                self.rect.left-=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_s):
                self.rect.top+=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_w):
                self.rect.top-=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE):
                global props 
                for prop in props:
                    if(self.rect.colliderect(prop)):
                        ding.play()
                        global endscreenText
                        endscreenText="Seeker won! Play again?"
                        phase+=1
                        return
                if(phase!=-1):
                    global GM
                    GM.startTime+=50
                    wrong.play()
            elif (e.type==pygame.QUIT):
                pygame.quit()


class Hider(pygame.sprite.Sprite):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.sprNames = os.listdir('TilesUsed')
        self.sprites = list()
        self.filteredSprNames=self.sprNames
        for spr in self.sprNames:
            if("Long" in spr):
                self.sprites.append(pygame.transform.scale(pygame.image.load("TilesUsed/"+spr),(40,80)))
            else:
                self.sprites.append(pygame.transform.scale(pygame.image.load("TilesUsed/"+spr),(40,40)))
        self.currentSpr=0
        self.image = self.sprites[self.currentSpr]
        self.rect = self.image.get_rect()
        # centriranje igraca
        self.rect.left+=600
        self.rect.top+=400
        self.timer = 0
        self.hidden=True
    
    
    def changeSpr(self,mov=1):
        self.currentSpr+=mov
        if(self.currentSpr>len(self.sprites)-1):
                self.currentSpr=0
        elif(self.currentSpr<0):
                self.currentSpr=len(self.sprites)-1
        print(self.sprNames[self.currentSpr])
        while(self.sprNames[self.currentSpr] not in self.filteredSprNames):
            self.currentSpr+=1
            if(self.currentSpr>len(self.sprites)-1):
                    self.currentSpr=0
            elif(self.currentSpr<0):
                    self.currentSpr=len(self.sprites)-1
            print(self.currentSpr)
            print(len(self.sprNames))

        self.image=self.sprites[self.currentSpr]
        self.rect.height = self.image.get_rect().height

    def update(self):
        global phase
        if(phase!=4):
            return
        self.timer+=1
        for e in pygame.event.get():
            if(e.type==pygame.KEYDOWN and e.key==pygame.K_d):
                self.rect.left+=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_a):
                self.rect.left-=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_s):
                self.rect.top+=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_w):
                self.rect.top-=40
                move.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_RIGHT):
                self.changeSpr()
                ding.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_LEFT):
                self.changeSpr(-1)
                ding.play()
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_DOWN):
                self.filteredSprNames=list(filter(lambda x: "0" in x or "1" in x,self.sprNames))
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_UP):
                self.filteredSprNames=list(filter(lambda x: "0" in x or "2" in x,self.sprNames))
            elif(e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE):
                global GM 
                GM.stop()
                ding.play()
            elif (e.type==pygame.QUIT):
                pygame.quit()
        
def draw_text(surf, text, size, x, y,c=(0,0,0)):
    font = pygame.font.Font("tinypixel.otf", size)
    text_surface = font.render(text, True,c)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def transitionScreen(text):
    screen.fill((0,0,0))
    draw_text(screen,text,30,600,300,(255,255,255))
    
    pygame.draw.rect(screen,(0,255,0),pygame.Rect(500,350,200,75))

    draw_text(screen,"Press P",30,600,375)


# pygame setup
pygame.init()
pygame.display.set_caption("HIDE N SEEK")
pygame.mixer.init()
maps=["map1.png","map2.png"]
currentMap = maps[ random.randint(0,len(maps)-1)]
bg=  pygame.transform.scale(pygame.image.load(currentMap),(1200,800))
phase=0
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
running = True
finRender = pygame.sprite.RenderPlain()
props = pygame.sprite.RenderPlain()
fin = Finder()
hid = Hider()
props.add(hid)
finRender.add(fin)
move = pygame.mixer.Sound("move.wav")
wrong = pygame.mixer.Sound("lose.wav")
ding = pygame.mixer.Sound("pick.wav")
endscreenText="""Hiders have won! Start new game?"""
GM = GameManager()
#print(os.listdir('TilesUsed'))
while running:
    pygame.time.Clock().tick(60)
    if(phase==0):
        transitionScreen("HIDE N SEEK")
        currentMap = maps[ random.randint(0,len(maps)-1)]
        bg=  pygame.transform.scale(pygame.image.load(currentMap),(1200,800))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and  event.key == pygame.K_p:
                phase+=1
    elif(phase==7):
        transitionScreen(endscreenText)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and  event.key == pygame.K_p:
                phase=0
                endscreenText="Hiders have won! Start new game?"
                fin.rect.topleft=(600,400)
                hid.rect.topleft=(600,400)
    elif(phase==1):
        transitionScreen("SEEKER LOOK")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and  event.key == pygame.K_p:
                phase+=1
                GM.start()
    elif(phase==3):
        transitionScreen("HIDE!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and  event.key == pygame.K_p:
                phase+=1
                GM.start(300)
    elif(phase==5):
        transitionScreen("SEEKER FIND!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and  event.key == pygame.K_p:
                phase+=1
                GM.start(300)
    elif(phase==2 or phase==4 or phase==6):
        finRender.update()
        props.update()
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        screen.blit(bg,bg.get_rect())
        #screen.blit(ball,(0,100))
        # RENDER YOUR GAME HERE
        finRender.draw(screen)
        props.draw(screen)
        #draw_text(screen,"bla",20,200,200)
        GM.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()