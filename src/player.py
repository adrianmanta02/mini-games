import pygame
from typing import Tuple
from sprite_loader import SpriteLoader
from screen import HEIGHT

sprite_loader = SpriteLoader()
FPS_COUNT = 60

# using sprite for pixel-perfect collisions
class Player(pygame.sprite.Sprite):
	COLOR = (255, 0, 0)
	GRAVITY = 1

	def __init__(self, x_position, y_position, width, height):
		self.rect = pygame.Rect(x_position, y_position, width, height)
		self.x_velocity = 0
		self.y_velocity = 1
		self.direction = "right" # it will help with player's animation handling
		self.animation_count = 0
		self.fall_count = 0 # timestamp for falling, the longer the player falls, the faster it is
		self.jump_count = 0
		self.sprites = sprite_loader.load_sprites("MainCharacters", "VirtualGuy", 32, 32, True)
		self.current_sprite = self.sprites["idle_right"][0]
		self.mask = pygame.mask.from_surface(self.current_sprite)
		self.animation_delay = 5 # animation delay between sprite changes

		self.lives = 5
		self.hit_count = 0
		self.hit_flag = False
		self.hit_timer = 0
		
		self.coins_earned = 0
		self.is_dead = False
		self.death_timer = 0

		self.checkpoint_x = x_position
		self.checkpoint_y = y_position

		self.reached_end_level = False
	
	def jump(self):
		self.y_velocity = -self.GRAVITY * 9 # change the direction of the velocity -> negative means moving upwards
		self.animation_count = 0

		self.jump_count += 1
	  
		if self.jump_count == 1:
			self.fall_count # as soon as player jumps, set the fall count to 0, in order not to be directly dragged down by the gravity

	def landed(self):
		self.fall_count = 0 # reset adding gravity counter
		self.y_velocity = 0 # remove floating effect
		self.jump_count = 0 

	def hit(self):
		self.lives -= 1
		self.hit_flag = True
		self.hit_timer = FPS_COUNT // 4 
		print("Lives: ", self.lives)

		# check if alive
		if self.lives == 0:
			self.is_dead = True
			self.death_timer = FPS_COUNT * 3 # display the "dead" message for 3 seconds 
	
	def hithead(self):
		self.fall_count = 0
		self.y_velocity *= -1 # bounce backwards
	
	def handle_vertical_collision(self, objects, dy):
		collided_objects = []
		for object in objects:
			if pygame.sprite.collide_mask(self, object):
				# check collisions
				object.on_player_collision(self)
				
				# only solid objects are blocking the movement
				if hasattr(object, 'is_solid') and object.is_solid:
					if dy > 0:
						self.rect.bottom = object.rect.top
						self.landed()
					elif dy < 0:
						self.rect.top = object.rect.bottom
						self.hithead()

					collided_objects.append(object)

		return collided_objects
	
	def move(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy
		
	def handle_horizontal_collision(self, objects, dx):
		self.move(dx, 0) # check if the player were to move, would they hit a block?
		self.update() # update the rectangle and the mask before handling the collision

		collided_object = None
		for object in objects:
			# # ignore non solid objects
			if hasattr(object, 'is_solid') and not object.is_solid:
				continue
			if pygame.sprite.collide_rect(self, object): 
				collided_object = object
				break
		
		self.move(-dx, 0)
		self.update()
		return collided_object

	def handle_move(self, velocity, object_colliding_with):
		keys = pygame.key.get_pressed()
		self.x_velocity = 0

		collide_left = self.handle_horizontal_collision(object_colliding_with, -velocity * 2)
		collide_right = self.handle_horizontal_collision(object_colliding_with, velocity * 2)

		if keys[pygame.K_LEFT] and not collide_left:
			self.move_left(velocity)
		
		if keys[pygame.K_RIGHT] and not collide_right:
			self.move_right(velocity)

		self.handle_vertical_collision(object_colliding_with, self.y_velocity)
 
	def move_right(self, velocity: int):
		self.x_velocity += velocity
		if self.direction != "right":
			self.direction = "right"
			self.animation_count = 0

	def move_left(self, velocity: int):
		self.x_velocity -= velocity
		if self.direction != "left":    
			self.direction = "left"
			self.animation_count = 0

	def moving_loop(self, fps_count, objects):
		self.rect.x += self.x_velocity

		if self.check_fallen_void(HEIGHT) == True:
			return 
		
		# gravity
		self.y_velocity += min(1, self.GRAVITY / fps_count) * self.fall_count
		self.rect.y += self.y_velocity
		self.fall_count += 1

		# vertical collisions
		self.handle_vertical_collision(objects, self.y_velocity)

		self.update_sprite()

	def draw(self, window: pygame.Surface, offset_x: int):
		window.blit(source = self.current_sprite, dest = (self.rect.x - offset_x, self.rect.y))

	def update_sprite(self):
		sprite = "idle" # default for not moving or jumping

		# jumping 
		if self.y_velocity < 0: 
			if self.jump_count == 1:
				sprite = "jump"
			elif self.jump_count == 2:
				sprite = "double_jump"
		# falling 
		elif self.y_velocity > self.GRAVITY * 2:
			sprite = "fall"
		 
		# running+
		elif self.x_velocity != 0: # movement detected -> load moving sprites
			sprite = "run"

		# getting damaged 
		elif self.hit_flag == True:
			sprite = "hit"
			self.hit_timer -= 1
			if self.hit_timer <= 0:
				self.hit_flag = False
		
		# get the corresponding sprites according to the direction our player is facing
		sprite_sheet = sprite + "_" + self.direction
		sprites = self.sprites[sprite_sheet]

		# animation effect for changing the player's model
		index = (self.animation_count // self.animation_delay) % len(sprites)
		self.current_sprite = sprites[index]

		self.animation_count += 1
		self.update()

	def update(self):
		# constantly adjust the rectangle for bounding the character based on the sprite
		self.rect = self.current_sprite.get_rect(topleft = (self.rect.x, self.rect.y))

		# perform pixel perfect collision
		self.mask = pygame.mask.from_surface(self.current_sprite)

	def reset_player(self):
		self.coins_earned = 0
		self.lives = 5
		self.current_sprite = self.sprites["idle_right"][0]
		self.is_dead = False
		self.death_timer = 0
		self.rect.x = self.checkpoint_x
		self.rect.y = self.checkpoint_y

	def check_fallen_void(self, maximum_height_allowed_for_screen: int): 
		threshold = 10
		if self.rect.y > maximum_height_allowed_for_screen + threshold:
			if not self.is_dead:
				self.is_dead = True
				self.death_timer = FPS_COUNT * 3
			return True
		return False
