import random
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT_NAME = 'arial'

# FPS changers:
FPS = 60 # increase if laggy
SNOWFLAKES = 250 # decrease if laggy and if you are on a bad computer turn it down to one nothing below that.




# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
TITLE = "SnowGOMan"
BGCOLOR = DARKGREY


TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
FREQ = random.randint(22000,50000)

PLAYER_SPEED=300
PLAYER_IMG="player.png"
PLAYER_ROTSPD = 250

MOB_FREQ = random.randrange(600,800)
FR = random.randint(3000,16000)