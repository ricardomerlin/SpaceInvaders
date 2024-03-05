import pygame

class GameOverScreen:
    def __init__(self, screen_width, screen_height):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render('Game Over', True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(screen_width/2, screen_height/2))

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)