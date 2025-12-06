import os
import sys
import json
import pygame
from typing import List
from os import listdir
from os.path import isfile, join
from screen import Screen
from player import Player
from block import Block
from fire import Fire
from checkpoint import Checkpoint

pygame.init()
pygame.display.set_caption("Adrian's Supergame")

BG_COLOR = (255, 255, 255)
FPS_COUNT = 60
INITIAL_X_POSITION = 100
INITIAL_Y_POSITION = 100

screen = Screen(fps = FPS_COUNT, bgcolor = BG_COLOR)
window = pygame.display.set_mode((screen.width, screen.height))
player =  Player(INITIAL_X_POSITION, INITIAL_Y_POSITION, 100, 100)

def draw_background(screen: Screen, window, tile_model_name: str, objects: List[Block], offset_x: int): 
	tiles, image = screen.get_background_tiles(tile_model_name)
	for tile in tiles:
		window.blit(image, tile)

	for object in objects:
		object.draw(window = window, offset_x = offset_x)
		
def load_level_from_json(level_number: int, block_size: int = 96):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	json_path = os.path.join(BASE_DIR, "..", "levels", f"level_{level_number}.json")
	
	objects = []
	
	try:
		with open(json_path, 'r') as f:
			level_data = json.load(f)
		
		# load blocks
		for block_data in level_data.get("blocks", []):
			block = Block(block_data["x"], block_data["y"], block_data["size"])
			objects.append(block)
		
		# load traps - fires
		for trap_data in level_data.get("fires", []):
			fire = Fire(trap_data["x"], trap_data["y"], 16, 32)
			fire.on()
			objects.append(fire)

		for checkpoint_data in level_data.get("checkpoints", []):
			checkpoint = Checkpoint(x = checkpoint_data["x"], 
						   			y = checkpoint_data["y"])
			objects.append(checkpoint)
		
		return objects
	
	except FileNotFoundError:
		return []
	except Exception as e:
		return []

def main(window):  
	clock = pygame.time.Clock()

	block_size = 96
	offset_x = 0 
	scroll_area_width = 200

	current_level = 1
	objects = load_level_from_json(current_level, block_size)

	# fallback for non existent level
	if not objects:
		floor = [Block((i * block_size), screen.height - block_size, block_size) 
                 for i in range(-screen.width // block_size, screen.width * 2 // block_size)]
		objects = [*floor, Block(0, screen.height - block_size * 2, block_size)]
	
	is_running = True
	while is_running:
		clock.tick(screen.fps) # run the game at the fps limit set by the screen

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
				pygame.quit()
				sys.exit()

			if player.is_dead: 
				continue # ignore any interaction if player is dead
		
			if event.type == pygame.KEYDOWN:
				# prevent infinitely jumping
				if event.key == pygame.K_SPACE and player.jump_count < 2:
					player.jump()

				if event.key == pygame.K_n:
					current_level += 1
					new_objects = load_level_from_json(current_level, block_size)
					if new_objects:
						objects = new_objects
						player.rect.x = 100
						player.rect.y = 100
						offset_x = 0
					else: 
						current_level -= 1

				if event.key == pygame.K_p: 
					if current_level > 1:
						current_level -= 1
						objects = load_level_from_json(current_level, block_size)
						player.rect.x = 100
						player.rect.y = 100
						offset_x = 0

				if event.key == pygame.K_r:
					objects = load_level_from_json(current_level, block_size)
					player.rect.x = 100 
					player.rect.y = 100
					offset_x = 0

		# handle the scrolling screen effect		
		if ((player.rect.right - offset_x >= screen.width - scroll_area_width) and player.x_velocity > 0) or ((player.rect.left - offset_x <= scroll_area_width and player.x_velocity < 0)):
			offset_x += player.x_velocity

		player.handle_move(5, objects)
		player.moving_loop(screen.fps, objects)

		for object in objects:	
			object.on_player_collision(player)
			object.update_sprite()

		draw_background(screen = screen, window = window, tile_model_name = "Purple.png", objects = objects, offset_x = offset_x)
		player.draw(window = window, offset_x = offset_x)

		# add hud
		font = pygame.font.Font(None, 36)
		level_text = font.render(f"Level {current_level}", True, (0,0,0))
		window.blit(level_text, (10, 10))

		small_font = pygame.font.Font(None, 24)
		controls = small_font.render("N: Next | P: Previous | R: Restart", True, (100, 100, 100))
		window.blit(controls, (10, screen.height - 30))

		# draw death screen - if player is dead due to fall into the void or damage dealt by enemies
		if player.is_dead:
			if screen.draw_death_screen(window, player) == True: 
				offset_x = 0

		pygame.display.flip()
if __name__ == "__main__":
	main(window = window)