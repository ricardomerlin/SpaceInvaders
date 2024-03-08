import pygame

class Missle(pygame.sprite.Sprite):
    missles = pygame.sprite.Group()

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('../sprites/missle.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.hit = False
        self.explosion_timer = 0

    def update(self, dt):
        if not self.hit:
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.kill()
        else:
            self.change_sprite('../sprites/missle_explosion.png')
            self.explosion_timer += dt
            if self.explosion_timer >= 0.3:
                self.kill()

    def change_sprite(self, new_image_path):
        new_image = pygame.image.load(new_image_path)
        self.image = pygame.transform.scale(new_image, (80, 60))
        self.rect = self.image.get_rect(center=self.rect.center)

    @classmethod
    def update_all(cls, dt):
        cls.missles.update(dt)

    @classmethod
    def draw_all(cls, screen):
        cls.missles.draw(screen)