import pygame
from typing import Tuple
from sprite_loader import SpriteLoader

sprite_loader = SpriteLoader()

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
        self.sprites = sprite_loader.load_sprites("MainCharacters", "VirtualGuy", 32, 32, True)
        self.current_sprite = self.sprites["idle_right"][0]
        self.mask = pygame.mask.from_surface(self.current_sprite)
        self.animation_delay = 5 # animation delay between sprite changes

    def landed(self):
        self.fall_count = 0 # reset adding gravity counter
        self.y_velocity = 0 
        self.jump_count = 0 

    def hithead(self):
        self.fall_count = 0
        self.y_velocity *= -1 # bounce backwards
    
    def handle_vertical_collision(self, objects, dy):
        collided_objects = []
        for object in objects:
            if pygame.sprite.collide_mask(self, object):
                if dy > 0:
                    self.rect.bottom = object.rect.top
                    self.landed()
                elif dy < 0:
                    self.rect.top = object.rect.bottom
                    self.hithead()

                collided_objects.append(object)

        return collided_objects

    def handle_move(self, velocity, object_colliding_with):
        keys = pygame.key.get_pressed()
        self.x_velocity = 0

        if keys[pygame.K_LEFT]:
            self.move_left(velocity)
        
        if keys[pygame.K_RIGHT]:
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

        # gravity
        self.y_velocity += min(1, self.GRAVITY / fps_count) * self.fall_count
        self.rect.y += self.y_velocity
        self.fall_count += 1
        
        # vertical collisions
        self.handle_vertical_collision(objects, self.y_velocity)

        self.update_sprite()

    def draw(self, window: pygame.Surface):
        window.blit(source = self.current_sprite, dest = (self.rect.x, self.rect.y))

    def update_sprite(self):
        sprite = "idle" # default for not moving or jumping

        if self.x_velocity != 0: # movement detected -> load moving sprites
            sprite = "run"

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

