from pytmx import *
import pygame
import time


############## Globals #################
pygame.init()

size = width, height = 608, 608
screen = pygame.display.set_mode(size)
black = 0, 0, 0

tmxdata = load_pygame("map.tmx")
image = tmxdata.get_tile_image(7, 0, 0)
imagerect = image.get_rect()

clock = pygame.time.Clock()
########################################


class Player(object):

    def __init__(self):
        self.images = pygame.image.load("sheet.png")
        self.x = 256
        self.y = 256
        self.direction = "up"
        self.currentImage = 1
        self.maxImage = 2
        self.speed = 50
        self.isWalking = True

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

        screen.blit(self.images, (self.x, self.y), (self.currentImage * 32, actions[self.direction], imageDimensions, imageDimensions))
         
            
       
         


class Map(object):
    
    def __init__(self):
        pass


    def draw(self, layers):
        
        # Assuming draw order for layers is 0, 1, 2 etc.
        for layer in layers:
            for x in range(0, 19):
                for y in range(0, 19):
                    image = tmxdata.get_tile_image(x, y, layer)
                    
                    if image:
                        screen.blit(image, (x * 32, y * 32))
                   

player = Player()
mapOne = Map()
while 1:
    clock.tick(60)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]: 
        player.direction = "down"
        player.y += 2
        
    if keys[pygame.K_UP]: 
        player.direction = "up"
        player.y -= 2
        
    if keys[pygame.K_LEFT]: 
        player.direction = "left"
        player.x -= 2
    
    if keys[pygame.K_RIGHT]: 
        player.direction = "right"
        player.x += 2

    
    if keys[pygame.K_UP] != 0 or keys[pygame.K_DOWN] != 0 or keys[pygame.K_LEFT] != 0 or keys[pygame.K_RIGHT] != 0:
        player.isWalking = True
    else:
        player.isWalking = False

    # Reset the screen
    screen.fill(black)
    # Draw the world
    mapOne.draw([0, 1])
    player.draw()
    mapOne.draw([2])

    

    # DEBUG


    pygame.display.flip()
 


