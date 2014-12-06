from constants import *
from map import Map, mapMgr
import pygame

class Player(object):

    def __init__(self):
        self.images = pygame.image.load(MAP_DIR + "sheet.png")
        
        # Player velocities
        self.xVel = 2
        self.yVel = 2        

        self.direction = "up"
        self.currentImage = 1
        self.maxImage = 2
        self.speed = 50
        self.isWalking = True

        # Current map were drawing on
        self.currentMap = mapMgr.getCurrentMap()
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
   
    def updateCamera(self): 


        self.rect.x += self.xVel     
        self.rect.y += self.yVel

        colliding = False
        # Test for blockers
        for blocker in mapMgr.getCurrentMap().blockers:
            if self.rect.colliderect(blocker):
                self.rect.x -= self.xVel
                self.xVel = 0
                
                self.rect.y -= self.yVel
                self.yVel = 0
               
                colliding = True
       

        cameraBoundX = SIZE[0] / 2
        cameraBoundY = SIZE[1] / 2
    
        #print('player x: ' + str(self.rect.x) + ' player y: ' + str(self.rect.y))
        
        # Test for camera boundaries and adjust it accordingly
        if self.currentMap.cameraX > 0:
            self.currentMap.cameraX = 0

        elif self.currentMap.cameraX < self.currentMap.maxXBound * -1:
            self.currentMap.cameraX = self.currentMap.maxXBound * -1
                     
        if (self.rect.x > 0 and self.rect.x < cameraBoundX) or (self.rect.x > self.currentMap.maxXBound * 2 - cameraBoundX and self.rect.x < self.currentMap.maxXBound * 2):
            # Do not move camera, player is at a bound
            pass
        elif not colliding:
            self.currentMap.cameraX += self.xVel * -1     
        else:
            pass


        if self.currentMap.cameraY > 0:
            self.currentMap.cameraY = 0

        elif self.currentMap.cameraY < self.currentMap.maxYBound * -1:
            self.currentMap.cameraY = self.currentMap.maxYBound * -1
                     
        if (self.rect.y > 0 and self.rect.y < cameraBoundY) or (self.rect.y > self.currentMap.maxYBound * 2 - cameraBoundY and self.rect.y < self.currentMap.maxYBound * 2):
                # Do not move camera, player is at a bound
            pass
        elif not colliding:
            self.currentMap.cameraY += self.yVel * -1  
        else:
            pass

    def update(self, keys):

        # Movement modifiers
        
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
        
        # Move the camera accordingly
        self.updateCamera()

 
        # Test for portals
        for portal in self.currentMap.portals:
            rect = portal[0]
            goto = portal[1]
            song = portal[2]

            if self.rect.colliderect(rect):
                tempMap = mapMgr.createNewMap(goto, song)
                mapMgr.setCurrentMap(tempMap)
                self.currentMap = mapMgr.getCurrentMap()
                
                # Put player in entrance
                self.rect.x = SIZE[0] / 2
                self.rect.y = SIZE[1] / 2



player = Player()
