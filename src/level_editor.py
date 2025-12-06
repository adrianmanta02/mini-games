import os
import sys
import pygame
import json
from typing import List, Dict
from screen import Screen
from player import Player
from block import Block
from fire import Fire

pygame.init()
pygame.display.set_caption("Level Editor - Click to place blocks")

BG_COLOR = (255, 255, 255)
FPS_COUNT = 60

class LevelEditor:
	def __init__(self, block_size: int = 96, screen_height: int = 800, screen_width: int = 1000):
		self.block_size = block_size
		self.screen_height = screen_height
		self.screen_width = screen_width
		self.objects = []
		self.grid_visible = True
		self.coords_visible = True
		self.current_tool = "block"  # "block" or "fire"
		self.offset_x = 0
		
		# Colors
		self.GRID_COLOR = (200, 200, 200)
		self.COORD_COLOR = (100, 100, 100)
		self.HIGHLIGHT_COLOR = (255, 255, 0, 100)
		
	def draw_grid(self, window, offset_x: int):
		# draw grid with vertical and horizontal lines
		if not self.grid_visible:
			return
			
		# vertical rules - space between = size of a block = 96pixels
		for x in range(-self.screen_width, self.screen_width * 10, self.block_size):
			# adjust position via camera offset
			screen_x = x - offset_x

			# check if the line is visible on the screen
			if -self.block_size <= screen_x <= self.screen_width + self.block_size:
				# draw only within the range of a block and the screen's width + extra block size
				
				VERTICAL_STARTING_POINT = (screen_x, 0)
				VERTICAL_ENDING_POINT = (screen_x, self.screen_height)

				pygame.draw.line(surface = window, 
					 			color = self.GRID_COLOR, 
							   	start_pos = VERTICAL_STARTING_POINT, 
							   	end_pos = VERTICAL_ENDING_POINT, 
							   	width = 1)
		
		# horizontal rules
		for y in range(0, self.screen_height, self.block_size):
			pygame.draw.line(surface = window, 
							color = self.GRID_COLOR, 
						   	start_pos = (0, y), 
						   	end_pos = (self.screen_width, y), 
							width = 1)
	
	def draw_coordinates(self, window, offset_x: int):
		# draw coordinates on the grid
		if not self.coords_visible:
			return
			
		font = pygame.font.Font(None, 16)
		
		# coordinates for any cell
		for x in range(-self.screen_width, self.screen_width * 10, self.block_size):
			for y in range(0, self.screen_height, self.block_size):
				screen_x = x - offset_x
				
				# check if current block is visible on the screen
				if -self.block_size <= screen_x <= self.screen_width:
					# place coordinates on the blokc
					coord_text = f"({x},{y})"
					text_surface = font.render(coord_text, True, self.COORD_COLOR)
					window.blit(text_surface, (screen_x + 2, y + 2))
	
	def draw_mouse_highlight(self, window, mouse_pos, offset_x: int):
		# highlight the cell that has the cursor on it
		mouse_x, mouse_y = mouse_pos
		
		# calculate the real position on the screen
		world_x = mouse_x + offset_x
		
		# grid snap - to the closest cell start
		grid_x = (world_x // self.block_size) * self.block_size
		grid_y = (mouse_y // self.block_size) * self.block_size
		
		# draw highlight - a surface with the size of a block
		screen_x = grid_x - offset_x
		highlight_surface = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
		highlight_surface.fill(self.HIGHLIGHT_COLOR)
		window.blit(highlight_surface, (screen_x, grid_y))
		
		# display coordinates 
		font = pygame.font.Font(None, 24)
		coord_text = f"Position: ({grid_x}, {grid_y})"
		text_surface = font.render(coord_text, True, (255, 0, 0))
		window.blit(text_surface, (10, self.screen_height - 30))
		
		return grid_x, grid_y
	
	def add_object(self, x: int, y: int):
		# add an object (block, trap etc) to the worldspace

		# check if there is already an object linked to this pair of coordinates
		for obj in self.objects:
			if obj.rect.x == x and obj.rect.y == y:
				return  # no need for duplicates
		
		if self.current_tool == "block":
			self.objects.append(Block(x, y, self.block_size))
		elif self.current_tool == "fire":
			# place fire on the ground
			fire = Fire(x, y + self.block_size - 64, 16, 32)
			fire.on()
			self.objects.append(fire)
	
	def remove_object(self, x: int, y: int):
		# keep only the objects having the coordinates different than the pair provided
		self.objects = [obj for obj in self.objects if not (obj.rect.x == x and obj.rect.y == y)]
	
	def save_level(self, filename: str):
		# save configuration in json files
		level_data = {
			'blocks': [],
			'fires': []
		}
		
		for obj in self.objects:
			obj.get_json_saving_format(level_data)
		
		# save everything in folder 'levels/'
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		levels_dir = os.path.join(BASE_DIR, "..", "levels")
		os.makedirs(levels_dir, exist_ok=True)
		
		filepath = os.path.join(levels_dir, filename)
		
		# write json data
		with open(filepath, 'w') as f:
			json.dump(level_data, f, indent=2)
		
		print(f"Level saved to: {filepath}")
		print(f"Total blocks: {len(level_data['blocks'])}")
		print(f"Total fires: {len(level_data['fires'])}")
	
	def load_level(self, filename: str):
		# load a level configuration from a JSON file
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		filepath = os.path.join(BASE_DIR, "..", "levels", filename)
		
		if not os.path.exists(filepath):
			print(f"Level file not found: {filepath}")
			return
		
		with open(filepath, 'r') as f:
			level_data = json.load(f)
		
		# delete all current objects
		self.objects = []
		
		# load blocks
		for block_data in level_data.get('blocks', []):
			self.objects.append(Block(
				block_data['x'],
				block_data['y'],
				block_data['size']
			))
		
		# load fire traps
		for fire_data in level_data.get('fires', []):
			fire = Fire(
				fire_data['x'],
				fire_data['y'],
				fire_data['width'],
				fire_data['height']
			)
			fire.on()
			self.objects.append(fire)
		
		print(f"Level loaded: {len(level_data.get('blocks', []))} blocks, {len(level_data.get('fires', []))} fires")
	
def draw_hud(window, editor: LevelEditor, screen: Screen):
	# draw hud with instructions and informations
	font = pygame.font.Font(None, 24)
	small_font = pygame.font.Font(None, 20)
	
	# semitransparent background for the hud
	hud_surface = pygame.Surface((screen.width, 120), pygame.SRCALPHA)
	hud_surface.fill((0, 0, 0, 180))
	window.blit(hud_surface, (0, 0))
	
	title = font.render("LEVEL EDITOR", True, (255, 255, 255))
	window.blit(title, (10, 10))
	
	tool_color = (0, 255, 0) if editor.current_tool == "block" else (255, 100, 0)
	tool_text = small_font.render(f"Tool: {editor.current_tool.upper()}", True, tool_color)
	window.blit(tool_text, (10, 35))
	
	# stats for the objects added already
	num_blocks = len([o for o in editor.objects if isinstance(o, Block)])
	num_fires = len([o for o in editor.objects if isinstance(o, Fire)])
	stats = small_font.render(f"Blocks: {num_blocks} | Fires: {num_fires}", True, (255, 255, 255))
	window.blit(stats, (10, 55))
	
	instructions = [
		"LEFT CLICK: Place | RIGHT CLICK: Remove | 1: Block | 2: Fire",
		"G: Toggle Grid | C: Toggle Coords | S: Save | L: Load,",
		"ARROWS: Move camera | SPACE: Test level | ESC: Clear all"
	]
	
	y_pos = 75
	for instruction in instructions:
		text = small_font.render(instruction, True, (200, 200, 200))
		window.blit(text, (10, y_pos))
		y_pos += 15

def main():
	screen = Screen(fps=FPS_COUNT, bgcolor=BG_COLOR)
	window = pygame.display.set_mode((screen.width, screen.height))
	clock = pygame.time.Clock()
	
	block_size = 96
	editor = LevelEditor(block_size, screen.height, screen.width)
	
	# player for testing, not visible on the screen though
	player = Player(100, 100, 100, 100)
	test_mode = False
	# area from which the camera scroll is triggered 
	scroll_area_width = 200
	
	running = True
	mouse_pressed = False
	
	while running:
		clock.tick(FPS_COUNT)
		mouse_pos = pygame.mouse.get_pos()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
			elif event.type == pygame.KEYDOWN:
				# toggle grid
				if event.key == pygame.K_g:
					editor.grid_visible = not editor.grid_visible
					print(f"Grid: {'ON' if editor.grid_visible else 'OFF'}")
				
				# toggle coordinates
				elif event.key == pygame.K_c:
					editor.coords_visible = not editor.coords_visible
					print(f"Coordinates: {'ON' if editor.coords_visible else 'OFF'}")
				
				# switch tools
				elif event.key == pygame.K_1:
					editor.current_tool = "block"
					print("Tool: BLOCK")
				
				elif event.key == pygame.K_2:
					editor.current_tool = "fire"
					print("Tool: FIRE")
				
				# save level
				elif event.key == pygame.K_s:
					filename = input("Enter filename (e.g., my_level.json): ")
					if not filename.endswith('.json'):
						filename += '.json'
					editor.save_level(filename)
				
				# load level
				elif event.key == pygame.K_l:
					filename = input("Enter filename to load (e.g., my_level.json): ")
					if not filename.endswith('.json'):
						filename += '.json'
					editor.load_level(filename)
								
				# clear all
				elif event.key == pygame.K_ESCAPE:
					confirm = input("Clear all objects? (y/n): ")
					if confirm.lower() == 'y':
						editor.objects = []
						print("All objects cleared")
				
				# test mode
				elif event.key == pygame.K_SPACE:
					test_mode = not test_mode
					if test_mode:
						player.rect.x = 100
						player.rect.y = 100
						print("TEST MODE - Use arrows to move, SPACE to jump, SPACE again to exit")
					else:
						print("EDITOR MODE")
				
				# player jump in test mode
				elif event.key == pygame.K_UP and test_mode and player.jump_count < 2:
					player.jump()
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pressed = True
			
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_pressed = False
		
		# camera movement - only in editor modwe
		if not test_mode:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				editor.offset_x -= 10
			if keys[pygame.K_RIGHT]:
				editor.offset_x += 10
		
		# player control
		if test_mode:
			if ((player.rect.right - editor.offset_x >= screen.width - scroll_area_width) and player.x_velocity > 0) or \
			   ((player.rect.left - editor.offset_x <= scroll_area_width and player.x_velocity < 0)):
				editor.offset_x += player.x_velocity
			
			player.handle_move(5, editor.objects)
			player.moving_loop(screen.fps, editor.objects)
			
			# update animations 
			for obj in editor.objects:
				obj.update_sprite()
		
		# mouse interactions
		if not test_mode and mouse_pressed:
			grid_x, grid_y = (mouse_pos[0] + editor.offset_x) // block_size * block_size, \
							mouse_pos[1] // block_size * block_size
			
			if pygame.mouse.get_pressed()[0]:  # left click - add
				editor.add_object(grid_x, grid_y)
			elif pygame.mouse.get_pressed()[2]:  # right click - remove
				editor.remove_object(grid_x, grid_y)
		
		# drawing
		window.fill(BG_COLOR)
		
		# draw background tiles
		tiles, image = screen.get_background_tiles("Purple.png")
		for tile in tiles:
			window.blit(image, tile)
		
		# draw grid
		editor.draw_grid(window, editor.offset_x)
		
		# draw coordinates on grid
		if not test_mode:
			editor.draw_coordinates(window, editor.offset_x)
		
		# draw objects
		for obj in editor.objects:
			obj.draw(window, editor.offset_x)
			obj.update_sprite()
		
		# draw mouse highlight - only in editor mode
		if not test_mode:
			editor.draw_mouse_highlight(window, mouse_pos, editor.offset_x)
		
		# draw player in test mode
		if test_mode:
			player.draw(window, editor.offset_x)
		
		# draw HUD
		if not test_mode:
			draw_hud(window, editor, screen)
		else:
			# minimal HUD in test mode
			font = pygame.font.Font(None, 24)
			test_text = font.render("TEST MODE - SPACE to exit", True, (255, 0, 0))
			window.blit(test_text, (screen.width // 2 - 150, 10))
		
		pygame.display.flip()
	
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
