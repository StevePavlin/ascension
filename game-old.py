from pytmx import *
import pygame
import time
import os


############## Globals #################
pygame.init()

size = width, height = 608, 608
screen = pygame.display.set_mode(size)
black = 0, 0, 0

tmxdata = load_pygame("./map/mapnew.tmx", pixelalpha=True)
image = tmxdata.get_tile_image(7, 0, 0)
imagerect = image.get_rect()

clock = pygame.time.Clock()

# Kingdom Hearts FTW ^_^
pygame.mixer.music.load('music/kairi.ogg')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()
########################################



class Player(object):

    def __init__(self):
        self.images = pygame.image.load("./map/sheet.png")
        
        
        self.xVel = 2
        self.yVel = 2        

        self.direction = "up"
        self.currentImage = 1
        self.maxImage = 2
        self.speed = 50
        self.isWalking = True
        
        # Much staticness very rect
        self.rect = pygame.Rect(256, 256, 32, 32)

    def draw(self):
        imageDimensions = 32
       
        # Sheet definitions
        actions = {
                "down": 0,
                "left": 32,
                "right": 64,
                "up": 96
        }
        
        #TODO Fix startup speed when beginning to walk
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


        screen.blit(self.images, (self.rect.x + mapOne.cameraX, self.rect.y + mapOne.cameraY), (self.currentImage * 32, actions[self.direction], imageDimensions, imageDimensions))
         
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
        
        mapOne.cameraX += self.xVel * -1        
        self.rect.x += self.xVel
        for blocker in mapOne.blockers:
            if self.rect.colliderect(blocker):
                self.rect.x -= self.xVel
                mapOne.cameraX -= self.xVel * -1
                self.xVel = 0

        mapOne.cameraY += self.yVel * -1
        self.rect.y += self.yVel
        for blocker in mapOne.blockers:
            if self.rect.colliderect(blocker):
                self.rect.y -= self.yVel
                mapOne.cameraY -= self.yVel * -1    
                self.yVel = 0
                       
        
        
         
class Map(object):
    
    def __init__(self):
        self.blockers = None
        self.findObstacles()
        self.cameraX = 0
        self.cameraY = 0


    def draw(self, layers):
        
        # Assuming draw order for layers is 0, 1, 2 etc.
        for layer in layers:
            for x in range(0, 39):
                for y in range(0, 39):
                    image = tmxdata.get_tile_image(x, y, layer)
                    
                    if image:
                        screen.blit(image, (x * 32 + self.cameraX, y * 32 + self.cameraY))
                   
    def findObstacles(self):
        blockers = []
 
        obstacleLayer = tmxdata.get_layer_by_name("Collision")
     
        for tile_object in obstacleLayer:
            properties = tile_object.__dict__
            
            if properties['name'] == 'blocker':
                x = properties['x'] 
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
            
                blockers.append(new_rect)
        
        self.blockers = blockers 


class Music(object):

    def __init__(self):
        self.musicList = os.listdir("music")
        self.currentSong = 0

    def play(self):
        
        pygame.mixer.music.load("music/" + self.musicList[self.currentSong])
        pygame.mixer.music.play()
        self.currentSong += 1

        if self.currentSong == len(self.musicList):
            # Repeat the songs
            self.currentSong = 0


    def playSong(fileName):
        pass

player = Player()
mapOne = Map()
music = Music()

while 1:
    clock.tick(60)
    pygame.display.set_caption("Ascension | " + "FPS " + str(int(clock.get_fps())))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
   
        elif event.type == pygame.constants.USEREVENT: 
            music.play()

    keys = pygame.key.get_pressed()
    player.update(keys)
    
    
    # Reset the screen
    screen.fill(black)
    # Draw the world
    mapOne.draw([0, 1])
    player.draw()
    mapOne.draw([2])
   
    

    # DEBUG


    pygame.display.flip()
 


