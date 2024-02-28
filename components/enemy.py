# class Enemy(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((50, 50))  # Example image, replace with actual enemy image
#         self.image.fill((255, 0, 0))  # Red color, replace with actual enemy image
#         self.rect = self.image.get_rect()
#         self.rect.center = (500, 200)  # Example initial position, adjust as needed

#         self.enemies = pygame.sprite.Group()

#     def update(self, dt):
#         pass

#     def draw(self, screen):
#         self.enemies.draw(screen)