import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, movement_type):
        super().__init__()
        self.image = pygame.image.load('../sprites/enemy_1.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, -self.rect.height)
        self.speed = speed
        self.start_time = pygame.time.get_ticks()
        self.initial_x = x
        self.initial_y = y
        self.amplitude = 50
        self.frequency = 2
        self.phase = 0
        self.movement_type = movement_type
        self.entry_speed = 1
        self.entry_duration = 2
        self.entry_complete = False

    def update(self, screen_width, screen_height):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if not self.entry_complete:
            entry_distance = self.entry_speed * self.entry_duration
            entry_speed_y = entry_distance / self.entry_duration
            new_y = self.rect.y + entry_speed_y * 3
            if new_y >= self.initial_y:
                new_y = self.initial_y
                self.entry_complete = True
                self.start_time = current_time
        else:
            new_y = self.rect.y

        if self.movement_type == "linear":
            new_x = self.initial_x + self.amplitude * math.sin(self.frequency * elapsed_time + self.phase)
        elif self.movement_type == 'circular':
            new_x = self.initial_x + 100 * math.cos(elapsed_time)
            new_y = self.initial_y + 100 * math.sin(elapsed_time)
        elif self.movement_type == "squiggly":
            new_x = self.initial_x + self.amplitude * math.sin(self.frequency * elapsed_time + self.phase)
            new_y = self.initial_y + self.amplitude * math.cos(self.frequency * elapsed_time + self.phase)
        else:
            new_x = self.initial_x
            new_y = self.initial_y
    



        self.rect.x = new_x
        self.rect.y = new_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)