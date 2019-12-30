import pygame as pg
from settings import *


class Map:
    def __init__(self, pathToImage):
        self.mapImage = pg.image.load(pathToImage).convert_alpha()
        self.tilewidth = self.mapImage.get_width()
        self.tileheight = self.mapImage.get_height()
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.rect = self.camera
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT/ 2)

        #limit scrolling to map TILESIZE
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.rect = self.camera
        print(self.rect.x)
        print(self.rect.y)

class CameraView:
    def __init__(self):
        self.camera = pg.Rect(0, 0, WIDTH, HEIGHT)
