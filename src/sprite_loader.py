import os
from os.path import join, isfile
import pygame

class SpriteLoader:
    def __init__(self):
        self.all_sprites = None

    """Flip the sprites since the representation for the assets consist only of a direction"""
    def flip(self, sprites):
        return [pygame.transform.flip(surface = sprite, flip_x = True, flip_y = False) for sprite in sprites]
    
    def load_sprites(self, directory1: str, directory2: str, width: int, height: int, direction = False):
        # obtain the path to the folder containing the spritesheets
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, "..", "assets", directory1, directory2)

        # get the paths for all spritesheets
        images = [image for image in os.listdir(path) if isfile(os.path.join(path, image))]

        all_sprites = {}
        for image in images:
            # each image contains a spritesheet 
            spritesheet = pygame.image.load(os.path.join(path, image))

            # in a spritesheet there are multiple sprites.
            sprites = []
            for i in range(spritesheet.get_width() // width):
                # each sprite is a pygame Surface that can be displayed on the screen
                surface = pygame.Surface(size = (width, height), flags = pygame.SRCALPHA, depth = 32)

                # get the geometrical side of it, that can be handled with the collisions and movements
                rect = pygame.Rect(i * width, 0, width, height)

                # display the surface 
                surface.blit(source = spritesheet, dest = (0, 0), area = rect)

                sprites.append(pygame.transform.scale2x(surface=surface))

            key = image.replace(".png", "") # set the keys for the dictionary based on the file names
            print("\nThis my key: ", key)
            print("This the sprites i got for the key: ", sprites)
            if direction:
                # asign correct stripes for direction purposes
                all_sprites[key + "_right"] = sprites
                all_sprites[key + "_left"] = self.flip(sprites)

            else: 
                all_sprites[key] = sprites

        print("\n\n\nSpriteeees: ", all_sprites)
        return all_sprites 