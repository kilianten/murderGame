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
from townsPeople import *
from priest import *
from interface import *
from times import *

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
        self.last_update = 0
        self.currentDay = 0
        self.daysRunning = 0
        self.isDebugMode = False
        self.isInChatMode = False
        self.gameMinutes = 0
        self.gameTime = DateTime(0, 0, 1)
        self.schedule = []
        self.generateEvents()
        self.runningEvents = []

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
        img_folder = path.join(self.game_folder, 'images')
        self.map = Map(path.join(img_folder, DEFAULT_MAP))

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
        self.acoustic_guitar = self.loadImage(img_folder, ACOUSTIC_GUITAR, 26, 52)
        self.brickwall_image = self.loadImage(img_folder, BRICKWALL,  32, 32)
        self.brickwall_corner_image = self.loadImage(img_folder, BRICKWALL_CORNER)
        self.grass01 = self.loadImage(img_folder, GRASS01)
        self.priest_img = self.loadImage(img_folder,PRIEST_IMAGE)
        self.speech_bubble_image = self.loadImage(img_folder,SPEECH_BUBBLE_IMAGE)
        self.conversation_hud_image = self.loadImage(img_folder, CONVERSATION_HUD, 0, 0)
        self.alter_image = self.loadImage(img_folder, ALTER_IMAGE, 48, 48)
        self.priestReadingAnimation = self.loadAnimation(img_folder, PRIEST_READING_ANIM)
        self.loadIcons(img_folder)

    def load_data(self):
        self.loadImages()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.collidable_sprites = pg.sprite.Group()
        self.townspeople = pg.sprite.Group()
        self.loadMap(self.map)
        self.acousticGuitar = AcousticGuitar(self, 2000, 200)
        self.camera = Camera(self.map.width, self.map.height)
        self.spawnTownspeople()

    def loadMap(self, map):
        for x in range(map.tilewidth):
            for y in range(map.tileheight):
                colour = map.mapImage.get_at((x,y))
                if colour == (119, 50, 40, 255):
                    Wall(self, x, y)
                if colour == (105, 106, 106, 255):
                    self.player = Player(self, x, y)
                if colour == (	142, 68, 140, 255):
                    self.alter = Alter(self, x, y)

    def generateEvents(self):
        self.schedule.append(Mass(1, 0, 1, 60, self))

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
        if self.isInChatMode == False:
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
        if self.player.state == "talking":
            self.screen.blit(self.conversation_hud_image, (0, (HEIGHT - self.conversation_hud_image.get_height())))
        if self.isDebugMode:
            self.debug()
        pg.display.flip()

    def drawGrid(self):
        cameraPosition = self.camera.camera.topleft
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def spawnTownspeople(self):
        self.priest = Priest(self, 64, 64, self.priest_img)

    def debug(self):
        self.drawGrid()
        for person in self.townspeople:
            if person.state == "walking":
                person.drawPath()
            pg.draw.rect(self.screen, RED, person.rect.move(self.camera.camera.topleft), 1)
        for object in self.collidable_sprites:
            pg.draw.rect(self.screen, ORANGE, object.hitbox.rect.move(self.camera.camera.topleft), 1)
        pg.draw.rect(self.screen, RED, self.player.hitbox.rect.move(self.camera.camera.topleft), 1)
        if self.player.visionRect != None:
            pg.draw.rect(self.screen, GREEN, self.player.visionRect.move(self.camera.camera.topleft), 1)
        pg.draw.rect(self.screen, RED, self.player.hitbox.rect.move(self.camera.camera.topleft), 1)

    def updateClock(self):
        now = pg.time.get_ticks()
        if now - self.last_update > CLOCK_UPDATE:
            self.last_update = now
            self.gameTime.update()
            print(self.runningEvents)
            for event in self.schedule:
                if self.gameTime == event.startTime:
                    event.startEvent()
                    self.runningEvents.append(event)
                    print(self.runningEvents)
                if self.gameTime == event.endTime:
                    event.endEvent()
                    self.runningEvents.remove(event)
                    self.schedule.remove(event)

    def increaseDay(self):
        self.daysRunning += 1

    def drawClock(self):
        self.drawSeconds()
        self.screen.blit(self.clock_semicolon_image, [165,20])
        self.drawHours()

    def drawSeconds(self):
        secondCounter = self.gameTime.minute % 10
        tenSecondCounter = int(self.gameTime.minute / 10)
        self.screen.blit(self.clock_number_images[tenSecondCounter], [180,20])
        self.screen.blit(self.clock_number_images[secondCounter], [200,20])

    def drawHours(self):
        hourCounter = self.gameTime.hour % 10
        tenHourCounter = int(self.gameTime.hour / 10)
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

    def loadImage(self, folder, imageName, xscale=TILESIZE, yscale=TILESIZE):
        image = pg.image.load(path.join(folder, imageName)).convert_alpha()
        return pg.transform.scale(image, (image.get_rect().width + xscale, image.get_rect().height + yscale))

    def loadIcon(self, folder, imageName, xscale=-40, yscale=-40):
        image = pg.image.load(path.join(folder, imageName)).convert_alpha()
        return pg.transform.scale(image, (image.get_rect().width + xscale, image.get_rect().height + yscale))

    def loadIcons(self, folder):
        self.icon_image_arrows = {}
        arrow = self.loadIcon(folder, ARROW_RIGHT)
        self.icon_home_image = self.loadIcon(folder, ICON_HOME)
        self.arrows = {}
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            self.arrows[dir] = pg.transform.rotate(arrow, vec(dir).angle_to(vec(1,0)))

    def loadAnimation(self, folder, imageCollection,  xscale=TILESIZE, yscale=TILESIZE):
        animationImage = []
        for imageName in imageCollection:
            image = pg.image.load(path.join(folder, imageName)).convert_alpha()
            animationImage.append(pg.transform.scale(image, (image.get_rect().width + xscale, image.get_rect().height + yscale)))
        return animationImage


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
