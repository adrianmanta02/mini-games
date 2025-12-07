import pygame
from entities.player import Player
from entities.base.collidable_object import CollidableObject
from entities.base.damageable_entity import DamageableEntity
from loader.sprite_loader import SpriteLoader

sprite_loader = SpriteLoader()

class Fire(CollidableObject, DamageableEntity):
	def __init__(self, x, y, width, height):
		CollidableObject.__init__(self, x, y, width, height, "fire")
		DamageableEntity.__init__(self, damage_sound_file="damage-sound.mp3", cooldown_frames=30)
		
		self.sprites = sprite_loader.load_sprites("Traps", "Fire", width, height)
		self.animation_delay = 3
		self.current_sprite = self.sprites["off"][0]
		self.mask = pygame.mask.from_surface(self.current_sprite)
		self.animation_count = 0
		self.animation_name = "off"
		self.is_solid = True  # fire blocks player 
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
		
		# update damage cooldown
		self.update_damage_cooldown()

	def on_player_collision(self, player: Player):
		# verify collision between player and fire
		collision = pygame.sprite.collide_mask(self, player)
		self.handle_player_damage(player, collision)

	def get_json_saving_format(self, level_data: dict):
		level_data['fires'].append({
					'x': self.rect.x,
					'y': self.rect.y,
					'width': self.width,
					'height': self.height
				})