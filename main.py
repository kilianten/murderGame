# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 2
# Collisions and Tilemaps
# Video link: https://youtu.be/ajR4BZBKTr4
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from map import *

class Game:

    game_folder = path.dirname(__file__)

    def __init__(self):
        pg.init()
        self.load_settings()
        if(SETTINGS["ISFULLSCREEN"] == "True"):
            self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.HUDenabled = True
        self.gameTime = [0, 0]
        self.last_update = 0
        self.currentDay = 0
        self.daysRunning = 0

    def load_settings(self):
        print("Loading Settings")
        if not path.exists(path.join(self.game_folder, 'settings.txt')):
            print("Settings file not found")
            print("Creating file")
            f = open(path.join(self.game_folder, 'settings.txt'), 'w')
            f.write("ISFULLSCREEN:True\n")
            f.close()
        f = open(path.join(self.game_folder, 'settings.txt'), 'r')
        for line in f.readlines():
            line = line.rstrip('\n').split(":")
            SETTINGS[line[0]]=line[1]
        f.close()

    def loadImages(self):
        self.map = Map(path.join(self.game_folder, 'map.txt'))
        img_folder = path.join(self.game_folder, 'images')

        self.player_img = self.loadImage(img_folder, PLAYER_IMAGE)
        self.player_img_foward = self.loadImage(img_folder, PLAYER_IMAGE_FOWARD)
        self.player_img_right = self.loadImage(img_folder, PLAYER_IMAGE_RIGHT)
        self.player_img_left = pg.transform.flip(self.player_img_right, True, False)
        self.player_walking_down = [ self.loadImage(img_folder, PLAYER_WALKING_DOWN[0]), self.player_img, self.loadImage(img_folder, PLAYER_WALKING_DOWN[1]), self.player_img]
        self.player_walking_foward = [ self.loadImage(img_folder, PLAYER_WALKING_FOWARD[0]), self.player_img_foward, self.loadImage(img_folder, PLAYER_WALKING_FOWARD[1]), self.player_img_foward]
        self.player_walking_right = [ self.loadImage(img_folder, PLAYER_WALKING_RIGHT[0]), self.player_img_right, self.loadImage(img_folder, PLAYER_WALKING_RIGHT[1]), self.player_img_right]
        self.player_walking_left = [ pg.transform.flip(self.player_walking_right[0], True, False), self.player_img_left, pg.transform.flip(self.player_walking_right[2], True, False), self.player_img_left]
        self.clock_number_images = self.loadArrayOfImages(CLOCK_NUMBERS, img_folder, -30, -30)
        self.clock_semicolon_image = self.loadImage(img_folder, CLOCK_SEMICOLON, -30, -30)
        self.days_of_week_images = self.loadArrayOfImages(DAYS_OF_WEEK, img_folder, -30, -16)
        self.acoustic_guitar = self.loadImage(img_folder, ACOUSTIC_GUITAR, 24, 58)

    def load_data(self):
        self.loadImages()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.acousticGuitar = AcousticGuitar(self, 200, 200)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        f = open(path.join(self.game_folder, 'settings.txt'), 'w')
        for key in SETTINGS:
            f.write(key + ":" + str(SETTINGS[key]) + "\n")
        f.close()
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        self.updateClock()

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.HUDenabled == True:
                self.drawClock()
                self.drawDay()
        pg.display.flip()

    def updateClock(self):
        now = pg.time.get_ticks()
        if now - self.last_update > CLOCK_UPDATE:
            self.last_update = now

            if self.gameTime[0] == 23 and self.gameTime[1] == 59:
                increaseDay()

            if self.gameTime[1] == 59:
                self.gameTime[0] += 1 #add an hour
            self.gameTime[1] = (self.gameTime[1] + 1) % 60

    def increaseDay(self):
        self.currentDay = (self.currentDay + 1) % 7  #increase day
        self.daysRunning += 1
        self.gameTime[0] = 0
        self.gameTime[1] = 0

    def drawClock(self):
        #calculate seconds
        secondCounter = self.gameTime[1] % 10
        tenSecondCounter = int(self.gameTime[1] / 10)
        self.screen.blit(self.clock_number_images[tenSecondCounter], [180,20])
        self.screen.blit(self.clock_number_images[secondCounter], [200,20])

        self.screen.blit(self.clock_semicolon_image, [165,20])
        #calculateHours
        hourCounter = self.gameTime[0] % 10
        tenHourCounter = int(self.gameTime[0] / 10)
        self.screen.blit(self.clock_number_images[hourCounter], [150,20])
        self.screen.blit(self.clock_number_images[tenHourCounter], [130,20])

    def drawDay(self):
        self.screen.blit(self.days_of_week_images[0], [10, 10] )

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F1:
                    if (SETTINGS["ISFULLSCREEN"] == 'True'):
                        #if fullscreen set to window
                        print("Entering Windowed mode")
                        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
                        SETTINGS["ISFULLSCREEN"] = "False"
                    else:
                        print("Entering Fullscreen mode")
                        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.FULLSCREEN)
                        SETTINGS["ISFULLSCREEN"] = "True"

    def loadImage(self, folder, imageName, xscale=64, yscale=64):
        image = pg.image.load(path.join(folder, imageName)).convert_alpha()
        return pg.transform.scale(image, (image.get_rect().width + xscale, image.get_rect().height + yscale))

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def loadArrayOfImages(self, array, img_folder, xScale = 32, yScale = 32):
        temp = []
        for i in range(0, len(array)):
            temp.append(self.loadImage(img_folder, array[i], xScale, yScale))
        return temp

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
