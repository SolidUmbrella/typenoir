from ast import parse
from os import stat
from sre_constants import ANY
import pygame
from pygame import mixer
import random
from constants import BLACK, LEVEL_NOT_ZERO, LEVEL_ZERO, WHITE, PAPER
from utils import drawBoard, drawText, drawTitleText, drawBackground
import gtts
from playsound import playsound
import json



class Scene:
    def __init__(self):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def input(self,sm):
        pass
    def update(self,sm):
        pass
    def present(self,sm):
        pass
class TitleScene(Scene):
    def __init__(self, state):
        super().__init__()
        self.name = 'Title'
        self.state = state
    def input(self, sm, screen, elements, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(MainMenuScene(self.state))
        if keys[pygame.K_q]:
            sm.pop()
    def update(self, sm, elements):
        pass
    def present(self, sm, screen, elements):
        drawBackground(screen, BLACK)
        drawTitleText(screen, 'type_noir', 350, 250)
        drawText(screen, 'press enter...', 385, 225, WHITE, BLACK)
class MainMenuScene(Scene):
     def __init__(self, state):
         super().__init__()
         self.state = state
         self.index = 0
         self.elements = []
         self.name = 'MainMenu'
     def input(self, sm, screen, elements,event):
        self.elements = elements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        if keys[pygame.K_UP] and self.index != 0:
            self.elements[self.index].selected = False
            self.elements[self.index].draw(screen)
            self.index -= 1
            self.elements[self.index].selected = True
            self.elements[self.index].draw(screen)
        if keys[pygame.K_DOWN] and self.index != len(self.elements) - 1:
            self.elements[self.index].selected = False
            self.elements[self.index].draw(screen)
            self.index += 1
            self.elements[self.index].selected = True
            self.elements[self.index].draw(screen)
        if keys[pygame.K_RETURN]:
            if self.elements[self.index].text == "new game":
                sm.push(GameScene(self.state))
            elif self.elements[self.index].text == "options":
                sm.push(OptionsMenuScene(self.state))
            elif self.elements[self.index].text == "how to":
                sm.push(GameGuideScene())
     def update(self, sm, elements):
        pass
     def present(self, sm, screen, elements):
         self.elements = elements
         drawBackground(screen, BLACK)
         drawTitleText(screen, 'type_noir', 350, 250)
         # create main menu
         
         if len(self.elements) > 0:
            for e in self.elements:
                # if e.rect.collidepoint(pygame.mouse.get_pos()):
                #     e.hovered = True
                # else:
                #     e.hovered = False
                e.draw(screen)

class OptionsMenuScene(Scene):
     def __init__(self, state):
         super().__init__()
         self.state = state
         self.index = 0
         self.elements = []
         self.name = 'OptionsMenu'
     def input(self, sm, screen, elements,event):
        self.elements = elements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        if keys[pygame.K_UP] and self.index != 0:
            print(self.elements[self.index].text)
            self.elements[self.index].selected = False
            self.elements[self.index].draw(screen)
            self.index -= 1
            self.elements[self.index].selected = True
            self.elements[self.index].draw(screen)
        if keys[pygame.K_DOWN] and self.index != len(self.elements) - 1:
            print(self.elements[self.index].text)
            self.elements[self.index].selected = False
            self.elements[self.index].draw(screen)
            self.index += 1
            self.elements[self.index].selected = True
            self.elements[self.index].draw(screen)
        if keys[pygame.K_RETURN]:
            if self.elements[self.index].text == "difficulty":
                if self.state.difficulty == 'EASY':
                    self.state.setDifficulty('NOT EASY')
                else:
                    self.state.setDifficulty('EASY')

     def update(self, sm, elements):
        pass
     def present(self, sm, screen, elements):
         self.elements = elements
         drawBackground(screen, BLACK)
         drawText(screen, self.state.difficulty, 150, 35, WHITE, BLACK)
         drawTitleText(screen, 'type_noir', 350, 250)
         # create main menu
         
         if len(self.elements) > 0:
            for e in self.elements:
                # if e.rect.collidepoint(pygame.mouse.get_pos()):
                #     e.hovered = True
                # else:
                #     e.hovered = False
                e.draw(screen)

class GameScene(Scene):
    def __init__(self, state):
        super().__init__()
        # self.words = ['maroon', 'bumfuzzle', 'asunder', 'bumpersnoot', 'chimpanzee', 'churro', 'dongle', 'fubsy', 'sozzled', 'hedgehog']
        mixer.Channel(0).play(mixer.Sound('assets/shady_business.mp3'))
        mixer.Channel(0).set_volume(0.1)
        self.state = state
        level  = LEVEL_ZERO
        if self.state.difficulty == 'NOT EASY':
            level = LEVEL_NOT_ZERO 
        self.words = level
        self.word = ""
        # parsed = json.loads(self.word)
        # word = parsed['word']
        # hint = parsed['hint']
        # # for key in self.word:
        # #     word = key
        # #     hint = self.word[key]
        # self.word = word
        self.hint = ""
        self.name = 'Game'
        self.playWord()
    def input(self, sm, screen, elements, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        if keys[pygame.K_RSHIFT]:
            self.playWord()
        if keys[pygame.K_LSHIFT]:
            self.playHint()
        for e in elements:
            e.handle_event(event)
        pygame.display.flip()
    def update(self, sm, elements):
        if self.state.time > 0:
            for e in elements:
                e.update()
    def present(self, sm, screen, elements):
        #  drawBackground(screen, (242,238,203))
         pad_seconds = ""
         if self.state.getSeconds() < 10:
             pad_seconds = "0"+str(self.state.getSeconds())
         else:
             pad_seconds = str(self.state.getSeconds())
         drawText(screen, 'Score: ' + str(self.state.score), 10, 10, BLACK, WHITE)
         drawText(screen, str(self.state.getMinutes())+":"+pad_seconds, 10, 40, BLACK, WHITE)
         if self.state.time > 0:
            if len(self.words) == 0:
                sm.push(GameOverScene(self.state))
            for e in elements:
                e.draw() 
         else:
            sm.push(GameOverScene(self.state))
         pygame.display.flip()
    def removeWord(self):
        if len(self.words) > 0:
            for i in range(len(self.words)):
                parsed = json.loads(self.words[i])
                if self.word == parsed['word']:
                    del self.words[i]
                    break   
            print(len(self.words))  
    def playWord(self):
        if len(self.words) > 0:
            self.word = random.choice(self.words)
            parsed = json.loads(self.word)
            word = parsed['word']
            hint = parsed['hint']
            # for key in self.word:
            #     word = key
            #     hint = self.word[key]
            self.word = word
            self.hint = hint
            print(self.word)
            print(self.hint)
            tts = gtts.gTTS(self.word)
            print('word='+self.word)
            tts.save('word.mp3')
            playsound('word.mp3')  
    def playHint(self):
        tts = gtts.gTTS(self.hint)
        tts.save('hint.mp3')
        playsound('hint.mp3')

class GameOverScene(Scene):
     def __init__(self, state):
        super().__init__()
        self.state = state
        self.name = 'GameOver'
        self.assesment = None
        # word_count = len(LEVEL_ZERO)
        if self.state.score < 2:
            self.assesment = "Poor..."
        elif self.state.score < 4:
            self.assesment = "Better!"
        elif self.state.score < 5:
            self.assesment = "Okay."
        elif self.state.score < 6:
            self.assesment = "You passed."
        elif self.state.score == 7:
            self.assesment = "Perfect!"
     def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        print('level select menu input')
     def update(self, sm, elements):
        print('level select menu update')
     def present(self, sm, screen, elements):
         drawBackground(screen, BLACK)
         drawText(screen, self.assesment, 450, 310, WHITE, BLACK)
         drawText(screen, 'final score: '+str(self.state.score), 450, 330, WHITE, BLACK)
         drawText(screen,'game over', 450, 350, WHITE, BLACK)

class LevelSelectScene(Scene):
     def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        print('level select menu input')
     def update(self, sm):
        print('level select menu update')
     def present(self, sm):
        print('level select menu present')

class GameGuideScene(Scene):
     def __init__(self):
        super().__init__()
        self.name = "Guide"
     def input(self, sm, screen, elements, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sm.pop()
        print('level select menu input')
     def update(self, sm, elements):
        print('level select menu update')
     def present(self, sm, screen, elements):
         drawBackground(screen, PAPER)
         drawText(screen, 'Instructions:', 450, 310, BLACK, WHITE)
         drawText(screen, "Spell the word you hear.", 450, 330, BLACK, WHITE)
         drawText(screen,'Use Right Shift hear it again.', 450, 350, BLACK, WHITE)
         drawText(screen,'And Left Shift for a hint.', 450, 370, BLACK, WHITE)


class SceneManager(Scene):
    def __init__(self, state):
        self.scenes = []
    def isEmpty(self):
        return len(self.scenes) == 0
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()
    def input(self,screen, elements,event):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self,screen, elements,event)
        pygame.display.flip()
    def update(self, elements):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, elements)
    def present(self, screen, elements):
        if len(self.scenes) > 0:
            self.scenes[-1].present(self, screen, elements)
        pygame.display.flip()
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()     
    def set(self, scene):
        while len(self.scenes) > 0:
            self.pop()
        self.push(scene)
    def getCurrentScene(self):
        return self.scenes[-1]