import pygame

class TitleScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 72)
        self.title_text = self.font.render("Space Adventure", True, (255, 255, 255))
        self.start_text = self.font.render("Press SPACE to Start", True, (255, 255, 255))

    def update(self, screen):
        screen.blit(self.title_text, (250, 200))
        screen.blit(self.start_text, (300, 400))

    def start_game(self):
        pass
