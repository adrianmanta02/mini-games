import os
import sys
import pygame
from os import listdir
from os.path import isfile, join
from screen import Screen

pygame.init()
pygame.display.set_caption("Adrian's Supergame")

BG_COLOR = (255, 255, 255)
FPS_COUNT = 60

screen = Screen(fps = FPS_COUNT, bgcolor = BG_COLOR)
window = pygame.display.set_mode((screen.width, screen.height))

def draw_background(screen: Screen, window, tile_model_name: str): 
    tiles, image = screen.get_background_tiles(tile_model_name)
    for tile in tiles:
        window.blit(image, tile)

    pygame.display.update()

def main(window):  
    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        clock.tick(screen.fps) # run the game at the fps limit set by the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                sys.exit()

        draw_background(screen = screen, window = window, tile_model_name = "Purple.png")

if __name__ == "__main__":
    main(window = window)