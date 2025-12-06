from typing import Tuple
import pygame
import os
from os.path import join

class Screen:
    def __init__(self, fps: int, bgcolor: Tuple[int, int, int]):
        self.width = 1000
        self.height = 800
        self.fps = fps
        self.bgcolor = bgcolor

    def set_background_color(self, bgcolor: Tuple[int, int, int]):
        self.bgcolor = bgcolor

    """Fills the background with repetitive tiles."""
    def get_background_tiles(self, tile_model_name: str):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "..", "assets", "Background", tile_model_name)
        image = pygame.image.load(image_path)
        _, _, height, width = image.get_rect()

        tiles = []
        for i in range(self.width // width + 1):
            for j in range(self.height // height + 1):
                position = [i * width, j * height] # obtain current position to place a tile
                tiles.append(position)

        return tiles, image
    