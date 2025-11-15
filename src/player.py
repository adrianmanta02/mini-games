import pygame
from typing import Tuple

# using sprite for pixel-perfect collisions
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x_position, y_position, width, height):
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.x_velocity = 0
        self.y_velocity = 0 
        self.mask = None

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
