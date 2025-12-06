import pygame
import os
from os.path import join
from player import Player
from collidable_object import CollidableObject
from sprite_loader import SpriteLoader

sprite_loader = SpriteLoader()

def load_damage_sound():
	BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
	path_to_damage_sound = join(BASE_DIRECTORY, "..", "assets", "Sound", "damage-sound.mp3")
	return path_to_damage_sound

class Fire(CollidableObject):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, "fire")
		self.sprites = sprite_loader.load_sprites("Traps", "Fire", width, height)
		self.animation_delay = 3
		self.current_sprite = self.sprites["off"][0]
		self.mask = pygame.mask.from_surface(self.current_sprite)
		self.animation_count = 0
		self.animation_name = "off"
		self.damage_sound = load_damage_sound()
	def on(self):
		self.animation_name = "on"

	def off(self):
		self.animation_name = "off"

	def update_sprite(self):
		sprites = self.sprites[self.animation_name]

		# animation effect for changing the player's model
		index = (self.animation_count // self.animation_delay) % len(sprites)
		self.current_sprite = sprites[index]

		self.animation_count += 1

		# constantly adjust the rectangle for bounding the character based on the sprite
		self.rect = self.current_sprite.get_rect(topleft = (self.rect.x, self.rect.y))

		# perform pixel perfect collision
		self.mask = pygame.mask.from_surface(self.current_sprite)

		# reset the animation index often times, because it is a static object on the screen
		if self.animation_count // self.animation_delay >= len(sprites):
			self.animation_count = 0

	def on_player_collision(self, player: Player):
		pygame.mixer.music.load(self.damage_sound)
		pygame.mixer.music.play()
		player.hit()

	def get_json_saving_format(self, level_data: dict):
		level_data['fires'].append({
					'x': self.rect.x,
					'y': self.rect.y,
					'width': self.width,
					'height': self.height
				})