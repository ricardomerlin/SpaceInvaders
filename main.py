import pygame
import os
import math
import time

class Plane_1(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale=1.0):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 500
        self.shoot_timer = 0
        self.health = 100

    def update(self, dt, all_sprites, bullets):
        movement = self.speed * dt

        self.shoot_timer += dt
        if self.shoot_timer >= 0.2:
            self.shoot(bullets)
            self.shoot_timer = 0

        # Movement handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.rect.x += movement * 0.75
            self.rect.y -= movement * 0.75
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.rect.x += movement * 0.75
            self.rect.y += movement * 0.75
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.rect.x -= movement * 0.75
            self.rect.y -= movement * 0.75
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.rect.x -= movement * 0.75
            self.rect.y += movement * 0.75
        elif keys[pygame.K_RIGHT]:
            self.rect.x += movement
        elif keys[pygame.K_LEFT]:
            self.rect.x -= movement
        elif keys[pygame.K_UP]:
            self.rect.y -= movement
        elif keys[pygame.K_DOWN]:
            self.rect.y += movement


        self.rect.x = max(0, min(self.rect.x, 1000 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 1000 - self.rect.height))


    def hit(self, player):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        distance = math.sqrt(math.pow(player.x - player.x(), 2) + math.pow(player.y - player.y(), 2))
        if distance < 20:
            return True
        else:
            return False

    def shoot(self, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.speed = 1000

    def update(self, dt):
        movement = self.speed * dt
        self.rect.y -= movement
        if self.rect.bottom < 0:
            self.kill()



class Enemy_1(pygame.sprite.Sprite):

    def __init__(self, image, x, y, scale=1.0):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.speed = 500
        self.shoot_timer = 0
        self.health = 100
        self.rect.x = 350
        self.rect.y = 0


# class Enemy_2(pygame.sprite.Sprite):
#     pass

# class Enemy_3(pygame.sprite.Sprite):
#     pass

# class Enemy_1(pygame.sprite.Sprite):
#     pass

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

plane_1_path = os.path.join(os.path.dirname(__file__), 'sprites/plane_1.png')
plane_1_art = pygame.image.load(plane_1_path).convert_alpha()

enemy_1_path = os.path.join(os.path.dirname(__file__), 'sprites/enemy_1.png')
enemy_1_art = pygame.image.load(enemy_1_path).convert_alpha()







bg_img = pygame.image.load('background_image/Space_pic.jpg')
bg_img = pygame.transform.scale(bg_img, (1000, 1000))

plane_1 = Plane_1(plane_1_art, 500, 800, scale = 0.5)
enemy_1 = Enemy_1(enemy_1_art, 500, 800, scale = 0.5)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(plane_1)
all_sprites.add(enemy_1)

clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000.0

    screen.blit(bg_img, (0, 0))

    all_sprites.update(dt, all_sprites, bullets)
    all_sprites.draw(screen)

    bullets.update(dt)
    bullets.draw(screen)

    pygame.display.flip()

pygame.quit()
