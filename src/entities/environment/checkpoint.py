import pygame
from entities.base.animated_sprite import AnimatedSprite
from entities.player import Player

class Checkpoint(AnimatedSprite):
	def __init__(self, x, y, width = 64, height = 64, sprite_path = "Items/Checkpoints", sprite_name = "Checkpoint"): 
		super().__init__(x, y, width, height, "checkpoint", sprite_path, sprite_name, default_animation = "Checkpoint (No Flag)")
		self.activated = False
		self.animation_finished = False
		self.is_solid = False  # player can go through checkpoint

	def activate(self):
		self.set_animation("Checkpoint (Flag Out) (64x64)")
		self.activated = True

	def update_sprite(self):
		# check for transition between 'flag out' and "flag idle" animations
		if self.activated and not self.animation_finished:
			if self.animation_name == "Checkpoint (Flag Out) (64x64)":
				sprites = self.sprites[self.animation_name]
				# when reaching last frame, switch to idle for current checkpoint
				if self.animation_count // self.animation_delay >= len(sprites) - 1:
					self.set_animation("Checkpoint (Flag Idle)(64x64)")
					self.animation_finished = True
		
		super().update_sprite()

	def on_player_collision(self, player: Player):
		if not self.activated and self.rect.colliderect(player.rect):
			self.activate()
			player.checkpoint_x = self.rect.x
			player.checkpoint_y = self.rect.y

	def get_json_saving_format(self, level_data: dict):
		if 'checkpoints' not in level_data:
			level_data['checkpoints'] = []
		
		level_data['checkpoints'].append({
			'x': self.rect.x,
			'y': self.rect.y,
			'width': self.width,
			'height': self.height
		})