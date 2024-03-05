import pygame
import math
from bullet import Bullet
from badBullet import BadBullet

class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, movement_type, screen_height):
        super().__init__()
        self.image = pygame.image.load('../sprites/enemy_1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, -self.rect.height)
        self.speed = speed
        self.start_time = pygame.time.get_ticks()
        self.initial_x = x
        self.initial_y = y
        self.amplitude = 100
        self.frequency = 2.5
        self.phase = 0
        self.movement_type = movement_type
        self.entry_speed = 1
        self.entry_duration = 2
        self.entry_complete = False
        self.health = 100
        self.hit_time = None
        self.killed = False
        self.screen_height = screen_height

        self.can_shoot = True
        self.shoot_timer = 0

        self.last_shot_time = pygame.time.get_ticks()

    def change_sprite(self, new_image_path):
        new_image = pygame.image.load(new_image_path)
        self.image = pygame.transform.scale(new_image, (100, 100))
        self.rect = self.image.get_rect(center=self.rect.center)

    def hit(self):
        bullet_hits = pygame.sprite.spritecollide(self, Bullet.bullets, True)
        for bullet in bullet_hits:
            self.hit_time = pygame.time.get_ticks()
            self.change_sprite('../sprites/enemy_1_hit.png')
            self.health -= 10
            if self.health <= 0:
                self.killed = True
            bullet.kill()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        new_x = self.rect.x
        new_y = self.rect.y

        if not self.can_shoot:
            self.shoot_timer += dt
            if self.shoot_timer >= 0.8:
                self.can_shoot = True
                self.shoot_timer = 0

        if self.can_shoot:
            self.shoot(dt)
                
        if not self.entry_complete:
            entry_distance = self.entry_speed * self.entry_duration
            entry_speed_y = entry_distance / self.entry_duration
            new_y = self.rect.y + entry_speed_y * 3
            new_x = self.rect.x
            if new_y >= self.initial_y:
                new_y = self.initial_y
                self.entry_complete = True
                self.start_time = current_time
                self.initial_x = new_x
                self.initial_y = new_y

        else:
            if self.movement_type == "linear":
                new_x = self.initial_x + self.amplitude * math.sin(self.frequency * elapsed_time + self.phase)
                new_y = self.initial_y + self.speed * elapsed_time
            elif self.movement_type == "circular":
                new_x = 150 + 100 * math.cos(elapsed_time)
                new_y = self.initial_y + 300 * math.sin(elapsed_time)
            elif self.movement_type == "circular_opposite":
                new_x = 750 - 100 * math.cos(elapsed_time)
                new_y = self.initial_y + 300 * math.sin(elapsed_time)

        self.rect.x = new_x
        self.rect.y = new_y

        if self.hit_time:
            seconds_passed = (pygame.time.get_ticks() - self.hit_time) / 1000
            if seconds_passed >= 0.1:
                self.change_sprite('../sprites/enemy_1.png')
                self.hit_time = None

    def shoot(self, dt):
        if self.can_shoot:
            bullet = BadBullet(self.rect.centerx, self.rect.centery, self.screen_height)
            BadBullet.bullets.add(bullet)
            self.can_shoot = False


    def draw(self, screen):
        screen.blit(self.image, self.rect)
