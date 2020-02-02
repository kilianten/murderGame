import pygame as pg
from settings import *
vec = pg.math.Vector2


MINUTES_IN_DAY = 1440
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24

class Event:
    def __init__(self, minute, hour, date, duration, game):
        self.startTime = DateTime(minute, hour, date)
        self.endTime = DateTime(minute, hour, date)
        self.duration = duration
        self.game = game

class DateTime:
    def __init__(self, minute, hour=None, date=None):
        if date == None:
           self.date = int(minute/MINUTES_IN_DAY)
           remainder = minute - (self.date * MINUTES_IN_DAY)
           self.hour = int(remainder / MINUTES_IN_HOUR)
           self.minute = remainder % MINUTES_IN_HOUR
        else:
           self.minute = minute
           self.hour = hour
           self.date = date

    def update(self):
        if self.minute == 59 and self.hour == 23:
            self.minute = 0
            self.hour = 0
            self.date += self.date
            self.day = (self.date + 1) % 7
        elif self.minute == 59:
            self.hour += 1
            self.minute = (self.minute + 1) % MINUTES_IN_HOUR
        self.minute += 1

    def getMinutes(self):
        return self.minute + self.hour * MINUTES_IN_HOUR + (self.date * HOURS_IN_DAY * MINUTES_IN_HOUR)


    def __eq__(self, other):
        if isinstance(other, DateTime):
           return self.getMinutes() == other.getMinutes()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.getMinutes() < other.getMinutes()

    def __le__(self, other):
        return self.getMinutes() <= other.getMinutes()

    def __gt__(self, other):
        return self.getMinutes() > other.getMinutes()

    def __ge__(self, other):
        return self.getMinutes() >= other.getMinutes()

    def __add__(self, other):
        if isinstance(other, DateTime):
            return self.getMinutes() + other.getMinutes()
        return False

class Schedule:
    def __init__(self):
        self.schedule = []

    def addEventToSchedule(self, event):
        pass

    def checkConflicts(self, eventToAdd):
        endTime = eventToAdd.getMinutes() + eventToAdd.duration
        for event in self.schedule:
            pass

class Mass(Event):
    def __init__(self, minute, hour, date, duration, game):
        super().__init__(minute, hour, date, duration, game)

    def startEvent(self):
        if self.game.priest.isAlive == True:
            self.game.priest.startJourney(vec(self.game.priest.pos), vec(self.game.alter.x, self.game.alter.y), self.game)
