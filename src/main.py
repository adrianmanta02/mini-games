import os
import sys
import pygame
from typing import List
from os import listdir
from os.path import isfile, join
from screen import Screen
from player import Player
from block import Block

pygame.init()
pygame.display.set_caption("Adrian's Supergame")

BG_COLOR = (255, 255, 255)
FPS_COUNT = 60

screen = Screen(fps = FPS_COUNT, bgcolor = BG_COLOR)
window = pygame.display.set_mode((screen.width, screen.height))
player =  Player(100, 100, 100, 100)

def draw_background(screen: Screen, window, tile_model_name: str, objects: List[Block], offset_x: int): 
    tiles, image = screen.get_background_tiles(tile_model_name)
    for tile in tiles:
        window.blit(image, tile)

    for object in objects:
        object.draw(window = window, offset_x = offset_x)
        
    pygame.display.update()

def main(window):  
    clock = pygame.time.Clock()

    block_size = 96
    offset_x = 0 
    scroll_area_width = 200

    # create the base floor of blocks
    floor = [Block((i * block_size), screen.height - block_size, block_size) for i in range(-screen.width // block_size, screen.width * 2 // block_size)]
    objects = [*floor, Block(0, screen.height - block_size * 2, block_size)]

    is_running = True
    while is_running:
        clock.tick(screen.fps) # run the game at the fps limit set by the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # prevent infinitely jumping
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        if ((player.rect.right - offset_x >= screen.width - scroll_area_width) and player.x_velocity > 0) or ((player.rect.left - offset_x <= scroll_area_width and player.x_velocity < 0)):
            offset_x += player.x_velocity

        player.handle_move(5, objects)
        player.moving_loop(screen.fps, objects)

        draw_background(screen = screen, window = window, tile_model_name = "Purple.png", objects = objects, offset_x = offset_x)
        player.draw(window = window, offset_x = offset_x)
        
        pygame.display.flip()
if __name__ == "__main__":
    main(window = window)