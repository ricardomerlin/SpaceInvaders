import pygame

class MonsterGoo(pygame.sprite.Sprite):
    goos = pygame.sprite.Group()

    def __init__(self, x, y, screen_height):
        super().__init__()
        self.image = pygame.image.load('../sprites/enemy_goo.png')
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.screen_height = screen_height
        self.explosion_timer = 0
        self.plane_hit = False
        self.has_hit_plane = False

    def update(self, dt):
        if not self.plane_hit:
            self.rect.y += self.speed
            if self.rect.top > self.screen_height:
                self.kill()
        else:
            self.change_sprite('../sprites/enemy_goo_explosion.png')
            self.explosion_timer += dt
            if self.explosion_timer >= 0.3:
                self.kill()

    def change_sprite(self, new_image_path):
        new_image = pygame.image.load(new_image_path)
        self.image = pygame.transform.scale(new_image, (80, 60))
        self.rect = self.image.get_rect(center=self.rect.center)

    @classmethod
    def update_all(cls, dt):
        cls.goos.update(dt)

    @classmethod
    def draw_all(cls, screen):
        cls.goos.draw(screen)