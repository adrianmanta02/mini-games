import pygame

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 100)
LIGHT_YELLOW = (255, 255, 200)
DARK_BLUE = (20, 20, 60)
PURPLE = (150, 100, 200)
SHADOW_PURPLE = (100, 80, 150)  # for shadow form
ORANGE = (255, 180, 100)
GREEN = (100, 255, 150)

# gradient colors for background
SKY_TOP = (135, 206, 235)
SKY_MIDDLE = (100, 150, 200)
SKY_BOTTOM = (50, 50, 80)

# gameplay settings
GROUND_LEVEL = 650
LIGHT_DRAIN_RATE_LIGHT = 0.25  # how much it decreases in light form
LIGHT_DRAIN_RATE_SHADOW = 0.0  # does not decrease in shadow form
MAX_LIGHT = 100
STARTING_LIGHT = 100
LIGHT_ORB_VALUE = 25

# gameplay settings - light form
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 35
PLAYER_SPEED_LIGHT = 7
JUMP_POWER_LIGHT = -17
GRAVITY = 0.8

# gameplay settings - shadow form
PLAYER_SPEED_SHADOW = 4
JUMP_POWER_SHADOW = -13

# camera settings
CAMERA_OFFSET_X = 300
SPOTLIGHT_RADIUS = 250