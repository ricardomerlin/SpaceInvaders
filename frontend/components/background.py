import pygame

class Background:
    def __init__(self, image_path, screen_width, screen_height):
        self.bg_img = pygame.image.load(image_path)
        self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        self.scroll = 0

    def update(self, dt, game_running):
        if game_running:
            self.scroll -= 2
            if self.scroll < -self.bg_img.get_height():
                self.scroll = 0

    def draw(self, screen):
        screen.blit(self.bg_img, (0, -self.scroll))
        screen.blit(self.bg_img, (0, -self.scroll - self.bg_img.get_height()))