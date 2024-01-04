import pygame
import os
import math
import sys
import pygame.freetype

# Idea is to make game where plane upgrades after certain amount of time alive. Enemy sprites are shooting at you, 3 at a time. Once all of the enemy sprites are dead, the next wave of sprites loads in. Maybe fades in from the side?


class Plane(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale=1.0):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 500
        self.shoot_timer = 0
        self.health = 10
        self.current_sprite = 0

        self.start_time = pygame.time.get_ticks()
        self.can_shoot = False

    def change_sprite(self, new_image, new_scale):
        all_sprites.remove(self)
        new_plane = Plane(new_image, self.rect.x, self.rect.y, scale=new_scale)
        all_sprites.add(new_plane)
        self.image = pygame.transform.scale(new_image, (int(new_image.get_width() * new_scale), int(new_image.get_height() * new_scale)))
        self.original_image = new_image
        new_plane.can_shoot = self.can_shoot

    def update(self, dt, bullets):
        movement = self.speed * dt

        if self.can_shoot:
            self.shoot_timer += dt
            if self.shoot_timer >= 0.3:
                self.shoot(bullets)
                self.shoot_timer = 0

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

        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000

        if elapsed_seconds == 10 and self.original_image == plane1_image:
            self.change_sprite(plane2_image, 0.6)

        elif elapsed_seconds == 10 and self.original_image == plane2_image:
            self.change_sprite(plane3_image, 0.7)

        bad_bullet_hits = pygame.sprite.spritecollide(self, bad_bullets, True)
        for bullet in bad_bullet_hits:
            self.health -= 10


    def shoot(self, bullets):
        if self.original_image == plane1_image:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
        elif self.original_image == plane2_image:
            bullet1 = Bullet(self.rect.centerx - 20, self.rect.top)
            bullet2 = Bullet(self.rect.centerx + 20, self.rect.top)
            bullets.add(bullet1, bullet2)
        elif self.original_image == plane3_image:
            bullet_1 = Bullet(self.rect.centerx - 40, self.rect.top)
            bullet_2 = Bullet(self.rect.centerx + 40, self.rect.top)
            bullet_3 = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet_1, bullet_2, bullet_3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.speed = 500

    def update(self, dt):
        movement = self.speed * dt
        self.rect.y -= movement
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, scale=1.0):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.speed = 500
        self.shoot_timer = 0
        self.health = 50
        self.rect.x = screen_width/2 - self.image.get_width()/2
        self.rect.y = -300

        self.start_time = pygame.time.get_ticks()

    def shoot_2(self, bad_bullets):
        print("shoot")
        if self.original_image == sprite1_image:
            bad_bullet = Bad_bullet(self.rect.centerx, self.rect.top)
            bad_bullets.add(bad_bullet)
        elif self.original_image == sprite2_image:
            bad_bullet_1 = Bad_bullet(self.rect.centerx - 40, self.rect.top)
            bad_bullet_2 = Bad_bullet(self.rect.centerx + 40, self.rect.top)
            bad_bullets.add(bad_bullet_1, bad_bullet_2)
        elif self.original_image == sprite3_image:
            bad_bullet_1 = Bad_bullet(self.rect.centerx - 40, self.rect.top)
            bad_bullet_2 = Bad_bullet(self.rect.centerx + 40, self.rect.top)
            bad_bullet_3 = Bad_bullet(self.rect.centerx, self.rect.top)
            bad_bullets.add(bad_bullet_1, bad_bullet_2, bad_bullet_3)

    def update(self, dt, bullets):

        self.shoot_timer += dt
        if self.shoot_timer >= 1:
            self.shoot_2(bad_bullets)
            self.shoot_timer = 0

        bullet_hits = pygame.sprite.spritecollide(self, bullets, True)
        for bullet in bullet_hits:
            self.health -= 10
        
        if self.health <= 0 and self.original_image == sprite1_image:
            all_sprites.remove(self)
            new_enemy = Enemy(sprite2_image, scale=1.0)
            all_sprites.add(new_enemy)
            self.image = pygame.transform.scale(sprite2_image, (int(sprite2_image.get_width() * 0.6), int(sprite2_image.get_height() * 0.6)))
            self.original_image = sprite2_image
            self.health = 50

        if self.original_image == sprite2_image and self.health <= 0:
            all_sprites.remove(self)
            new_enemy = Enemy(sprite3_image, scale=1.0)
            all_sprites.add(new_enemy)
            self.image = pygame.transform.scale(sprite3_image, (int(sprite2_image.get_width() * 0.6), int(sprite2_image.get_height() * 0.6)))
            self.original_image = sprite2_image
        
        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000


        movement = 3
        if 0 <= elapsed_seconds <= 1:
            self.rect.y += movement
        if 2 <= elapsed_seconds < 5 or 11 <= elapsed_seconds < 17 or 23 <= elapsed_seconds < 29 or 35 <= elapsed_seconds < 41:
            self.rect.x += movement
        if 5 <= elapsed_seconds < 11 or 17 <= elapsed_seconds < 23 or 29 <= elapsed_seconds < 35 or 39 <= elapsed_seconds < 47:
            self.rect.x -= movement


class Bad_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.speed = 300

    def update(self, dt):
        movement = self.speed * dt
        self.rect.y += movement
        if self.rect.bottom < 0:
            self.kill()



pygame.init()


screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))




sprite1_image = pygame.image.load("sprites/enemy_1.png").convert_alpha()
sprite2_image = pygame.image.load("sprites/enemy_2.png").convert_alpha()
sprite3_image = pygame.image.load("sprites/enemy_3.png").convert_alpha()

plane1_image = pygame.image.load("sprites/plane_1.png").convert_alpha()
plane2_image = pygame.image.load("sprites/plane_2.png").convert_alpha()
plane3_image = pygame.image.load("sprites/plane_3.png").convert_alpha()

plane_1_path = os.path.join(os.path.dirname(__file__), 'sprites/plane_1.png')
plane_1_art = pygame.image.load(plane_1_path).convert_alpha()


bg_img = pygame.image.load('background_image/space.jpg').convert()
bg_img = pygame.transform.scale(bg_img, (1000, 1000))
bg_height = bg_img.get_height()
bg_rect = bg_img.get_rect()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bad_bullets = pygame.sprite.Group()







#define game variables
scroll = 0
tiles = math.ceil(screen_height / bg_height) + 1

clock = pygame.time.Clock()


pygame.font.init()
font = pygame.font.SysFont(None, 36)

title_font = pygame.font.SysFont(None, 72)
title_text = title_font.render("Space Adventure", True, (255, 255, 255))
start_text = font.render("Press SPACE to Start", True, (255, 255, 255))

elapsed_seconds = (pygame.time.get_ticks()) // 1000

title_screen = True
game_running = False

running = True


# def reset():
#     global plane, enemy, elapsed_seconds
#     plane = Plane(plane1_image, 500, 800, scale=0.5)
#     enemy = Enemy(sprite1_image, scale = 0.5)
#     elapsed_seconds = 0

game_started = False
plane = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # pygame.time.delay(2000)
            bullets.empty()
            bad_bullets.empty()
            all_sprites.empty()
            plane = Plane(plane1_image, 500, 800, scale=0.5)
            title_screen = False
            game_running = True
            game_started = True
            seconds_count = 0
            plane.can_shoot = True
            start_time = pygame.time.get_ticks()
            enemy = Enemy(sprite1_image, scale = 0.5)
            all_sprites.add(enemy)
            dt = clock.tick(60) / 1000.0
            all_sprites.add(plane)
            # pygame.time.delay(1000)
            # all_sprites.update(dt, bullets)
            # all_sprites.draw(screen)
            # bullets.update(dt)
            # bullets.draw(screen)


    if title_screen:
        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 400))
        pygame.display.update()
    
    if game_running:
        for i in range(0, tiles):
            screen.blit(bg_img, (0, -i * bg_height + scroll))
        gameover_text = font.render(f'Time:{elapsed_seconds}', True, (240, 248, 255))
        screen.blit(gameover_text, (25, 25))
        scroll += 2

        if abs(scroll) > bg_height:
            scroll = 0

        if plane.health <= 0:
            gameover_text = font.render('Game Over', True, (255, 0, 0))
            screen.blit(gameover_text, (screen_width // 2 - 80, screen_height // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            title_screen = True
            game_running = False
            game_started = False
            # reset()

        dt = clock.tick(60) / 1000.0

        all_sprites.update(dt, bullets)
        all_sprites.draw(screen)
        bullets.update(dt)
        bullets.draw(screen)

        if game_started:  # Only update and draw enemies if the game has started
            bad_bullets.update(dt)
            bad_bullets.draw(screen)

            current_time = pygame.time.get_ticks()
            elapsed_seconds = (current_time - start_time) // 1000

            if elapsed_seconds > seconds_count:
                seconds_count = elapsed_seconds

            for enemy in pygame.sprite.spritecollide(plane, all_sprites, False):
                if isinstance(enemy, Enemy):
                    if enemy.hit(plane):
                        enemy.kill()

        pygame.display.update()

pygame.quit()