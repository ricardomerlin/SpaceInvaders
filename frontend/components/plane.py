import pygame
from bullet import Bullet
from badBullet import BadBullet
from missles import Missle
from monsterGoo import MonsterGoo

class Plane(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast, plane_1_hit, plane_2_hit, plane_3_hit):
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

        self.plane_1_hit = plane_1_hit
        self.plane_2_hit = plane_2_hit
        self.plane_3_hit = plane_3_hit

        self.image = self.plane_1_standard
        original_width, original_height = self.image.get_size()
        new_width = int(original_width * 0.4)
        new_height = int(original_height * 0.4)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 300
        self.can_shoot = True
        self.shoot_timer = 0
        self.shoot_missle_timer = 0
        self.original_image = None
        self.planes = pygame.sprite.Group()
        self.health = 1000
        self.max_health = 1000
        self.start_time = 0

        self.hit_duration = 0.2
        self.hit_timer = 0
        self.is_hit = False

        self.hit_tracker = 0


    def start_game(self):
        self.game_running = True
        self.start_time = pygame.time.get_ticks()
        self.elapsed_seconds = 0

    # def draw_hitbox(self, screen):
    #     pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def update(self, dt, elapsed_seconds):
        movement = self.speed * dt 

        self.elapsed_seconds = elapsed_seconds

        if self.is_hit:
            self.hit_timer += dt
            if self.hit_timer < self.hit_duration:
                hit_plane = None
                if self.original_image == self.plane_1_standard or self.original_image == self.plane_1_fast or self.original_image == self.plane_1_slow:
                    hit_plane = self.plane_1_hit
                elif self.original_image == self.plane_2_standard or self.original_image == self.plane_2_fast or self.original_image == self.plane_2_slow:
                    hit_plane = self.plane_2_hit
                elif self.original_image == self.plane_3_standard or self.original_image == self.plane_3_fast or self.original_image == self.plane_3_slow:
                    hit_plane = self.plane_3_hit
                self.update_hit_sprite(hit_plane)
            else:
                self.is_hit = False
                return_to_normal = None
                if self.original_image == self.plane_1_standard or self.original_image == self.plane_1_fast or self.original_image == self.plane_1_slow:
                    return_to_normal = self.plane_1_standard
                elif self.original_image == self.plane_2_standard or self.original_image == self.plane_2_fast or self.original_image == self.plane_2_slow:
                    return_to_normal = self.plane_2_standard
                elif self.original_image == self.plane_3_standard or self.original_image == self.plane_3_fast or self.original_image == self.plane_3_slow:
                    return_to_normal = self.plane_3_standard
                self.update_hit_sprite(return_to_normal)
                self.hit_timer = 0

        if self.can_shoot:
            if self.original_image == self.plane_1_standard or self.original_image == self.plane_1_fast or self.original_image == self.plane_1_slow:
                self.shoot_timer += dt
                self.shoot_missle_timer += dt
                if self.shoot_timer >= 0.4:
                    self.shoot()
                    self.shoot_timer = 0
                if self.shoot_missle_timer >= 5:
                    self.shootMissles()
                    self.shoot_missle_timer = 0
            if self.original_image == self.plane_2_standard or self.original_image == self.plane_2_fast or self.original_image == self.plane_2_slow:
                self.shoot_timer += dt
                self.shoot_missle_timer += dt
                if self.shoot_timer >= 0.3:
                    self.shoot()
                    self.shoot_timer = 0
                if self.shoot_missle_timer >= 3:
                    self.shootMissles()
                    self.shoot_missle_timer = 0
            if self.original_image == self.plane_3_standard or self.original_image == self.plane_3_fast or self.original_image == self.plane_3_slow:
                self.shoot_timer += dt
                self.shoot_missle_timer += dt
                if self.shoot_timer >= 0.2:
                    self.shoot()
                    self.shoot_timer = 0
                if self.shoot_missle_timer >= 1:
                    self.shootMissles()
                    self.shoot_missle_timer = 0

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= movement
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += movement

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        if self.elapsed_seconds < 20:
            if dy < 0:
                new_sprite = self.plane_1_fast
            elif dy > 0:
                new_sprite = self.plane_1_slow
            else:
                new_sprite = self.plane_1_standard
        elif 15 <= self.elapsed_seconds < 40:
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

        bad_bullet_hits = pygame.sprite.spritecollide(self, self.bad_bullets, True)
        enemy_goo_hits = pygame.sprite.spritecollide(self, MonsterGoo.goos, False)
        for bullet in bad_bullet_hits:
            self.health -= 10
            self.hit_tracker += 5
            self.is_hit = True
        for goo in enemy_goo_hits:
            if not goo.has_hit_plane:
                self.hit_tracker += 7
                goo.plane_hit = True
                goo.has_hit_plane = True
                self.health -= 30
                self.is_hit = True

    def change_sprite(self, new_image, new_scale):
        old_center = self.rect.center
        self.planes.remove(self)
        scaled_image = pygame.transform.scale(
            new_image,
            (
                int(new_image.get_width() * new_scale),
                int(new_image.get_height() * new_scale),
            ),
        )
        self.image = scaled_image
        self.original_image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.planes.add(self)


    def update_hit_sprite(self, new_image_path):
        original_width, original_height = new_image_path.get_size()
        aspect_ratio = original_width / original_height

        new_width = int(self.rect.height * aspect_ratio)
        new_height = int(self.rect.height)

        scaled_image = pygame.transform.scale(new_image_path, (new_width, new_height))
        self.image = scaled_image
        

    def healthbar(self, window):
        health_bar_width = 600
        health_bar_height = 10
        health_bar_x = (self.screen.get_width() - health_bar_width) // 2
        health_bar_y = 20
        
        health_percentage = max(0, min(self.health / self.max_health, 1))
        
        pygame.draw.rect(window, (50, 50, 50), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        bar_color = (0, 255, 0)
        if health_percentage < 0.5:
            bar_color = (255, 255, 0)
        if health_percentage < 0.2:
            bar_color = (255, 0, 0)
        filled_width = int(health_percentage * health_bar_width)
        pygame.draw.rect(window, bar_color, (health_bar_x, health_bar_y, filled_width, health_bar_height))
        
        font = pygame.font.Font(None, 20)
        text = font.render('Plane Health', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, health_bar_y + health_bar_height - 20))
        window.blit(text, text_rect)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.original_image in [self.plane_1_standard, self.plane_1_fast, self.plane_1_slow]:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            Bullet.bullets.add(bullet)
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

    def shootMissles(self):
        missle = Missle(self.rect.centerx, self.rect.top)
        Missle.missles.add(missle)

    def hit_enemy(self):
        hit = pygame.sprite.spritecollide(self, self.enemies, True)
        if hit:
            self.enemies.health -= 10
            return True