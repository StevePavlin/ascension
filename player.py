from constants import *
from map import mapMgr
import pygame


class Player(object):

    def __init__(self):
        self.images = pygame.image.load(MAP_DIR + "sheet.png")
        
        
        self.xVel = 2
        self.yVel = 2        

        self.direction = "up"
        self.currentImage = 1
        self.maxImage = 2
        self.speed = 50
        self.isWalking = True
        
        # Much staticness very rect
        self.rect = pygame.Rect(256, 256, 32, 32)

        self.screen = pygame.display.get_surface()

    def draw(self):
        imageDimensions = 32
       
        # Sheet definitions
        actions = {
                "down": 0,
                "left": 32,
                "right": 64,
                "up": 96
        }
        
        if self.isWalking:
            # Delay 
            self.speed -= 1
            if self.speed == 0:  
                self.speed = 50

                if self.currentImage == 0:
                    self.currentImage = 2
                else:
                    self.currentImage = 0     
        else:
            # They are walking
            self.currentImage = 1


        self.screen.blit(self.images, (self.rect.x + mapMgr.getCurrentMap().cameraX, self.rect.y + mapMgr.getCurrentMap().cameraY), (self.currentImage * 32, actions[self.direction], imageDimensions, imageDimensions))
         
    def update(self, keys):

        # Cap velocity
        
        
        if keys[pygame.K_DOWN]: 
            self.direction = "down"
            self.yVel = 3

        elif keys[pygame.K_UP]: 
            self.direction = "up"
            self.yVel = -3
        else:
            self.yVel = 0

        if keys[pygame.K_LEFT]:
            self.direction = "left"
            self.xVel = -3
        
        elif keys[pygame.K_RIGHT]: 
            self.direction = "right"
            self.xVel = 3
        
        else:
            self.xVel = 0
        
        if keys[pygame.K_UP] != 0 or keys[pygame.K_DOWN] != 0 or keys[pygame.K_LEFT] != 0 or keys[pygame.K_RIGHT] != 0:
            self.isWalking = True
        else:
            self.isWalking = False
        
        mapMgr.getCurrentMap().cameraX += self.xVel * -1        
        self.rect.x += self.xVel
        for blocker in mapMgr.getCurrentMap().blockers:
            if self.rect.colliderect(blocker):
                self.rect.x -= self.xVel
                mapMgr.getCurrentMap().cameraX -= self.xVel * -1
                self.xVel = 0

        mapMgr.getCurrentMap().cameraY += self.yVel * -1
        self.rect.y += self.yVel
        for blocker in mapMgr.getCurrentMap().blockers:
            if self.rect.colliderect(blocker):
                self.rect.y -= self.yVel
                mapMgr.getCurrentMap().cameraY -= self.yVel * -1    
                self.yVel = 0

player = Player()
