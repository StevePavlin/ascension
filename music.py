from constants import *
import pygame
import os

class Music(object):

    def __init__(self):
        self.musicList = os.listdir("music")
        self.currentSong = 0

        # Allows for easy repeats
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)

    def play(self):
                
        pygame.mixer.music.load(MUSIC_DIR + self.musicList[self.currentSong])
        pygame.mixer.music.play()
        self.currentSong += 1

        if self.currentSong == len(self.musicList):
                        # Repeat the songs
            self.currentSong = 0


    def playSong(fileName):
        pass

music = Music()
music.play()

