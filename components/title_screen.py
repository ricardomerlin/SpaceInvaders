import pygame

class TitleScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont(None, 100)
        self.start_font = pygame.font.SysFont(None, 50)
        self.blurb_font = pygame.font.SysFont(None, 30)

        self.title_text = self.title_font.render("Space Invaders", True, (255, 255, 255))
        self.start_text = self.start_font.render("Press SPACE to Start", True, (255, 255, 255))

        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.start_rect = self.start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 200))

        self.color_timer = 0
        self.color_speed = 5

        self.blurb_text = self.blurb_font.render("Welcome to Space Invaders! Destroy all enemy waves before your ship runs out of health.", True, (255, 255, 255))
        self.blurb_rect = self.blurb_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.blurd_text_2 = self.blurb_font.render("Your ship will upgrade every 20 seconds, good luck!", True, (255, 255, 255))
        self.blurb_rect_2 = self.blurd_text_2.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))

    def update(self, screen):
        color_value = (255, 255 - self.color_timer, 255 - self.color_timer)
        self.title_text = self.title_font.render("Space Invaders", True, color_value)

        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        screen.blit(self.blurb_text, self.blurb_rect)
        screen.blit(self.blurd_text_2, self.blurb_rect_2)

        self.color_timer = (self.color_timer + self.color_speed) % 256

    def start_game(self):
        pass
