import pygame
import math
from constants import *


class Bug:
    # bug patrolling left-right

    def __init__(self, x, y, patrol_range=200, speed=2):
        self.start_x = x
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left
        self.animation_offset = 0
        self.color = (100, 50, 150)  # purple

    def update(self):
        # update position and animation
        # movement
        self.x += self.speed * self.direction

        # change direction at edges
        if self.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x < self.start_x:
            self.direction = 1

        # leg animation
        self.animation_offset += 0.2

    def draw(self, screen, screen_movement):
        # draw the bug
        draw_x = self.x - screen_movement

        # check if visible
        if draw_x < -50 or draw_x > SCREEN_WIDTH + 50:
            return

        # body
        body_rect = pygame.Rect(draw_x, self.y, self.width, self.height)
        pygame.draw.ellipse(screen, self.color, body_rect)
        pygame.draw.ellipse(screen, (80, 40, 120), body_rect, 2)

        # head
        head_x = draw_x + (self.width if self.direction == 1 else 0)
        pygame.draw.circle(screen, (120, 60, 180), (int(head_x), int(self.y + self.height // 2)), 8)

        # eye
        eye_x = head_x + (3 if self.direction == 1 else -3)
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(self.y + self.height // 2 - 2)), 2)

        # antennas
        antenna_base_x = head_x
        antenna_base_y = self.y + 5
        antenna_angle = math.sin(self.animation_offset) * 0.3

        for i in [-1, 1]:
            end_x = antenna_base_x + i * 8 + math.cos(antenna_angle) * 5 * self.direction
            end_y = antenna_base_y - 10 + abs(math.sin(antenna_angle)) * 3
            pygame.draw.line(screen, (150, 100, 200),
                             (int(antenna_base_x), int(antenna_base_y)),
                             (int(end_x), int(end_y)), 2)
            pygame.draw.circle(screen, (180, 130, 230), (int(end_x), int(end_y)), 3)

        # animated legs
        leg_phase = math.sin(self.animation_offset)
        for i in range(3):
            leg_x = draw_x + 8 + i * 8
            leg_y_offset = 3 * math.sin(self.animation_offset + i) if i % 2 == 0 else -3 * math.sin(
                self.animation_offset + i)
            pygame.draw.line(screen, (80, 40, 120),
                             (int(leg_x), int(self.y + self.height)),
                             (int(leg_x + 5 * self.direction), int(self.y + self.height + 8 + leg_y_offset)), 2)

    def get_rect(self):
        # for collisions
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Ant:
    # ant walking on the ground

    def __init__(self, x, y, patrol_range=150, speed=3):
        self.start_x = x
        self.x = x
        self.y = y
        self.width = 25
        self.height = 15
        self.patrol_range = patrol_range
        self.speed = speed
        self.direction = 1
        self.animation_offset = 0
        self.color = (80, 40, 40)  # dark brown

    def update(self):
        # update position
        self.x += self.speed * self.direction

        if self.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x < self.start_x:
            self.direction = 1

        self.animation_offset += 0.3

    def draw(self, screen, screen_movement):
        # draw the ant
        draw_x = self.x - screen_movement

        if draw_x < -50 or draw_x > SCREEN_WIDTH + 50:
            return

        # body
        # abdomen
        pygame.draw.circle(screen, self.color,
                           (int(draw_x), int(self.y + 7)), 8)
        # thorax
        pygame.draw.circle(screen, (100, 50, 50),
                           (int(draw_x + 10 * self.direction), int(self.y + 5)), 6)
        # head
        pygame.draw.circle(screen, (90, 45, 45),
                           (int(draw_x + 18 * self.direction), int(self.y + 5)), 5)

        # eyes
        eye_x = draw_x + 20 * self.direction
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(self.y + 4)), 2)

        # antennas
        antenna_x = draw_x + 22 * self.direction
        antenna_y = self.y + 3
        antenna_wave = math.sin(self.animation_offset) * 0.4

        for angle_offset in [-0.5, 0.5]:
            end_x = antenna_x + math.cos(antenna_wave + angle_offset) * 8 * self.direction
            end_y = antenna_y - abs(math.sin(antenna_wave + angle_offset)) * 8
            pygame.draw.line(screen, (60, 30, 30),
                             (int(antenna_x), int(antenna_y)),
                             (int(end_x), int(end_y)), 1)

        # legs
        for i in range(3):
            leg_x = draw_x + i * 6
            leg_offset = 3 * math.sin(self.animation_offset + i * 1.5)
            pygame.draw.line(screen, (60, 30, 30),
                             (int(leg_x), int(self.y + 10)),
                             (int(leg_x + 4 * self.direction), int(self.y + 14 + leg_offset)), 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Firefly_Enemy:
    # enemy firefly - flies up and down

    def __init__(self, x, y, fly_range=100, speed=1.5):
        self.start_y = y
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.fly_range = fly_range
        self.speed = speed
        self.direction = 1  # 1 = down, -1 = up
        self.glow_pulse = 0
        self.color = (255, 80, 80)  # red

    def update(self):
        # update position
        self.y += self.speed * self.direction

        if self.y > self.start_y + self.fly_range:
            self.direction = -1
        elif self.y < self.start_y:
            self.direction = 1

        self.glow_pulse += 0.1

    def draw(self, screen, screen_movement):
        # draw the enemy firefly
        draw_x = self.x - screen_movement

        if draw_x < -50 or draw_x > SCREEN_WIDTH + 50:
            return

        # red glow
        pulse = math.sin(self.glow_pulse) * 5 + 15
        glow_radius = int(25 + pulse)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)

        for i in range(glow_radius, 0, -3):
            alpha = int(80 * (i / glow_radius))
            pygame.draw.circle(glow_surface, (*self.color[:3], alpha),
                               (glow_radius, glow_radius), i)

        screen.blit(glow_surface,
                    (draw_x + self.width // 2 - glow_radius,
                     int(self.y) + self.height // 2 - glow_radius))

        # body
        pygame.draw.circle(screen, self.color,
                           (int(draw_x + self.width // 2), int(self.y + self.height // 2)),
                           self.width // 2)

        # eyes
        eye_offset = 6
        eye_size = 4
        pygame.draw.circle(screen, (150, 0, 0),
                           (int(draw_x + self.width // 2 - eye_offset), int(self.y + self.height // 2 - 2)),
                           eye_size)
        pygame.draw.circle(screen, (150, 0, 0),
                           (int(draw_x + self.width // 2 + eye_offset), int(self.y + self.height // 2 - 2)),
                           eye_size)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)