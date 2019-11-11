import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vx = 0, 0
        self.x = x + TILESIZE
        self.y = y + TILESIZE
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.dir = 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dir = 3
            self.walking = True
            self.vx = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.dir = 1
            self.walking = True
        if keys[pg.K_w]:
            self.dir = 0
            self.vy = -PLAYER_SPEED
            self.walking = True
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.dir = 2
            self.walking = True
        if self.vx != 0 and self.vy != 0:
            #stop diagnal movement from being faster
            self.vx *= 0.7071
            self.vy *= 0.7071
        if self.vy == 0 and self.vx == 0:
            self.walking = False

    def collide_with_walls(self, dir):
        for wall in self.game.walls:
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x

            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.yx = 0
                    self.rect.y = self.y

    def update(self):
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

    def animate(self):
        now = pg.time.get_ticks()
        if self.walking: #walking S towards player
            if now - self.last_update > WALKING_ANIMATION_UPDATE:
                self.last_update = now
                self.image = self.getWalkingAnimation();
        else:
            self.image = self.getStandingSprite()

    def getWalkingAnimation(self):
        if self.dir == 2:
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_down)
            return self.game.player_walking_down[self.current_frame]
        if self.dir == 0:
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_foward)
            return self.game.player_walking_foward[self.current_frame]
        if self.dir == 1:
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_right)
            return self.game.player_walking_right[self.current_frame]
        if self.dir == 3:
            self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_left)
            return self.game.player_walking_left[self.current_frame]

    def getStandingSprite(self):
        if self.dir == 2:
            return self.game.player_img
        if self.dir == 0:
            return self.game.player_img_foward
        if self.dir == 1:
            return self.game.player_img_right
        if self.dir == 3:
            return self.game.player_img_left

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
