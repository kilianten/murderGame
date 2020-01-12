import pygame as pg
from settings import *
from collections import deque
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
        self.dir = 0
        self.hitbox = Hitbox(self.rect)
        self.hitbox.setDimensions(-70,-80)
        self.isDebugModePressed = False

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dir = 3
            self.walking = True
            self.vx = -PLAYER_SPEED
            self.hitbox.setWidth(25)
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.dir = 1
            self.walking = True
            self.hitbox.setWidth(25)
        if keys[pg.K_w]:
            self.dir = 0
            self.hitbox.setWidth(40)
            self.vy = -PLAYER_SPEED
            self.walking = True
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.dir = 2
            self.walking = True
            self.hitbox.setWidth(40)
        if keys[pg.K_SLASH]:
            self.isDebugModePressed = True
        if self.isDebugModePressed == True and not keys[pg.K_SLASH]: #check if key released
            self.game.isDebugMode = not self.game.isDebugMode
            self.isDebugModePressed = False

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

class Person(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.collidable_sprites, game.townspeople
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x + TILESIZE
        self.y = y + TILESIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.dir = 0
        self.hitbox = Hitbox(self.rect)
        self.hitbox.setDimensions(-70,-80)
        self.start = vec(14, 0)
        self.goal = vec(2, 2)
        self.grid = SquareGrid(self.game)
        self.path = self.grid.breadth_first_search(self.grid, self.goal,self.start)

    def vec2int(self, v):
        return (int(v.x), int(v.y))

    def update(self):
        self.y += 1
        self.rect.y = self.y
        self.dir = 1
        self.walking = True

    def drawPath(self):
        current = self.start + self.path[self.vec2int(self.start)]
        while current != self.goal:
            x = current.x * TILESIZE + TILESIZE / 2
            y = current.y * TILESIZE + TILESIZE / 2
            img = self.game.arrows[self.vec2int(self.path[(current.x, current.y)])]
            r = img.get_rect(center=(x, y))
            r = r.move(self.game.camera.camera.topleft)
            self.game.screen.blit(img, r)
            # find next in path
            current = current + self.path[self.vec2int(current)]

class SquareGrid:
    def __init__(self, game):
        self.game = game
        self.width = self.game.map.width/64
        self.height = self.game.map.height/64
        self.walls = []
        for wall in self.game.walls:
            self.walls.append(vec(wall.x, wall.y))
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        # don't use this for diagonals:
        if (node.x + node.y) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def vec2int(self, v):
        return (int(v.x), int(v.y))

    def breadth_first_search(self, graph, start, end):
        frontier = deque()
        frontier.append(start)
        path = {}
        path[self.vec2int(start)] = None
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == end:
                break
            for next in graph.find_neighbors(current):
                if self.vec2int(next) not in path:
                    frontier.append(next)
                    path[self.vec2int(next)] = current - next
        return path

class Priest(Person):
    pass
