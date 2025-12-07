import pygame
from entities.base.animated_sprite import AnimatedSprite
from entities.player import Player

class End(AnimatedSprite):
	def __init__(self, x, y, width = 64, height = 64, sprite_path = "Items/Checkpoints", sprite_name = "End"): 
		super().__init__(x, y, width, height, "end", sprite_path, sprite_name, default_animation = "End (Idle)")
		self.activated = False
		self.animation_finished = False
		self.is_solid = False  # player can go through end trophy

	def activate(self):
		self.set_animation("End (Pressed) (64x64)")
		self.activated = True

	def update_sprite(self):
		# check if there s the need of making the transition between animation modes
		if self.activated and not self.animation_finished:
			if self.animation_name == "End (Pressed) (64x64)":
				sprites = self.sprites[self.animation_name]
				# when reaching the last frame for 'idle', switch to 'pressed';
				if self.animation_count // self.animation_delay >= len(sprites) - 1:
					self.set_animation("End (Idle)")
					self.animation_finished = True
		
		super().update_sprite()

	def on_player_collision(self, player: Player):
		if not self.activated and self.rect.colliderect(player.rect):
			self.activate()
			player.coins_earned += 100
			player.reached_end_level = True

	def get_json_saving_format(self, level_data: dict):
		level_data['end'] = {
			'x': self.rect.x,
			'y': self.rect.y,
			'width': self.width,
			'height': self.height
		}