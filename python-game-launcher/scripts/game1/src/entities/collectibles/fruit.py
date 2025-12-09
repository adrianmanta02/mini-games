import pygame
from entities.base.animated_sprite import AnimatedSprite
import os
import random

def get_fruit_folders(folder_path: str):
	all_entries = os.listdir(folder_path)
	
	# filter for directories only (now we have Apple/, Bananas/ and so on)
	fruit_folders = [entry for entry in all_entries 
	                 if os.path.isdir(os.path.join(folder_path, entry))]
	return fruit_folders

class Fruit(AnimatedSprite):
	def __init__(self, x, y, width = 32, height = 32, sprite_path = "Items/Fruits", sprite_name = None):
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(BASE_DIR, "..", "..", "..", "assets", sprite_path)
		
		# get all fruit folder name
		fruit_names = get_fruit_folders(path)
		
		# select a random fruit
		if sprite_name is None:
			random_fruit_name_index = random.randint(0, len(fruit_names) - 1)
			sprite_name = fruit_names[random_fruit_name_index]
		
		super().__init__(x, y, width, height, "fruit", sprite_path, sprite_name, default_animation = sprite_name)
		
		self.sprite_name = sprite_name
		self.is_solid = False
		self.eliminate_from_map_once_touched = False

	def on_player_collision(self, player):
		if self.rect.colliderect(player.rect):
			player.coins_earned += 20
			# check player character change
			player.change_character()
			print(f"Those are my coins: {player.coins_earned}")
			print(f"This is my current character: {player.current_character}")
			self.eliminate_from_map_once_touched = True


	def get_json_saving_format(self, level_data):
		# Initialize fruits list if not exists
		if 'fruits' not in level_data:
			level_data['fruits'] = []
		
		level_data['fruits'].append({
			'x': self.rect.x,
			'y': self.rect.y,
			'width': self.width,
			'height': self.height
		})
		