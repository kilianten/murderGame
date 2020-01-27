# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,127,80)

# game settings
SETTINGS = {"ISFULLSCREEN":"True"}
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "MurderVille"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#playerSettings
PLAYER_SPEED = 250
PLAYER_IMAGE = "max.png"
PLAYER_IMAGE_FOWARD = "maxWalkingForward1.png"
PLAYER_IMAGE_RIGHT = "maxWalkinRight1.png"
PLAYER_WALKING_DOWN = ["maxWalking1.png", "maxWalking2.png"]
PLAYER_WALKING_FOWARD = ["maxWalkingForward2.png", "maxWalkingForward3.png"]
PLAYER_WALKING_RIGHT = ["maxWalkinRight2.png", "maxWalkinRight3.png"]
WALKING_ANIMATION_UPDATE = 200
PLAYER_HITBOX_OFFSET = 40

#clock SETTINGS
CLOCK_NUMBERS = ["clock0.png", "clock1.png", "clock2.png", "clock3.png", "clock4.png", "clock5.png", "clock6.png", "clock7.png", "clock8.png", "clock9.png"]
CLOCK_SEMICOLON = "clockSemicolon.png"
CLOCK_UPDATE = 1000

#DateSettings
DAYS_OF_WEEK = ["mon.png"]

#items
ACOUSTIC_GUITAR = "acousticGuitar.png"
SPEECH_BUBBLE_IMAGE = "speechBubble.png"
ALTER_IMAGE = "alter.png"

#TILES
BRICKWALL = "brickWall32.png"
BRICKWALL_CORNER = "brickWallCorner.png"
GRASS01 = "grass.png"

#TOWNSPEOPLE
#Priest
PRIEST_IMAGE = "priest.png"
PRIEST_READING_ANIM = ["priestReading1.png", "priestReading2.png", "priestReading3.png", "priestReading4.png", "priestReading5.png", "priestReading6.png", "priestReading7.png", "priestReading8.png", "priestReading9.png", "priestReading10.png", "priestReading11.png", "priestReading12.png", "priestReading13.png"]

#HUD
ICON_HOME = "home.png"
ARROW_RIGHT = "arrowRight.png"
ICON_SIZE = 5
CONVERSATION_HUD = "conversationMenu.png"

#MAPFILES
DEFAULT_MAP = "map1.png"

#mapColours GUIDE
#77A856:grass01
#773228:brickwall
#8e448c:alter

#townsPeople
PRIEST_SPEED = 20

#conversations
NUM_OF_OPTIONS = 3
SPEECH_TREE = {"Chat": ["How are you?", "Whats up"], "Argue": ["I hate you"], "Insult":["You suck"], "Compliment":["You look good"]}
MAIN_MENU = []
for key in SPEECH_TREE:
   MAIN_MENU.append(key)
