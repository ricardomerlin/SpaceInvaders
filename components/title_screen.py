import pygame

class TitleScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define fonts
        self.title_font = pygame.font.SysFont(None, 100)
        self.start_font = pygame.font.SysFont(None, 50)

        # Render text
        self.title_text = self.title_font.render("Space Adventure", True, (255, 255, 255))
        self.start_text = self.start_font.render("Press SPACE to Start", True, (255, 255, 255))

        # Get text rect for centering
        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.start_rect = self.start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        # Color transition variables
        self.color_timer = 0
        self.color_speed = 5

    def update(self, screen):
        # Apply color transition to the title text
        color_value = (255, 255 - self.color_timer, 255 - self.color_timer)
        self.title_text = self.title_font.render("Space Adventure", True, color_value)

        # Blit everything to the screen
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)

        # Update color transition timer
        self.color_timer = (self.color_timer + self.color_speed) % 256

    def start_game(self):
        pass
