import pygame
from player import Player

class CollidableObject(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, name = None):
		super().__init__()
		self.rect = pygame.Rect(x, y, width, height)
		# support transparent background using srcalpha
		self.current_sprite = pygame.Surface((width, height), pygame.SRCALPHA)
		self.width = width
		self.height = height
		self.name = name

	def draw(self, window, offset_x):
		window.blit(self.current_sprite, (self.rect.x - offset_x, self.rect.y))

	def on_player_collision(self, player: Player):
		pass
	
	def update_sprite(self):
		pass

	def get_json_saving_format(self, level_data: dict):
		pass