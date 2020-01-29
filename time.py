MINUTES_IN_DAY = 1440
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24

class Event:
   def __init__(self, minute, hour, date, duration):
       self.startTime = DateTime(minute, hour, date)
       self.endTime = DateTime(minute, hour, date)

class DateTime:
   def __init__(self, minute, hour=None, date=None):
       if date == None:
           self.date = int(minute/MINUTES_IN_DAY)
           remainder = minute - (self.date * MINUTES_IN_DAY)
           print(remainder)
           self.hour = int(remainder / MINUTES_IN_HOUR)
           self.minute = remainder % MINUTES_IN_HOUR
       else:
           self.minute = minute
           self.hour = hour
           self.date = date

    def update():
        if self.minute == 59 and self.hour == 23:
            self.minute = 0
            self.hour = 0
        elif self.minute == 59:
            self.hour += 1
        self.minute = (self.minute + 1) % MINUTES_IN_HOUR

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

if __name__ == "__main__":
   main()
