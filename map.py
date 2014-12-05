import pygame
from pytmx import *
from constants import *
from music import *


"""
MapManager class used to track the current map being drawn and draw it
"""
#TODO Possibly convert this class to a Singleton, only one instance is needed
class MapManager(object):

    def __init__(self, mapObject):
        self.mapObject = mapObject
        self.screen = pygame.display.get_surface()
    
    def getCurrentMap(self):
        return self.mapObject

    def setCurrentMap(self, mapObject):
        self.mapObject = mapObject
    
    def createNewMap(self, fileName, songName):
        return Map(fileName, songName)

    def draw(self, drawnPlayer):
        # First draw the background and foreground
        if not drawnPlayer:
            layers = [0, 2]
        else:
            layers = [2, 3]


        for layer in range(layers[0], layers[1]):
            # Loop through x and y tiles and draw the layers
            for x in range(0, self.mapObject.maxX + 1):
                for y in range(0, self.mapObject.maxY + 1):
                    image = self.mapObject.tmxData.get_tile_image(x, y, layer)
                    
                    # Make sure the image isnt null

                    if image:
                        self.screen.blit(image, (x * 32 + self.mapObject.cameraX, y * 32 + self.mapObject.cameraY))


   
""" 
Map class to be managed by MapManager
The input .tmx requires 3 layers:
-Background (Drawn before player)
-Foreground (Drawn before player)
-Top (Drawn after player)
-Collision (All blocks to be collision prone must have the property name "blocker" 

Use Tiled (http://mapeditor.org) to build these maps
"""
class Map(object):
    
    def __init__(self, fileName, songName):
        self.blockers = None
        self.portals = None
 
        self.cameraX = 0
        self.cameraY = 0

        self.fileName = fileName
        self.tmxData = load_pygame(MAP_DIR + fileName, pixelalpha=True)

        self.maxX = None
        self.maxY = None

        self.song = songName 

        self.findObstacles()
        self.findPortals()
        self.getMaxBlocks()
        
        # Use the bounds to set the camera properly
        self.maxXBound = int((self.maxX * 32) / 2)
        self.maxYBound = int((self.maxY * 32) / 2)


        
        music.setCurrentSong(self.song)

    # Sets the max x and max y block
    def getMaxBlocks(self): 
        temp = self.tmxData.get_layer_by_name("Background")

        for tile in temp.tiles():
            pass
        
        self.maxX = tile[0]
        self.maxY = tile[1]
       
       

                  
    def findObstacles(self):
        blockers = []
 
        obstacleLayer = self.tmxData.get_layer_by_name("Collision")
     
        for tile_object in obstacleLayer:
            properties = tile_object.__dict__
            
            if properties['name'] == 'blocker':
                x = properties['x'] 
                y = properties['y']
                width = properties['width']
                height = properties['height']
                newRect = pygame.Rect(x, y, width, height)
            
                blockers.append(newRect)
        
        self.blockers = blockers 

    def findPortals(self):
        portals = []

        obstacleLayer = self.tmxData.get_layer_by_name("Collision")

        for tile_object in obstacleLayer:
            properties = tile_object.__dict__
            print(properties)

            if properties['name'] == 'portal':
                
                mapFile = properties['properties']['goto']
                songFile = properties['properties']['song']
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                newRect = pygame.Rect(x, y, width, height)

                temp = [newRect, mapFile, songFile]
                portals.append(temp)

        self.portals = portals
        #print(self.portals)
        
mapOne = Map('forest.tmx', 'kairi')
mapMgr = MapManager(mapOne)

mapMgr.setCurrentMap(mapOne)



