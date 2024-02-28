import pygame

class Bullet(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5  # Placeholder bullet d

    def update(self, dt):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    @classmethod
    def update_all(cls, dt):
        cls.bullets.update(dt)

    @classmethod
    def draw_all(cls, screen):
        cls.bullets.draw(screen)
