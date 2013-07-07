from pygame.locals import *

# Base width and height is the actual game area width and height.
BASE_WIDTH = 854
BASE_HEIGHT = 480

# Screen width and height is the game window width and height.
SCREEN_WIDTH = 854#1024
SCREEN_HEIGHT = 480#576

WINDOW_CAPTION = "mBreak"
BACKGROUND_COLOR = (64, 64, 64)
MAX_FPS = 60

""" Graphical settings """
# Ball settings
BALL_TRAILS = False

# Shadow settings
SHADOWS = True
SHADOW_OFFSET_X = 3
SHADOW_OFFSET_Y = 4
SHADOW_COLOR = (0, 0, 0, 255)
SHADOW_LINGER = True
SHADOW_LINGER_TIME = 2000
SHADOW_ALPHA_STEP = 25

# Text shadow settings
TEXT_SHADOWS = True
TEXT_SHADOW_OFFSET = 6
TEXT_SHADOW_COLOR = (0, 0, 0, 255)

# Music settings
TITLE_MUSIC = "res/music/title_screen.ogg"

# Player Left settings.
PLAYER_LEFT_NAME = "Player Left"
PLAYER_LEFT_KEY_UP = K_w
PLAYER_LEFT_KEY_DOWN = K_s

# Player Right settings.
PLAYER_RIGHT_NAME = "Player Right"
PLAYER_RIGHT_KEY_UP = K_UP
PLAYER_RIGHT_KEY_DOWN = K_DOWN

# Enables various debug information.
DEBUG_MODE = True
DEBUG_FONT = "fonts/8-BIT WONDER.TTF"