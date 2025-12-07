from typing import Tuple
import pygame
import os
from os.path import join

WIDTH = 1000
HEIGHT = 800

class Screen:
	def __init__(self, fps: int, bgcolor: Tuple[int, int, int]):
		self.width = WIDTH
		self.height = HEIGHT
		self.fps = fps
		self.bgcolor = bgcolor
		self.completion_timer = 0

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
	
	def draw_death_screen(self, window, player):
		if not player.is_dead:
			return False
		
		# semitransp overlay
		overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 180)) 
		window.blit(overlay, (0, 0))
		
		# "you are dead" message
		font_large = pygame.font.Font(None, 120)
		death_text = font_large.render("YOU ARE DEAD!", True, (255, 0, 0))
		text_rect = death_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
		
		# shadow effect for the text
		shadow_text = font_large.render("YOU ARE DEAD!", True, (100, 0, 0))
		shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 4, self.height // 2 - 46))
		window.blit(shadow_text, shadow_rect)
		window.blit(death_text, text_rect)

		font_checkpoint_info = pygame.font.Font(None, 36)
		checkpoint_info_text = font_checkpoint_info.render(f"You will be redirected to the last checkpoint...", True, (200,200,200))
		checkpoint_info_rect = checkpoint_info_text.get_rect(center = (self.width // 2, self.height // 2 + 90))
		window.blit(checkpoint_info_text, checkpoint_info_rect)

		# restart instruction
		font_small = pygame.font.Font(None, 36)
		timer_seconds = player.death_timer // self.fps
		
		if timer_seconds > 0:
			restart_text = font_small.render(f"Respawning in {timer_seconds}...", True, (200, 200, 200))
		else:
			restart_text = font_small.render("Press R to restart or ESC to quit", True, (200, 200, 200))
		
		restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 120))
		window.blit(restart_text, restart_rect)
		
		player.death_timer -= 1
		
		# reset player state after restart
		if player.death_timer <= 0:
			player.reset_player()
			return True
		
		return False
	
	def draw_level_completed_screen(self, window):
		# display the 'success' screen after reaching the end trophy
		if self.completion_timer == 0:
			self.completion_timer = self.fps * 3  # 3 seconds lifetime for the screen 
		
		# semitransp overlay
		overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 150)) 
		window.blit(overlay, (0, 0))
		
		# "level completed!" message
		font_large = pygame.font.Font(None, 100)
		completed_text = font_large.render("LEVEL COMPLETED!", True, (0, 255, 0))
		text_rect = completed_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
		
		# shadow effect for the text
		shadow_text = font_large.render("LEVEL COMPLETED!", True, (0, 100, 0))
		shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 4, self.height // 2 - 46))
		window.blit(shadow_text, shadow_rect)
		window.blit(completed_text, text_rect)
		
		# next level instruction
		font_small = pygame.font.Font(None, 36)
		timer_seconds = self.completion_timer // self.fps
		
		if timer_seconds > 0:
			next_text = font_small.render(f"Next level in {timer_seconds}...", True, (200, 200, 200))
		else:
			next_text = font_small.render("Press N for next level", True, (200, 200, 200))
			
		next_rect = next_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
		window.blit(next_text, next_rect)
		
		self.completion_timer -= 1
		
		if self.completion_timer <= 0:
			self.completion_timer = 0  # reset success screen timer for next displays
			return True
		
		return False	
	