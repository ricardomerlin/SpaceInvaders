import pygame
import math
from badBullet import BadBullet
from bullet import Bullet
from missles import Missle
from monsterGoo import MonsterGoo
import random

class Enemy_3(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, movement_type, screen_height):
        super().__init__()
        self.image = pygame.image.load('../sprites/enemy_3.png')
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.center = (x, -self.rect.height)
        self.speed = speed
        self.start_time = pygame.time.get_ticks()
        self.initial_x = x
        self.initial_y = y
        self.amplitude = 200
        self.frequency = 2
        self.phase = 0
        self.movement_type = movement_type
        self.entry_speed = 1
        self.entry_duration = 2
        self.entry_complete = False
        self.health = 5000
        self.hit_time = None
        self.killed = False
        self.screen_height = screen_height

        self.can_shoot = True
        self.can_shoot_goo = True
        self.shoot_timer = 0
        self.shoot_goo_timer = 0

        self.last_shot_time = pygame.time.get_ticks()

    def change_sprite(self, new_image_path):
        new_image = pygame.image.load(new_image_path)
        self.image = pygame.transform.scale(new_image, (300, 300))
        self.rect = self.image.get_rect(center=self.rect.center)

    def hit(self):
        bullet_hits = pygame.sprite.spritecollide(self, Bullet.bullets, False)
        missle_hits = pygame.sprite.spritecollide(self, Missle.missles, False)
        for bullet in bullet_hits:
            self.hit_time = pygame.time.get_ticks()
            self.change_sprite('../sprites/enemy_3_hit.png')
            self.health -= 1000
            if self.health <= 0:
                self.killed = True
            bullet.kill()
        for missle in missle_hits:
            self.hit_time = pygame.time.get_ticks()
            self.change_sprite('../sprites/enemy_3_hit.png')
            self.health -= 30
            if self.health <= 0:
                self.killed = True
            missle.hit = True   

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        new_x = self.rect.x
        new_y = self.rect.y

        if not self.can_shoot:
            self.shoot_timer += dt
            if self.shoot_timer >= 0.3:
                self.can_shoot = True
                self.shoot_timer = 0

        if not self.can_shoot_goo:
            self.shoot_goo_timer += dt
            if self.shoot_goo_timer >= 1:
                self.can_shoot_goo = True
                self.shoot_goo_timer = 0

        if self.can_shoot:
            self.shoot(dt)

        if self.can_shoot_goo:
            self.shoot_goo(dt)

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
                new_y = self.initial_y + self.amplitude * math.cos(self.speed * elapsed_time)

        self.rect.x = new_x
        self.rect.y = new_y

        if self.hit_time:
            seconds_passed = (pygame.time.get_ticks() - self.hit_time) / 1000
            if seconds_passed >= 0.1:
                self.change_sprite('../sprites/enemy_3.png')
                self.hit_time = None

    def shoot(self, dt):
        if self.can_shoot:
            bullet = BadBullet(self.rect.centerx, self.rect.centery, self.screen_height)
            bullet2 = BadBullet(self.rect.centerx - 30, self.rect.centery, self.screen_height)
            bullet3 = BadBullet(self.rect.centerx + 30, self.rect.centery, self.screen_height)
            BadBullet.bullets.add(bullet, bullet2, bullet3)
            self.can_shoot = False

    def shoot_goo(self, dt):
        if self.can_shoot_goo:
            goo = MonsterGoo(self.rect.centerx, self.rect.centery, self.screen_height)
            MonsterGoo.goos.add(goo)
            self.can_shoot_goo = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
