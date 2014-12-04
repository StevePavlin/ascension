import pygame
import time
import os
from pytmx import *
from constants import *

""" Control class for the entire game.
    Game loop and state control lives here """
class Game(object):

    def __init__(self):
        self.running = None
        self.screen = None
        self.tmxdata = None
        self.clock = None
    
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        
                

        # Start the loop
        self.running = True

    # Game Loop begins here
    def loop(self):
        while self.running:
                       
            self.clock.tick(60)
            pygame.display.set_caption("Ascension | " + "FPS " + str(int(self.clock.get_fps())))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
           
                elif event.type == pygame.constants.USEREVENT: 
                    print('event')
                    music.play()
                    


            keys = pygame.key.get_pressed()
            player.update(keys)
            
            
            # Reset the screen
            self.screen.fill(BLACK)
            # Draw the world
            mapMgr.draw(drawnPlayer = False)
            player.draw()
            mapMgr.draw(drawnPlayer = True)
           
            

            # DEBUG


            pygame.display.flip()
         

game = Game()
game.setup()

# Get game objects setup
from map import mapMgr
from player import player
from music import music

game.loop()
