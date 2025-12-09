import pygame

from entities.base.collidable_object import CollidableObject
from loader.sprite_loader import SpriteLoader

sprite_loader = SpriteLoader()
class AnimatedSprite(CollidableObject):
	def __init__(self, x, y, width, height, object_name, sprite_path, sprite_name, default_animation):
		super().__init__(x, y, width, height, object_name)
		self.sprites = sprite_loader.load_sprites(sprite_path, sprite_name, width, height)
		self.animation_delay = 3
		self.animation_count = 0
		self.animation_name = default_animation
		
		# check for animation name in sprite keys
		if self.animation_name in self.sprites and len(self.sprites[self.animation_name]) > 0:
			self.current_sprite = self.sprites[self.animation_name][0]
		else: 
			# fallback for animation name
			first_key = list(self.sprites.keys())[0]
			print(f"This is first key list: {first_key}")
			self.current_sprite = self.sprites[first_key][0]

		self.mask = pygame.mask.from_surface(self.current_sprite)

	def set_animation(self, animation_name):
		# change current animation
		if animation_name != self.animation_name and animation_name in self.sprites:
			self.animation_name = animation_name
			self.animation_count = 0  # reset counter to start from the first frame

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
			