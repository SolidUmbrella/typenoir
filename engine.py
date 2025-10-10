import pygame
from constants import WHITE, PAPER, TIME

BLACK = (0,0,0)

class Camera():
     def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1
     def setWorldPosition(self, x, y):
        self.worldX = x
        self.worldY = y
     def trackEntity(self, e):
         self.entityToTrack = e

class Position():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)

class Animations():
    def __init__(self):
        self.animationList = {}
    def add(self, state, animation):
        self.animationList[state] = animation

class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.timer = 0
        self.speed = 30

    def update(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.timer = 0
            self.imageIndex += 1

            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY, zoomLevel):
        image = self.imageList[self.imageIndex]
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (newWidth, newHeight)), (x, y))

class System():
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen, entities):
        for entity in entities:
            if self.check(entity):
                self.updateEntity(screen, entity, entities)
    def updateEntity(self, screen, entity, entities):
         pass 

class CameraSystem(System):
    def __init__(self):
        super().__init__()
    def check(self, entity):
        return entity.camera is not None
    def updateEntity(self, screen, entity, entities):
        zoom = min(entity.camera.zoomLevel, 2.5)
        # set clipping
        camRect = entity.camera.rect
        clip = pygame.Rect(camRect.x, camRect.y, camRect.width, camRect.height)
        screen.set_clip(clip)

        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.width / 2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.height / 2
            entity.camera.worldX = (currentX * 0.93) + (targetX * 0.07)
            entity.camera.worldY = (currentY * 0.93) + (targetY * 0.07)

        # calc offsets
        offsetX = camRect.x + camRect.width / 2 - (entity.camera.worldX * zoom)
        offsetY = camRect.y + camRect.height / 2 - (entity.camera.worldY * zoom)

        # fill camera bg
        screen.fill(PAPER)

        for e in entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(
                screen,
                (e.position.rect.x * zoom) + offsetX,
                (e.position.rect.y * zoom) + offsetY,
                e.direction == 'left',
                False,
                zoom
            )
        # unset clip
        screen.set_clip(None)

class Entity():
    def __init__(self):
        self.state = 'idle'
        self.position = None
        self.animations = Animations()
        self.direction = 'right'
        self.camera = None
class State():
    def __init__(self):
        self.difficulty = 'EASY'
        self.score = 0
        self.time = TIME #2:17 mn:s
    def increaseScore(self):
        self.score += 1
    def decreaseScore(self):
        self.score -= 1
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
    def startTimer(self):
        self.time -= 1
    def addTime(self):
        self.time += 10
    def removeTime(self):
        self.time -= 5
    def getMinutes(self):
        minutes = self.time // 60
        return minutes
    def getSeconds(self):
        if self.time//60 != 0:
            seconds = self.time % ((60)*(self.time//60))
        else:
            seconds = self.time
        return seconds