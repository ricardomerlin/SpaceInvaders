import pygame
import os
import math
import sys
import pygame.freetype


class Plane(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale=0.3):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 500
        self.shoot_timer = 0
        self.health = 100
        self.max_health = 100

        self.start_time = pygame.time.get_ticks()
        self.can_shoot = False

    def change_sprite(self, new_image, new_scale):
        global plane
        all_sprites.remove(self)
        plane = Plane(new_image, self.rect.x, self.rect.y, scale=new_scale)
        all_sprites.add(plane)
        self.image = pygame.transform.scale(
            new_image,
            (
                int(new_image.get_width() * new_scale),
                int(new_image.get_height() * new_scale),
            ),
        )
        self.original_image = new_image
        plane.can_shoot = self.can_shoot

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

        if elapsed_seconds == 15 and self.original_image == plane1_image:
            self.change_sprite(plane2_image, 0.4)

        elif elapsed_seconds == 15 and self.original_image == plane2_image:
            self.change_sprite(plane3_image, 0.5)

        if (
            self.original_image == plane1_image
            or self.original_image == plane2_image
            or self.original_image == plane3_image
        ):
            self.healthbar(screen)
            bad_bullet_hits = pygame.sprite.spritecollide(self, bad_bullets, True)
            for bullet in bad_bullet_hits:
                self.health -= 10

        bad_bullet_hits = pygame.sprite.spritecollide(self, bad_bullets, True)
        for bullet in bad_bullet_hits:
            self.health -= 10

    def healthbar(self, window):
        health_bar_width = 10
        health_bar_height = 100
        health_bar_x = self.rect.x - health_bar_width - 5
        health_bar_y = self.rect.y - 5

        pygame.draw.rect(
            window,
            (255, 0, 0),
            (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                health_bar_x,
                health_bar_y + (1 - self.health / self.max_health) * health_bar_height,
                health_bar_width,
                (self.health / self.max_health) * health_bar_height,
            ),
        )
        print(f"healthbar health {self.health}")

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
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.speed = 500
        self.shoot_timer = 0
        self.health = 100
        self.rect.x = screen_width / 2 - self.image.get_width() / 2
        self.rect.y = -300

        self.start_time = pygame.time.get_ticks()

    def shoot_2(self, bad_bullets):
        if self.original_image == sprite1_image:
            bad_bullet = Bad_bullet(self.rect.centerx, self.rect.top + 100)
            bad_bullets.add(bad_bullet)
        elif self.original_image == sprite2_image:
            self.speed = 800
            bad_bullet_1 = Bad_bullet(self.rect.centerx - 120, self.rect.top + 170)
            bad_bullet_2 = Bad_bullet(self.rect.centerx - 100, self.rect.top + 170)
            bad_bullet_3 = Bad_bullet(self.rect.centerx + 120, self.rect.top + 170)
            bad_bullet_4 = Bad_bullet(self.rect.centerx + 100, self.rect.top + 170)
            bad_bullet_1.speed = 800
            bad_bullet_2.speed = 800
            bad_bullet_3.speed = 800
            bad_bullet_4.speed = 800
            bad_bullets.add(bad_bullet_1, bad_bullet_2, bad_bullet_3, bad_bullet_4)

        elif self.original_image == sprite3_image:
            self.speed = 1500
            bad_bullet_1 = Bad_bullet(self.rect.centerx - 120, self.rect.top + 240)
            bad_bullet_2 = Bad_bullet(self.rect.centerx + 120, self.rect.top + 240)
            # maybe add missle?
            bad_bullet_1.speed = 1500
            bad_bullet_2.speed = 1500
            bad_bullets.add(bad_bullet_1, bad_bullet_2)

        if self.original_image == sprite3_image and self.health <= 0:
            title_screen = True

    def hit(self, player):
        return self.rect.colliderect(player.rect)

    def update(self, dt, bullets):
        self.shoot_timer += dt
        if self.shoot_timer >= 1:
            self.shoot_2(bad_bullets)
            self.shoot_timer = 0

        bullet_hits = pygame.sprite.spritecollide(self, bullets, True)
        for bullet in bullet_hits:
            self.health -= 10

        if self.health <= 0 and self.original_image == sprite1_image:
            global enemy
            all_sprites.remove(self)
            enemy = Enemy(sprite2_image, scale=0.7)
            enemy.health = 200
            all_sprites.add(enemy)
            self.image = pygame.transform.scale(
                sprite2_image,
                (
                    int(sprite2_image.get_width() * 0.6),
                    int(sprite2_image.get_height() * 0.6),
                ),
            )
            self.original_image = sprite2_image
            self.health = 300

        if self.original_image == sprite2_image and self.health <= 0:
            all_sprites.remove(self)
            enemy = Enemy(sprite3_image, scale=0.8)
            enemy.health = 300
            all_sprites.add(enemy)
            self.image = pygame.transform.scale(
                sprite3_image,
                (
                    int(sprite3_image.get_width() * 0.6),
                    int(sprite3_image.get_height() * 0.6),
                ),
            )
            self.original_image = sprite3_image
            self.health = 100

        elapsed_seconds = (pygame.time.get_ticks() - self.start_time)//1000

        if self.original_image == sprite1_image:
            movement = 2.8
            if 0 <= elapsed_seconds <= 1:
                self.rect.y += movement
            if (
                2 <= elapsed_seconds < 4
                or 8 <= elapsed_seconds < 12
                or 16 <= elapsed_seconds < 20
                or 24 <= elapsed_seconds < 28
                or 32 <= elapsed_seconds < 36
                or 40 <= elapsed_seconds < 44
            ):
                self.rect.x += movement
            if (
                4 <= elapsed_seconds < 8
                or 12 <= elapsed_seconds < 16
                or 20 <= elapsed_seconds < 24
                or 28 <= elapsed_seconds < 32
                or 36 <= elapsed_seconds < 40
            ):
                self.rect.x -= movement

        if self.original_image == sprite2_image:
            print(self.health)
            movement = 5
            if 0 <= elapsed_seconds <= 0.6:
                self.rect.y += movement
            elif 0.6 < elapsed_seconds <= 1.6:  # Move right
                self.rect.x += movement
            elif 1.6 < elapsed_seconds <= 2.6:  # Move down
                self.rect.y += movement
            elif 2.6 < elapsed_seconds <= 4.6:  # Move left
                self.rect.x -= movement
            elif 3.6 < elapsed_seconds <= 5.6:  # Move up
                self.rect.y -= movement
            elif 5.6 < elapsed_seconds <= 7.6:  # Move right
                self.rect.x += movement
            elif 7.6 < elapsed_seconds <= 8.6:  # Move down
                self.rect.y += movement
            elif 8.6 < elapsed_seconds <= 10.6:  # Move left
                self.rect.x -= movement
            elif 10.6 < elapsed_seconds <= 11.6:  # Move up
                self.rect.y -= movement
            elif 11.6 < elapsed_seconds <= 12.6:  # Move right
                self.rect.x += movement
            elif 12.6 < elapsed_seconds <= 13.6:  # Move down
                self.rect.y += movement
            elif 13.6 < elapsed_seconds <= 14.6:  # Move left
                self.rect.x -= movement
            elif 14.6 < elapsed_seconds <= 15.6:  # Move up
                self.rect.y -= movement
            elif 15.6 < elapsed_seconds <= 17.6:  # Move right
                self.rect.x += movement
            elif 17.6 < elapsed_seconds <= 18.6:  # Move down
                self.rect.y += movement
            elif 18.6 < elapsed_seconds <= 20.6:  # Move left
                self.rect.x -= movement
            elif 20.6 < elapsed_seconds <= 21.6:  # Move up
                self.rect.y -= movement
            elif 21.6 < elapsed_seconds <= 23.6:  # Move left
                self.rect.x -= movement
            elif 23.6 < elapsed_seconds <= 24.6:  # Move up
                self.rect.y -= movement
            elif 24.6 < elapsed_seconds <= 26.6:  # Move right
                self.rect.x += movement
            elif 26.6 < elapsed_seconds <= 27.6:  # Move down
                self.rect.y += movement
            elif 27.6 < elapsed_seconds <= 29.6:  # Move left
                self.rect.x -= movement
            elif 29.6 < elapsed_seconds <= 30.6:  # Move up
                self.rect.y -= movement
            

        elif self.original_image == sprite3_image:
            movement = 4
            if 0 <= elapsed_seconds <= 1:
                self.rect.y += movement
            elif 1 < elapsed_seconds <= 3:
                self.rect.x += 3
                self.rect.y -= 2
            elif 3 < elapsed_seconds <= 4:  # Move down
                self.rect.y += 10
            elif 4 < elapsed_seconds <= 8:  # Move right-down
                self.rect.x -= 3
                self.rect.y -= 2.5
            elif 8 < elapsed_seconds <= 9:  # Move down
                self.rect.y += 8
            elif 9 < elapsed_seconds <= 11:  # Move left-down
                self.rect.x += 3
                self.rect.y -= 2.5
            elif 11 < elapsed_seconds <= 12:  # Move up
                self.rect.y -= 8
            elif 12 < elapsed_seconds <= 16:  # Move right-down
                self.rect.x += 2
                self.rect.y += 2
            elif 16 < elapsed_seconds <= 17:  # Move down
                self.rect.y += 8
            elif 17 < elapsed_seconds <= 22:  # Move left-up
                self.rect.x -= 3
                self.rect.y -= 3
            elif 22 < elapsed_seconds <= 24:
                self.rect.x += 6.5
            elif 24 < elapsed_seconds <= 25:  # Move down
                self.rect.y += 10
            elif 25 < elapsed_seconds <= 29:  # Move right-down
                self.rect.x -= 3
                self.rect.y -= 2.5
            elif 29 < elapsed_seconds <= 30:  # Move down
                self.rect.y += 8
            elif 30 < elapsed_seconds <= 32:  # Move left-down
                self.rect.x += 3
                self.rect.y -= 2.5
            elif 32 < elapsed_seconds <= 33:  # Move up
                self.rect.y -= 8
            elif 33 < elapsed_seconds <= 37:  # Move right-down
                self.rect.x += 2
                self.rect.y += 2
            elif 37 < elapsed_seconds <= 38:  # Move down
                self.rect.y += 8
            elif 38 < elapsed_seconds <= 43:  # Move left-up
                self.rect.x -= 3
                self.rect.y -= 3
            elif 43 < elapsed_seconds <= 45:
                self.rect.x += 6.5
            elif 45 < elapsed_seconds <= 46:  # Move down
                self.rect.y += 10
                self.rect.x += 1
            elif 46 < elapsed_seconds <= 50:  # Move right-down
                self.rect.x -= 3
                self.rect.y -= 2.5
            elif 50 < elapsed_seconds <= 51:  # Move down
                self.rect.y += 8
            elif 51 < elapsed_seconds <= 53:  # Move left-down
                self.rect.x += 3
                self.rect.y -= 2.5
            elif 53 < elapsed_seconds <= 54:  # Move up
                self.rect.y -= 8
            elif 54 < elapsed_seconds <= 58:  # Move right-down
                self.rect.x += 2
                self.rect.y += 2
            elif 58 < elapsed_seconds <= 59:  # Move down
                self.rect.y += 8
            elif 59 < elapsed_seconds <= 64:  # Move left-up
                self.rect.x -= 3
                self.rect.y -= 3
            elif 64 < elapsed_seconds <= 66:
                self.rect.x += 6.5
            elif 66 < elapsed_seconds <= 67:  # Move down
                self.rect.y += 10
            elif 67 < elapsed_seconds <= 71:  # Move right-down
                self.rect.x -= 3
                self.rect.y -= 2.5
            elif 71 < elapsed_seconds <= 72:  # Move down
                self.rect.y += 8
            elif 72 < elapsed_seconds <= 74:  # Move left-down
                self.rect.x += 3
                self.rect.y -= 2.5
            elif 74 < elapsed_seconds <= 75:  # Move up
                self.rect.y -= 8
            elif 75 < elapsed_seconds <= 79:  # Move right-down
                self.rect.x += 2
                self.rect.y += 2
            elif 79 < elapsed_seconds <= 80:  # Move down
                self.rect.y += 8
            elif 80 < elapsed_seconds <= 85:  # Move left-up
                self.rect.x -= 3
                self.rect.y -= 3
            elif 85 < elapsed_seconds <= 87:
                self.rect.x += 6.5



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

plane_1_path = os.path.join(os.path.dirname(__file__), "sprites/plane_1.png")
plane_1_art = pygame.image.load(plane_1_path).convert_alpha()


bg_img = pygame.image.load("background_image/space.jpg").convert()
bg_img = pygame.transform.scale(bg_img, (1000, 1000))
bg_height = bg_img.get_height()
bg_rect = bg_img.get_rect()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bad_bullets = pygame.sprite.Group()


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

game_started = False
plane = None
enemy = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.time.delay(1000)
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
            enemy = Enemy(sprite1_image, scale=0.5)
            all_sprites.add(enemy)
            dt = clock.tick(60) / 1000.0
            all_sprites.add(plane)
            assert isinstance(enemy, Enemy)

    if title_screen:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 400))
        pygame.display.update()

    if game_running:
        for i in range(0, tiles):
            screen.blit(bg_img, (0, -i * bg_height + scroll))
        time_text = font.render(f"Time:{elapsed_seconds}", True, (240, 248, 255))
        screen.blit(time_text, (25, 25))
        scroll += 2

        if abs(scroll) > bg_height:
            scroll = 0

        dt = clock.tick(60) / 1000.0

        all_sprites.update(dt, bullets)
        all_sprites.draw(screen)
        bullets.update(dt)
        bullets.draw(screen)

        if game_started:
            assert isinstance(plane, Plane)
            bad_bullets.update(dt)
            bad_bullets.draw(screen)

            current_time = pygame.time.get_ticks()
            elapsed_seconds = (current_time - start_time) // 1000

            if elapsed_seconds > seconds_count:
                seconds_count = elapsed_seconds
            assert isinstance(enemy, Enemy)
            print(plane.health)
            if plane.health <= 0:
                gameover_text = font.render("Game Over, You Suck", True, (255, 0, 0))
                screen.blit(gameover_text, (screen_width // 2 - 80, screen_height // 2))
                pygame.display.update()
                pygame.time.delay(4000)
                title_screen = True
                game_running = False
                game_started = False
                # reset()

            if enemy.original_image == sprite3_image and enemy.health <= 0:
                screen.fill((0, 0, 0))
                youwin_text = font.render("You Win!", True, (255, 0, 0))
                screen.blit(youwin_text, (screen_width // 2 - 80, screen_height // 2))
                pygame.display.update()
                pygame.time.delay(4000)
                title_screen = True
                game_running = False
                game_started = False

            # if enemy.original_image == sprite3_image and elapsed_seconds == 5:
            #     screen.fill((0, 0, 0))
            #     timeexpired_text = font.render("Took too long! You lose, be better.", True, (255, 0, 0))
            #     screen.blit(timeexpired_text, (screen_width // 2 - 80, screen_height // 2))
            #     pygame.display.update()
            #     pygame.time.delay(5000)
            #     title_screen = True
            #     game_running = False
            #     game_started = False


        pygame.display.update()

pygame.quit()
