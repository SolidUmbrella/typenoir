from tkinter.tix import Tree
import pygame
import time
from engine import Entity, Animation, Position
from constants import WHITE, BLACK

cursor = pygame.image.load('assets/cursor.png')
cursor_blink = pygame.image.load('assets/cursor_blink.png')

def drawBackground(screen, color):
    screen.fill(color)

def drawTitleText(screen, text, x, y):
    font = pygame.font.SysFont([
    "American Typewriter",
    "Courier New",
    "Courier",
    "Liberation Mono",
    "DejaVu Serif",
    "Times New Roman"
], 48)
    text = font.render(text, True, WHITE, BLACK)
    text_box = text.get_rect()
    text_box.topleft = (x,y)
    screen.blit(text, text_box)

def drawText(screen, text, x, y, color, bgColor):
    font = pygame.font.SysFont(["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New"], 14)
    text = font.render(text, True, color, bgColor)
    text_box = text.get_rect()
    text_box.topleft = (x,y)
    screen.blit(text, text_box)

def makeMenu():
    ...
def drawBoard(screen):
    keyboard = [['q','w','e','t'],['r','y','u','i'],['o','p','a','s'],['d','f','g','h'],['j','k','l','z'],['x','c','v','b'],['n','m', 'X','O']]
    for n in range(5):
        for m in range(3):
            print(keyboard[n][m])
            drawText(screen, keyboard[n][m], m,n, WHITE,BLACK)
# class Menu():
#     def __init__(self, elements):
#         self.index = 0
#         self.elements = elements
#     def input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_UP] and self.index != 0:
#             self.index -= 1
#             print(self.index)
#         if keys[pygame.K_DOWN] and self.index != len(self.elements):
#             self.index += 1
#             print(self.index)
#         if keys[pygame.K_RETURN]:
#             print(self.elements[self.index].text)
#     def draw(self, screen):
#         for e in self.elements:
#             e.draw(screen)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        FONT = pygame.font.SysFont(["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New"], 64)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.entity = Entity()
        self.update_time = pygame.time.get_ticks()
        self.entity.position = Position(x,y,w,h)
        self.entity.animations.add('idle', Animation([self.txt_surface]))


    def handle_event(self, event):
        FONT = pygame.font.SysFont(["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New"], 64)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     # If the user clicked on the input_box rect.
        #     if self.rect.collidepoint(event.pos):
        #         # Toggle the active variable.
        #         self.active = not self.active
        #     else:
        #         self.active = False
            # Change the current color of the input box.
            # self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            # if self.active:
            if event.key == pygame.K_RETURN:
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)
    def clear(self):
        self.text = ''
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
       self.entity.position = Position(self.rect.x,self.rect.y, self.txt_surface.get_rect().width,self.txt_surface.get_rect().height)
       self.entity.animations.add('idle', Animation([self.txt_surface]))
    def start(self):
        entity = Entity()
        entity.position = Position(0,0,8,72)
        entity.animations.add('idle', Animation([cursor_blink]))
        return entity
    def makeCursor(self):
        entity = Entity()
        entity.position = Position(self.txt_surface.get_rect().width,0,8,72)
        entity.animations.add('idle', Animation([cursor, cursor_blink]))
        return entity
    def makeInputEntity(self):
        return self.entity
    

   

class MenuElement():
    def __init__(self, text, pos, selected, screen):
        self.selected = selected
        self.hovered = False
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw(screen)

    def draw(self,screen):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        font = pygame.font.SysFont(["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New"], 14)
        self.rend = font.render(self.text, True, self.get_color()[0], self.get_color()[1])
        
    def get_color(self): 
        if self.selected:
            color = BLACK
            bgColor = WHITE
            return [color, bgColor]
        elif self.hovered:
            color = WHITE
            bgColor = BLACK
            return [color, bgColor]
        else:
            color = (100,100,100)
            bgColor = BLACK
            return [color, bgColor]

        # if self.hovered:
        #     return (255, 255, 255)
        # else:
        #     return (100, 100, 100)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

class TitleGraphic():
    def __init__(self):
        pass
    





        
           
        
            
            
        
  
