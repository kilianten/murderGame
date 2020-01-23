import pygame as pg
from settings import *
from collections import deque
import heapq
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.collidable_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x + TILESIZE
        self.y = y + TILESIZE
        self.vx, self.vx = 0, 0
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.dir = (0, 1)
        self.hitbox = Hitbox(self.rect)
        self.hitbox.setDimensions(-70,-80)
        self.isDebugModePressed = False
        self.isIPressed = False
        self.visionRect = None
        self.isTalking = False

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dir = vec(-1, 0)
            self.walking = True
            self.vx = -PLAYER_SPEED
            self.hitbox.setWidth(25)
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.dir = vec(1, 0)
            self.walking = True
            self.hitbox.setWidth(25)
        if keys[pg.K_w]:
            self.dir = vec(0, -1)
            self.hitbox.setWidth(40)
            self.vy = -PLAYER_SPEED
            self.walking = True
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.dir = vec(0, 1)
            self.walking = True
            self.hitbox.setWidth(40)
        if keys[pg.K_SLASH]:
            self.isDebugModePressed = True
        if self.isDebugModePressed == True and not keys[pg.K_SLASH]: #check if key released
            self.game.isDebugMode = not self.game.isDebugMode
            self.isDebugModePressed = False
        if keys[pg.K_i]:
            self.isIPressed = True
        if self.isIPressed == True and not keys[pg.K_i]: #check if key released
            self.game.priest.startJourney(vec(self.game.priest.pos), vec(5, 5), self.game)
            self.isIPressed = False
        if keys[pg.K_e]:
            self.visionRect = pg.Rect((vec((self.pos) * TILESIZE) + (vec(self.dir) * 64)), (TILESIZE * 2, TILESIZE * 2))
            for person in self.game.townspeople:
                if self.visionRect.colliderect(person.rect) and person.isNotInRush:
                    person.isTalking = True
                    person.isWalking = False
                    self.isTalking = True
                    person.createSpeechBubble()

        if self.vx != 0 and self.vy != 0:
            #stop diagnal movement from being faster
            self.vx *= 0.7071
            self.vy *= 0.7071
        if self.vy == 0 and self.vx == 0:
            self.walking = False

    def collide_with_walls(self, dir, hitbox):
        for wall in self.game.walls:
            if dir == 'x':
                hits = pg.sprite.spritecollide(hitbox, self.game.walls, False)
                if hits:
                    return True

            if dir == 'y':
                hits = pg.sprite.spritecollide(self.hitbox, self.game.walls, False)
                if hits:
                    return True
        return False

    def update(self):
        self.animate()
        self.get_keys()
        self.rect.x
        checkHitbox = Hitbox(self.hitbox.rect)
        checkHitbox.rect.x += self.vx * self.game.dt
        if(not self.collide_with_walls('x', checkHitbox)):
            self.x += self.vx * self.game.dt
            self.rect.x = self.x

        checkHitbox.rect.y += self.vy * self.game.dt
        if(not self.collide_with_walls('y', checkHitbox)):
            self.y += self.vy * self.game.dt
            self.rect.y = self.y

        self.hitbox.setPosition(self.rect.center, 0, PLAYER_HITBOX_OFFSET)
        self.pos = vec(int(self.hitbox.rect.center[0] / TILESIZE), int(self.hitbox.rect.center[1] / TILESIZE))
        self.pos = vec(self.pos)


    def animate(self):
        now = pg.time.get_ticks()
        if self.walking: #walking S towards player
            if now - self.last_update > WALKING_ANIMATION_UPDATE:
                self.last_update = now
                self.image = self.getWalkingAnimation();
        else:
            self.image = self.getStandingSprite()

    def getWalkingAnimation(self):
        if self.dir == vec(0, 1):
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_down)
            return self.game.player_walking_down[self.current_frame]
        if self.dir == vec(0, -1):
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_foward)
            return self.game.player_walking_foward[self.current_frame]
        if self.dir == vec(1, 0):
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_right)
            return self.game.player_walking_right[self.current_frame]
        if self.dir == vec(-1, 0):
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_left)
            return self.game.player_walking_left[self.current_frame]

    def getStandingSprite(self):
        if self.dir == vec(0, 1):
            return self.game.player_img
        if self.dir == vec(0, -1):
            return self.game.player_img_foward
        if self.dir == vec(1, 0):
            return self.game.player_img_right
        if self.dir == vec(-1, 0):
            return self.game.player_img_left

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.brickwall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        if(direction == "corner"):
            self.rect.x = x * TILESIZE
            self.rect.y = y * TILESIZE
        if(direction == "horizontal"):
            self.rect.x = x * TILESIZE
            self.rect.y = y * TILESIZE

class AcousticGuitar(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.acoustic_guitar
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x =  x
        self.rect.y =  y

class Hitbox(pg.sprite.Sprite):
    def __init__(self, startingRect):
        self.rect = startingRect

    def setPosition(self, center, xOffset, yOffset):
        self.rect.center = center
        self.rect.y += yOffset
        self.rect.x += xOffset

    def setDimensions(self, x, y):
        self.rect = self.rect.inflate(x, y)

    def setWidth(self, width):
        self.rect.width = width

    def setHeight(self, height):
        self.rect.height = height
