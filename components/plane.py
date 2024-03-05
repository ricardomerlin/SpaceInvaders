import pygame
from bullet import Bullet
from badBullet import BadBullet

class Plane(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast):
        super().__init__()
        self.screen = screen
        self.bad_bullets = BadBullet.bullets

        self.plane_1_standard = plane_1_standard
        self.plane_1_slow = plane_1_slow
        self.plane_1_fast = plane_1_fast

        self.plane_2_standard = plane_2_standard
        self.plane_2_slow = plane_2_slow
        self.plane_2_fast = plane_2_fast

        self.plane_3_standard = plane_3_standard
        self.plane_3_slow = plane_3_slow
        self.plane_3_fast = plane_3_fast

        self.image = self.plane_1_standard
        original_width, original_height = self.image.get_size()
        new_width = int(original_width * 0.4)
        new_height = int(original_height * 0.4)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 300
        self.can_shoot = False
        self.shoot_timer = 0
        self.original_image = None
        self.planes = pygame.sprite.Group()
        self.health = 1000
        self.max_health = 100
        self.start_time = 0


    def start_game(self):
        self.game_running = True
        self.start_time = pygame.time.get_ticks()
        self.elapsed_seconds = 0

    def update(self, dt, elapsed_seconds):
        movement = self.speed * dt 

        self.elapsed_seconds = elapsed_seconds

        if self.can_shoot:
            if self.original_image == self.plane_1_standard or self.original_image == self.plane_1_fast or self.original_image == self.plane_1_slow:
                self.shoot_timer += dt
                if self.shoot_timer >= 0.3:
                    self.shoot()
                    self.shoot_timer = 0
            if self.original_image == self.plane_2_standard or self.original_image == self.plane_2_fast or self.original_image == self.plane_2_slow:
                self.shoot_timer += dt
                if self.shoot_timer >= 0.2:
                    self.shoot()
                    self.shoot_timer = 0
            if self.original_image == self.plane_3_standard or self.original_image == self.plane_3_fast or self.original_image == self.plane_3_slow:
                self.shoot_timer += dt
                if self.shoot_timer >= 0.1:
                    self.shoot()
                    self.shoot_timer = 0

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_RIGHT]:
            dx += movement
        if keys[pygame.K_LEFT]:
            dx -= movement
        if keys[pygame.K_UP]:
            dy -= movement
        if keys[pygame.K_DOWN]:
            dy += movement

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        if self.elapsed_seconds < 15:
            if dy < 0:
                new_sprite = self.plane_1_fast
            elif dy > 0:
                new_sprite = self.plane_1_slow
            else:
                new_sprite = self.plane_1_standard
        elif 15 <= self.elapsed_seconds < 30:
            if dy < 0:
                new_sprite = self.plane_2_fast
            elif dy > 0:
                new_sprite = self.plane_2_slow
            else:
                new_sprite = self.plane_2_standard
        else:
            if dy < 0:
                new_sprite = self.plane_3_fast
            elif dy > 0:
                new_sprite = self.plane_3_slow
            else:
                new_sprite = self.plane_3_standard

        if new_sprite != self.original_image:
            self.change_sprite(new_sprite, 0.4)

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, 1000 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 1000 - self.rect.height))

        if (
            self.original_image == self.plane_1_standard
            or self.original_image == self.plane_2_standard
            or self.original_image == self.plane_3_standard
        ):
            self.healthbar(self.screen)
            bad_bullet_hits = pygame.sprite.spritecollide(self, self.bad_bullets, True)
            for bullet in bad_bullet_hits:
                print('Hit')
                self.health -= 10

        bad_bullet_hits = pygame.sprite.spritecollide(self, self.bad_bullets, True)
        for bullet in bad_bullet_hits:
            self.health -= 10

    def change_sprite(self, new_image, new_scale):
        self.planes.remove(self)
        self.image = pygame.transform.scale(
            new_image,
            (
                int(new_image.get_width() * new_scale),
                int(new_image.get_height() * new_scale),
            ),
        )
        self.original_image = new_image
        self.planes.add(self)

    def healthbar(self, window):
        bg_rect_width = 120
        bg_rect_height = 20
        bg_rect_x = 10
        bg_rect_y = 10
        pygame.draw.rect(window, (50, 50, 50), (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height))

        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = bg_rect_x + 5
        health_bar_y = bg_rect_y + 5
        pygame.draw.rect(window, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        if self.health > 70:
            color = (0, 255, 0)
        elif self.health > 30:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(window, color, (health_bar_x, health_bar_y, (self.health / self.max_health) * health_bar_width, health_bar_height))

        font = pygame.font.Font(None, 20)
        text = font.render(f'Health: {self.health}/100', True, (255, 255, 255))
        window.blit(text, (bg_rect_x + bg_rect_width + 10, bg_rect_y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.original_image in [self.plane_1_standard, self.plane_1_fast, self.plane_1_slow]:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            Bullet.bullets.add(bullet)
            print(Bullet.bullets)
        elif self.original_image in [self.plane_2_standard, self.plane_2_fast, self.plane_2_slow]:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            Bullet.bullets.add(bullet1)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            Bullet.bullets.add(bullet2)
        elif self.original_image in [self.plane_3_standard, self.plane_3_fast, self.plane_3_slow]:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            Bullet.bullets.add(bullet1)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            Bullet.bullets.add(bullet2)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery)
            Bullet.bullets.add(bullet3)

    def hit_enemy(self):
        hit = pygame.sprite.spritecollide(self, self.enemies, True)
        if hit:
            self.enemies.health -= 10
            return True