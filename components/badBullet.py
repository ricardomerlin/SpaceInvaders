import pygame

class BadBullet(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()

    def __init__(self, x, y, screen_height):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6
        self.screen_height = screen_height

    def update(self, dt):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()

    @classmethod
    def update_all(cls, dt):
        cls.bullets.update(dt)

    @classmethod
    def draw_all(cls, screen):
        cls.bullets.draw(screen)

