import pygame
from constants import *


class Platform:

    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type

        if platform_type == "light":
            self.color = (200, 200, 100)
            self.border_color = (255, 255, 150)
        elif platform_type == "shadow":
            self.color = (80, 80, 120)
            self.border_color = (120, 120, 160)
        else:
            self.color = (100, 150, 100)
            self.border_color = (150, 200, 150)

    def draw(self, screen, screen_movement):
        draw_x = self.x - screen_movement

        pygame.draw.rect(screen, self.border_color,
                         (draw_x - 2, self.y - 2, self.width + 4, self.height + 4),
                         border_radius=5)
        pygame.draw.rect(screen, self.color,
                         (draw_x, self.y, self.width, self.height),
                         border_radius=5)

        for i in range(3):
            line_y = self.y + self.height // 4 * (i + 1)
            pygame.draw.line(screen, self.border_color,
                             (draw_x + 5, line_y),
                             (draw_x + self.width - 5, line_y), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class FormBarrier:

    def __init__(self, x, y, width, height, allowed_form):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.allowed_form = allowed_form  # "light" or "shadow"

        if allowed_form == "light":
            self.color = (255, 255, 100, 120)
            self.border_color = YELLOW
        else:
            self.color = (100, 80, 150, 120)
            self.border_color = SHADOW_PURPLE

    def can_pass(self, player_form):
        # returns True if the player can pass
        return player_form == self.allowed_form

    def draw(self, screen, screen_movement):
        draw_x = self.x - screen_movement

        barrier_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        barrier_surface.fill(self.color)
        screen.blit(barrier_surface, (draw_x, self.y))

        # vertical lines
        for i in range(0, self.width, 15):
            pygame.draw.line(screen, self.border_color,
                             (draw_x + i, self.y),
                             (draw_x + i, self.y + self.height), 3)

        # border
        pygame.draw.rect(screen, self.border_color,
                         (draw_x, self.y, self.width, self.height), 3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class ShadowZone:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alpha = 120

    def draw(self, screen, screen_movement):
        draw_x = self.x - screen_movement

        shadow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        shadow_surface.fill((*DARK_BLUE[:3], self.alpha))
        screen.blit(shadow_surface, (draw_x, self.y))

        pygame.draw.rect(screen, PURPLE, (draw_x, self.y, self.width, self.height), 2)

    def contains_player(self, player):
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        return (self.x < player_center_x < self.x + self.width and
                self.y < player_center_y < self.y + self.height)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Hazard:
    # obstacle

    def __init__(self, x, y, size=30, hazard_type="spike"):
        self.x = x
        self.y = y
        self.size = size
        self.hazard_type = hazard_type
        self.color = (180, 50, 50)

    def draw(self, screen, screen_movement):
        draw_x = self.x - screen_movement

        if self.hazard_type == "spike":
            points = [
                (draw_x, self.y + self.size),
                (draw_x + self.size, self.y + self.size),
                (draw_x + self.size // 2, self.y)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (200, 0, 0), points, 2)
        else:
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class MovingPlatform(Platform):

    def __init__(self, x, y, width, height, platform_type, move_type="vertical", move_range=100, speed=2):
        super().__init__(x, y, width, height, platform_type)
        self.start_x = x
        self.start_y = y
        self.move_type = move_type  # "vertical" sau "horizontal"
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1 sau -1

    def update(self):
        # update positon
        if self.move_type == "vertical":
            self.y += self.speed * self.direction
            if self.y > self.start_y + self.move_range or self.y < self.start_y:
                self.direction *= -1
        else:  # horizontal
            self.x += self.speed * self.direction
            if self.x > self.start_x + self.move_range or self.x < self.start_x:
                self.direction *= -1


class MovingPlatform(Platform):

    def __init__(self, x, y, width, height, platform_type, move_type="vertical", move_range=100, speed=2):
        super().__init__(x, y, width, height, platform_type)
        self.start_x = x
        self.start_y = y
        self.move_type = move_type  # "vertical" or "horizontal"
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1 or -1

    def update(self):
        # update position
        if self.move_type == "vertical":
            self.y += self.speed * self.direction
            if self.y > self.start_y + self.move_range or self.y < self.start_y:
                self.direction *= -1
        else:  # horizontal
            self.x += self.speed * self.direction
            if self.x > self.start_x + self.move_range or self.x < self.start_x:
                self.direction *= -1