import os
import pygame
from os.path import join
from collidable_object import CollidableObject

class Block(CollidableObject): 
    def __init__(self, x, y, size):  
        super().__init__(x,y,size,size)
        block = self.load_block(size)
        self.current_sprite.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.current_sprite)

    def load_block(self, size):
        # get the absolute path to the terrain assets
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = join(BASE_DIR, "..", "assets", "Terrain", "Terrain.png")
        
        # load the image with transparent bg support 
        image = pygame.image.load(path).convert_alpha()

        # create the surface and the rectangle used for collisions
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 64, size, size)

        # display the block on the screen
        surface.blit(image, (0,0), rect)

        # rescale the block
        return pygame.transform.scale2x(surface)

