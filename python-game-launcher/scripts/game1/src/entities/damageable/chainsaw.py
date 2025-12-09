import pygame
from entities.base.animated_sprite import AnimatedSprite
from entities.base.damageable_entity import DamageableEntity

class Chainsaw(AnimatedSprite, DamageableEntity):
	def __init__(self, x, y, width = 38, height = 38, sprite_path = "Traps", sprite_name = "Saw"):
		AnimatedSprite.__init__(self, x, y, width, height, "saw", sprite_path, sprite_name, default_animation = "on")
		DamageableEntity.__init__(self, damage_sound_file=None, cooldown_frames=60)  # No sound for chainsaw
		
		self.is_solid = True
		self.initial_x = x  # save initial position for repetitive movement
		self.moving_right = False  # direction of movement
		self.movement_distance = 200  # oscillation distance
		self.speed = 2  # moving speed 
	def update_sprite(self):
		super().update_sprite()
		
		# movement left to right to left in a loop
		if not self.moving_right:
			# moving towards left -> decrement x position of rect figure 
			self.rect.x -= self.speed
			# once reaching left limit, change direction
			if self.rect.x <= self.initial_x - self.movement_distance:
				self.moving_right = True
		else:
			# moving towards right (x increasing)
			self.rect.x += self.speed
			# once reaching back the initial position, change it
			if self.rect.x >= self.initial_x:
				self.moving_right = False
		
		# update damage cooldown
		self.update_damage_cooldown()

	def on_player_collision(self, player):
		collision = pygame.sprite.collide_mask(self, player)
		self.handle_player_damage(player, collision)

	def get_json_saving_format(self, level_data: dict):
		level_data['chainsaws'].append({
			'x': self.initial_x,  # save initial position, not current (moving) position
			'y': self.rect.y,
			'width': self.width,
			'height': self.height
		})
