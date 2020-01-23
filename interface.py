from settings import *

class ConversationMenu:
   def __init__(self):
       self.index = 0
       self.numberOfOptions = NUM_OF_OPTIONS
       self.mainMenu = True
       self.index = 1
       self.displayMenu()

   def displayMenu(self):
       for optionIndex in range (0, NUM_OF_OPTIONS):
           currentIndex = optionIndex + (NUM_OF_OPTIONS * self.index)
           if currentIndex > len(MAIN_MENU) - 1:
               break
           else:
               print(MAIN_MENU[optionIndex + (NUM_OF_OPTIONS * self.index)])

   def exitMenu(self):
       pass

   def displayBranch(self):
       pass


conv = ConversationMenu()
