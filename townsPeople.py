import pygame as pg
from settings import *
from collections import deque
import heapq
from sprites import Hitbox
vec = pg.math.Vector2

class Person(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self._layer = 3
        self.groups = game.all_sprites, game.collidable_sprites, game.townspeople
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.grid = None
        self.path = None
        self.state = "idle"
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.dir = (1, 0)
        self.hitbox = Hitbox(self.rect)
        self.pos = vec(int(self.x/TILESIZE), int(self.y/TILESIZE))
        self.isNotInRush = True
        self.isAlive = True
        self.desire = "idle"
        self.offsetImageX = 0
        self.offsetImageY = 0

    def vec2int(self, v):
        return (int(v.x), int(v.y))

    def update(self):
        if self.state == "walking":
            if self.journey.update(self.pos) == False:
                self.state = "idle"
            else :
                self.moveCharacter(self.journey.update(self.pos))
        self.x = self.pos.x * 64
        self.y = self.pos.y * 64
        self.rect.x = self.x - (TILESIZE / 2) + self.offsetImageX
        self.rect.y = self.y - TILESIZE + self.offsetImageY

    def startJourney(self, start, destination, game):
        self.journey = Journey(start, destination, game)
        self.state = "walking"

    def drawPath(self):
        for node in self.journey.path:
            x, y = node
            rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE).move(self.game.camera.camera.topleft)
            pg.draw.rect(self.game.screen, LIGHTGREY, rect)
        current = self.journey.start + self.journey.path[vec2int(self.journey.start)]
        while current != self.journey.destination:
            x = current.x * TILESIZE + TILESIZE / 2
            y = current.y * TILESIZE + TILESIZE / 2
            img = self.game.arrows[vec2int(self.journey.path[(current.x, current.y)])]
            r = img.get_rect(center=(x, y))
            r = r.move(self.game.camera.camera.topleft)
            self.game.screen.blit(img, r)
            # find next in path
            current = current + self.journey.path[vec2int(current)]

    def moveCharacter(self, vector):
        self.pos = vec(vector + self.pos)
        self.x = self.x + (vector.x * 64)
        self.y = self.y + (vector.y * 64)
        self.rect.x = self.x - (TILESIZE / 2)
        self.rect.y = self.y - TILESIZE

    def createSpeechBubble(self):
        self.SpeechBubble =  SpeechBubble(self.x + TILESIZE + self.offsetImageX, self.y - (TILESIZE * 2) +  self.offsetImageY, self.game)

class Journey:
    def __init__(self, start, destination, game):
        self.start = start
        self.destination = destination
        self.grid = WeightedGrid(game)
        self.path = self.grid.a_star_search(self.grid, start, destination)
        self.nextStep = self.path[vec2int(self.start)] + self.start
        self.currentNode = self.path[vec2int(start)]

    def update(self, currentPos):
        if currentPos != self.destination:
            if currentPos == self.nextStep:
                self.currentNode = self.path[vec2int(self.nextStep)]
                self.nextStep = self.nextStep + self.path[vec2int(self.nextStep)]
            # find next in path
            return self.currentNode / PRIEST_SPEED
        else:
            self.isWalking = False
            return False

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

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

    def heuristic(self, node1, node2):
        return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10

    def breadth_first_search(self, graph, start, end):
        frontier = deque()
        frontier.append(start)
        path = {}
        path[vec2int(start)] = None
        while len(frontier) > 0:
            current = frontier.popleft()
            if current == end:
                break
            for next in graph.find_neighbors(current):
                if vec2int(next) not in path:
                    frontier.append(next)
                    path[vec2int(next)] = current - next
        return path

    def dijkstra_search(self, graph, start, end):
        frontier = PriorityQueue()
        frontier.put(vec2int(start), 0)
        path = {}
        cost = {}
        path[vec2int(start)] = None
        cost[vec2int(start)] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == end:
                break
            for next in graph.find_neighbors(vec(current)):
                next = vec2int(next)
                next_cost = cost[current] + graph.cost(current, next)
                if next not in cost or next_cost < cost[next]:
                    cost[next] = next_cost
                    priority = next_cost + self.heuristic(end, vec(next))
                    frontier.put(next, priority)
                    path[next] = vec(current) - vec(next)
        return path

    def a_star_search(self, graph, end, start):
        frontier = PriorityQueue()
        frontier.put(vec2int(start), 0)
        path = {}
        cost = {}
        path[vec2int(start)] = None
        cost[vec2int(start)] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == end:
                break
            for next in graph.find_neighbors(vec(current)):
                next = vec2int(next)
                next_cost = cost[current] + graph.cost(current, next)
                if next not in cost or next_cost < cost[next]:
                    cost[next] = next_cost
                    priority = self.heuristic(end, vec(next))
                    frontier.put(next, priority)
                    path[next] = vec(current) - vec(next)
        return path

class WeightedGrid(SquareGrid):
    def __init__(self, game):
        super().__init__(game)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 0) + 10

def vec2int(v):
    return (int(v.x), int(v.y))

class SpeechBubble(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.speech_bubble_image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x =  self.x
        self.rect.y =  self.y
