from html import entities
import pygame
from pygame import mixer
import random
from constants import BLACK, PAPER, SCREEN_SIZE, DARK_GREY, WHITE
from scene import SceneManager, TitleScene
from utils import MenuElement, InputBox, drawBoard, drawText
from engine import Camera, CameraSystem, State, Position


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('type_noir')
clock = pygame.time.Clock()

# Scene Manager
# -- stack of scenes,
# -- push and pop scenes from stack
game_state = State()
sceneManager = SceneManager(game_state)
entities = []

# Present Main Menu
titleScene = TitleScene(game_state)
sceneManager.push(titleScene)

# menu_blink = pygame.USEREVENT + 0
# pygame.time.set_timer(menu_blink, 1000)

new_game_label = MenuElement('new game',(10, 35),True, screen)
options_label = MenuElement('options',(10, 65), False, screen)
guide_label = MenuElement('how to',(10, 95), False, screen)

menu_elements = [new_game_label, options_label, guide_label]


difficulty_label = MenuElement('difficulty', (10,35), True, screen)
sound_fx_label = MenuElement('sound fx', (10,65),False, screen)
options_elements = [difficulty_label, sound_fx_label]

input_box1 = InputBox(0, 0, 280, 64)
inputEntity = input_box1.makeInputEntity()
cursor = input_box1.makeCursor()
start = input_box1.start()

# inputEntity.camera = Camera(0, 0, 400, 400)
# inputEntity.camera.setWorldPosition(0,0)
# inputEntity.camera.trackEntity(inputEntity)

cursor.camera = Camera(10, 10, 980, 680)
cursor.camera.setWorldPosition(0,0)
cursor.camera.trackEntity(cursor)

entities.append(inputEntity)
entities.append(cursor)
entities.append(start)

cameraSystem = CameraSystem()
# input_box2 = InputBox(100, 300, 140, 32)
input_boxes = [input_box1]

clicks = []
mixer.init()
for n in range(4):
    clicks.append(mixer.Sound('assets/clicks/kb_click'+str(n)+'.wav'))

# GAME LOOP
running = True
# score = 0
idle = True
# difficulty = 'EASY'
current_word = ['']



mixer.Channel(1).set_volume(1.5)

check_word = pygame.USEREVENT + 0
pygame.time.set_timer(check_word, 2000)

timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)

while running:
    # TODO: Skip word, minus time


    
    if sceneManager.isEmpty():
        running = False
   
    for entity in entities:
        entity.animations.animationList[entity.state].update()
    
    if sceneManager.getCurrentScene().name == 'MainMenu':    
       sceneManager.present(screen, menu_elements)
       sceneManager.update(menu_elements)
    elif sceneManager.getCurrentScene().name == 'Title':
       sceneManager.present(screen, [])
       sceneManager.update([])
    elif sceneManager.getCurrentScene().name == 'OptionsMenu':
       sceneManager.present(screen, options_elements)
       sceneManager.update(options_elements)
    elif sceneManager.getCurrentScene().name == 'Game':
       sceneManager.present(screen, input_boxes)
       sceneManager.update(input_boxes)
    elif sceneManager.getCurrentScene().name == 'Guide':
       sceneManager.present(screen, [])
       sceneManager.update([])
    elif sceneManager.getCurrentScene().name == 'GameOver':
       sceneManager.present(screen, [])
       sceneManager.update([])
    #    sceneManager.getCurrentScene().displayQuestion(screen)

    new_cursor_x = cursor.position.rect.x
    new_cursor_y = cursor.position.rect.y
    
    # check for quit
    for event in pygame.event.get():
        if event.type == timer and sceneManager.getCurrentScene().name == 'Game':
            if game_state.time > 0:
                game_state.startTimer()
            else:
               pygame.time.set_timer(timer, 0)
        if event.type == pygame.KEYDOWN:
            current = sceneManager.getCurrentScene()
            mixer.Channel(1).play(random.choice(clicks))
            if sceneManager.getCurrentScene().name == 'MainMenu':    
                sceneManager.input(screen, menu_elements, event)
            elif sceneManager.getCurrentScene().name == 'OptionsMenu':    
                sceneManager.input(screen, options_elements, event)
            elif sceneManager.getCurrentScene().name == 'Title':
                sceneManager.input(screen, [], event)
            elif sceneManager.getCurrentScene().name == 'Guide':
                sceneManager.input(screen, [], event)
            elif sceneManager.getCurrentScene().name == 'Game':
                game = sceneManager.getCurrentScene()
                if event.key == pygame.K_RETURN:
                    if input_box1.text == game.word:
                        game_state.addTime()
                        cursor.camera.zoomLevel = 1
                        cursor.camera.setWorldPosition(0,0)
                        cursor.camera.trackEntity(start)
                        game.removeWord()
                        game.playWord()
                        game_state.increaseScore()
                    else:
                        game_state.removeTime()
                        game_state.decreaseScore()
                elif event.key == pygame.K_BACKSPACE:     
                    new_cursor_x = input_box1.txt_surface.get_rect().width
                if input_box1.text == '':
                    cursor.camera.zoomLevel = 1
                    cursor.camera.setWorldPosition(0,0)
                    cursor.camera.trackEntity(start)
                else:
                    cursor.camera.trackEntity(cursor)
                    cursor.camera.zoomLevel += 0.1
                    new_cursor_x = input_box1.txt_surface.get_rect().width
                    idle = False
                sceneManager.input(screen, input_boxes, event)
                new_cursor_x = input_box1.txt_surface.get_rect().width

                
                
            # if event.key == pygame.K_SPACE:
            #     sceneManager.getCurrentScene().playWord()
            
                 
                # self.text += event.unicode
            # Re-render the text.
            # self.txt_surface = FONT.render(self.text, True, self.color)
        # if sceneManager.getCurrentScene().name == 'Game' and event.type == check_word and not idle:
        #     print(current_word)
        #     idle = True
        #     if current_word[-1] == input_box1.text:
        #         cursor.camera.zoomLevel = 1
        #         cursor.camera.setWorldPosition(0,0)
        #         cursor.camera.trackEntity(start)
        #     else:
        #         current_word.append(input_box1.text)
        # if sceneManager.getCurrentScene().name == 'Game' and event.type != pygame.TEXTEDITING and not idle:
        #         cursor.camera.zoomLevel = 1
        #         cursor.camera.setWorldPosition(0,0)
        #         cursor.camera.trackEntity(start)
        #         idle = True

            # now = pygame.time.get_ticks()
            # if now != input_box1.update_time and not idle:
            #     cursor.camera.zoomLevel = 1
            #     cursor.camera.setWorldPosition(0,0)
            #     cursor.camera.trackEntity(start)
            #     idle = True


       

            
        if event.type == pygame.QUIT:
            running = False
       
        
  
    # cursor input
    keys = pygame.key.get_pressed()
   

    new_cursor_rect = pygame.Rect(int(new_cursor_x), int(cursor.position.rect.y),cursor.position.rect.width,cursor.position.rect.height)
    cursor.position.rect.x = int(new_cursor_x)
    
    screen.fill(PAPER)
    cameraSystem.update(screen, entities)
    clock.tick(60)

# quit
pygame.quit()