import pygame
import math
from constants import *


class Firefly:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.gravity = GRAVITY
        self.on_ground = True

        # light
        self.light_level = STARTING_LIGHT

        # form - "light" or "shadow"
        self.form = "light"

        # animaion
        self.glow_pulse = 0

    @property
    def speed(self):
        # speed depends on the form
        return PLAYER_SPEED_LIGHT if self.form == "light" else PLAYER_SPEED_SHADOW

    @property
    def jump_power(self):
        # jump power depends on the form
        return JUMP_POWER_LIGHT if self.form == "light" else JUMP_POWER_SHADOW

    def move(self, keys, level_width):
        if keys[pygame.K_LEFT] and self.x > 10:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < level_width - self.width - 10:
            self.x += self.speed

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self, ground_level):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.y >= ground_level - self.height:
            self.y = ground_level - self.height
            self.velocity_y = 0
            self.on_ground = True

    def switch_form(self):
        # manually change form
        if self.form == "light":
            self.form = "shadow"
        else:
            self.form = "light"

    def force_shadow_form(self):
        # force shadow form (when in shadow zone)
        self.form = "shadow"

    def update_light(self, dt, in_shadow_zone=False):
        # decreases light only in light form
        if self.form == "light" and not in_shadow_zone:
            self.light_level -= LIGHT_DRAIN_RATE_LIGHT * dt

        # does not decrease in shadow form
        if self.light_level < 0:
            self.light_level = 0
        if self.light_level > MAX_LIGHT:
            self.light_level = MAX_LIGHT

    def collect_light(self, amount):
        # add light
        self.light_level += amount
        if self.light_level > MAX_LIGHT:
            self.light_level = MAX_LIGHT

    def draw(self, screen, screen_movement):
        # draw the firefly
        draw_x = self.x - screen_movement
        draw_y = self.y

        center_x = int(draw_x + self.width // 2)
        center_y = int(draw_y + self.height // 2)

        # update animation for pulse
        self.glow_pulse += 0.1
        pulse = math.sin(self.glow_pulse) * 3

        if self.form == "light":
            # light form

            # outer glow rings
            glow_colors = [
                (200, 200, 120, 30),
                (220, 220, 140, 50),
                (240, 240, 160, 70),
            ]

            base_radius = 40
            for i, color in enumerate(glow_colors):
                radius = int(base_radius - i * 8 + pulse)
                glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, color, (radius, radius), radius)
                screen.blit(glow_surf, (center_x - radius, center_y - radius))

            # main body - bright yellow
            pygame.draw.circle(screen, (255, 255, 100), (center_x, center_y), 17)

            # inner highlight
            pygame.draw.circle(screen, (255, 255, 200), (center_x, center_y), 10)

            eye_offset = 8
            eye_size = 5

        else:
            # shadow form

            # purple glow rings
            glow_colors = [
                (100, 80, 150, 30),
                (120, 90, 170, 50),
                (140, 100, 190, 70),
            ]

            base_radius = 30
            for i, color in enumerate(glow_colors):
                radius = int(base_radius - i * 6 + pulse)
                glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, color, (radius, radius), radius)
                screen.blit(glow_surf, (center_x - radius, center_y - radius))

            # main body - purple
            pygame.draw.circle(screen, (130, 90, 180), (center_x, center_y), 17)

            # inner highlight
            pygame.draw.circle(screen, (160, 120, 200), (center_x, center_y), 10)

            eye_offset = 7
            eye_size = 4

        # eyes - black circles
        pygame.draw.circle(screen, BLACK,
                           (center_x - eye_offset, center_y - 3),
                           eye_size)
        pygame.draw.circle(screen, BLACK,
                           (center_x + eye_offset, center_y - 3),
                           eye_size)

        # white highlights
        pygame.draw.circle(screen, WHITE,
                           (center_x - eye_offset + 1, center_y - 4), 2)
        pygame.draw.circle(screen, WHITE,
                           (center_x + eye_offset + 1, center_y - 4), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_platform_collision(self, platforms):
        player_rect = self.get_rect()
        for platform in platforms:
            platform_rect = platform.get_rect()
            if player_rect.colliderect(platform_rect):
                if self.velocity_y > 0 and player_rect.bottom >= platform_rect.top:
                    self.y = platform_rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    return True
        return False