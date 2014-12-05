from constants import *
import pygame
import os

class Music(object):

    def __init__(self):
        self.currentSong = None

        # Allows for easy repeats
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    def getCurrentSong(self):
        return self.currentSong

    def setCurrentSong(self, fileName):
        self.currentSong = fileName + ".ogg"
        self.play()

    def play(self):
        pygame.mixer.music.load(MUSIC_DIR + self.currentSong)
        pygame.mixer.music.play()
        pass

music = Music()

