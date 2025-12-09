import pygame
import sys
import os

# add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# screen settings
WIDTH = 1000
HEIGHT = 800
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
BLUE = (70, 130, 255)
DARK_BLUE = (50, 100, 200)
GREEN = (100, 200, 100)
DARK_GREEN = (70, 150, 70)

class Button:
	def __init__(self, x, y, width, height, text, color):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.color = color
		
	def draw(self, window):
		# draw button with shadow effect
		shadow_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width, self.rect.height)
		pygame.draw.rect(window, GRAY, shadow_rect, border_radius=10)
		
		# draw main button
		pygame.draw.rect(window, self.color, self.rect, border_radius=10)
		pygame.draw.rect(window, BLACK, self.rect, 3, border_radius=10)
		
		# draw text
		font = pygame.font.Font(None, 48)
		text_surface = font.render(self.text, True, WHITE)
		text_rect = text_surface.get_rect(center=self.rect.center)
		window.blit(text_surface, text_rect)
		
	def is_clicked(self, mouse_pos, mouse_click):
		return self.rect.collidepoint(mouse_pos) and mouse_click

class MainMenu:
	def __init__(self):
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Pixel Jumpers")
		self.clock = pygame.time.Clock()
		
		# create buttons
		button_width = 300
		button_height = 80
		button_x = WIDTH // 2 - button_width // 2
		
		self.play_button = Button(
			button_x, 300, button_width, button_height,
			"PLAY", BLUE
		)
		
		self.editor_button = Button(
			button_x, 420, button_width, button_height,
			"LEVEL EDITOR", GREEN
		)
		
		self.quit_button = Button(
			button_x, 540, button_width, button_height,
			"QUIT", GRAY
		)
		
	def draw_title(self):
		font_large = pygame.font.Font(None, 120)
		title_text = font_large.render("PIXEL JUMPERS", True, BLACK)
		title_rect = title_text.get_rect(center=(WIDTH // 2 + 4, 120 + 4))
		self.window.blit(title_text, title_rect)
		
		title_text_main = font_large.render("PIXEL JUMPERS", True, BLUE)
		title_rect_main = title_text_main.get_rect(center=(WIDTH // 2, 120))
		self.window.blit(title_text_main, title_rect_main)
		
	def run(self):
		running = True
		
		while running:
			self.clock.tick(FPS)
			mouse_pos = pygame.mouse.get_pos()
			mouse_click = False
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					sys.exit()
					
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_click = True
				
			# Check button clicks
			if self.play_button.is_clicked(mouse_pos, mouse_click):
				self.start_game()			
			if self.editor_button.is_clicked(mouse_pos, mouse_click):
				self.start_editor()
				
			if self.quit_button.is_clicked(mouse_pos, mouse_click):
				running = False
				pygame.quit()
				sys.exit()
			
			# draw everything
			self.window.fill(WHITE)
			self.draw_title()
			self.play_button.draw(self.window)
			self.editor_button.draw(self.window)
			self.quit_button.draw(self.window)
			
			pygame.display.flip()
			
	def start_game(self):
		# close menu and start main game
		import game
		game.main(game.window)
		# when game ends, return to menu
		self.__init__()
		self.run()
		
	def start_editor(self):
		# close menu and start level editor
		import level_editor
		level_editor.main()
		# when editor closes, return to menu
		self.__init__()
		self.run()

if __name__ == "__main__":
	menu = MainMenu()
	menu.run()
