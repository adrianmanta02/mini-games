import pygame
import math
from constants import *


class LightOrb:
    # Collectible light orb
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.collected = False
        self.pulse = 0
        self.float_offset = 0

    def update(self):
        # pulsing and floating animation
        if not self.collected:
            self.pulse += 0.1
            self.float_offset = math.sin(self.pulse) * 5

    def draw(self, screen, screen_movement):
        # drawing the orb with a glow
        if self.collected:
            return

        draw_x = self.x - screen_movement

        # screen visibility check
        if draw_x < -50 or draw_x > SCREEN_WIDTH + 50:
            return

        # position with floating effect
        draw_y = self.y + self.float_offset

        # pulsing for size
        pulse_size = math.sin(self.pulse * 2) * 3
        current_radius = self.radius + pulse_size

        # glow effect
        for i in range(3, 0, -1):
            alpha = 50 * i
            glow_radius = int(current_radius + i * 8)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            color = (*LIGHT_YELLOW[:3], alpha)
            pygame.draw.circle(glow_surface, color, (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (draw_x - glow_radius, draw_y - glow_radius))

        # main orb
        pygame.draw.circle(screen, LIGHT_YELLOW, (int(draw_x), int(draw_y)), int(current_radius))

        # white center
        pygame.draw.circle(screen, WHITE, (int(draw_x), int(draw_y)), int(current_radius // 2))

    def check_collision(self, player):
        # check if the player collected it
        if self.collected:
            return False

        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        distance = math.sqrt((player_center_x - self.x) ** 2 + (player_center_y - self.y) ** 2)

        if distance < self.radius + player.width // 2:
            self.collected = True
            return True
        return False


class Portal:
    # finish portal
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.width = 100
        self.height = GROUND_LEVEL
        self.pulse = 0
        self.particles = []

    def update(self):
        import random
        self.pulse += 0.05

        # generating particles
        if len(self.particles) < 50:
            self.particles.append({
                'x': self.x + random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(1, 3),
                'size': random.randint(2, 6)
            })

        # update particles
        for particle in self.particles:
            particle['y'] -= particle['speed']
            if particle['y'] < 0:
                particle['y'] = self.height

    def draw(self, screen, screen_movement):
        draw_x = self.x - screen_movement

        # check if visible on screen
        if draw_x < -self.width or draw_x > SCREEN_WIDTH:
            return

        # portal gradient
        for i in range(self.width):
            alpha = int(150 * (1 - abs(i - self.width / 2) / (self.width / 2)))
            color = (*GREEN[:3], alpha)

            portal_surface = pygame.Surface((2, self.height), pygame.SRCALPHA)
            portal_surface.fill(color)
            screen.blit(portal_surface, (draw_x + i, 0))

        # particles
        for particle in self.particles:
            brightness = int(200 + 55 * math.sin(self.pulse * 5))
            color = (brightness, 255, brightness)
            pygame.draw.circle(screen, color,
                               (int(draw_x + particle['x'] - self.x),
                                int(particle['y'])),
                               particle['size'])

        # glow effect pulsating
        pulse_size = math.sin(self.pulse) * 20 + 30
        glow_surface = pygame.Surface((self.width + int(pulse_size) * 2, self.height), pygame.SRCALPHA)

        for i in range(int(pulse_size), 0, -5):
            alpha = int(50 * (i / pulse_size))
            pygame.draw.rect(glow_surface, (*GREEN[:3], alpha),
                             (int(pulse_size - i), 0, self.width + i * 2, self.height))

        screen.blit(glow_surface, (draw_x - pulse_size, 0))