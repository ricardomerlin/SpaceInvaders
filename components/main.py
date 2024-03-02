import pygame
from plane import Plane
from enemy import Enemy
from bullet import Bullet
from background import Background
from title_screen import TitleScreen

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

bullets = pygame.sprite.Group()
bad_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Load plane sprites
plane_1_standard = pygame.image.load('../sprites/plane_1_standard.png')
plane_1_slow = pygame.image.load('../sprites/plane_1_slow.png')
plane_1_fast = pygame.image.load('../sprites/plane_1_fast.png')

plane_2_standard = pygame.image.load('../sprites/plane_2_standard.png')
plane_2_slow = pygame.image.load('../sprites/plane_2_slow.png')
plane_2_fast = pygame.image.load('../sprites/plane_2_fast.png')

plane_3_standard = pygame.image.load('../sprites/plane_3_standard.png')
plane_3_slow = pygame.image.load('../sprites/plane_3_slow.png')
plane_3_fast = pygame.image.load('../sprites/plane_3_fast.png')

x = 500
y = 800

plane = Plane(screen, x, y, bullets, bad_bullets, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast)

bg = Background('../images/space.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

running = True
game_running = False

enemy_speed = 2  #
enemy_wave_1_spawn_info = [Enemy(x=100, y=100, speed=2, movement_type="cirular"), Enemy(x=500, y=100, speed=2, movement_type="squiggly"), Enemy(x=800, y=100, speed=2, movement_type="linear")]

spawn_enemy_event = pygame.USEREVENT + 1

enemy_spawn_delay = 3
enemy_spawn_counter = 0
enemy_spawn_index = 0

# Main game loop
while running:
    dt = clock.tick(60) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_running:
                title_screen.start_game()
                plane.start_time = pygame.time.get_ticks()
                game_running = True
        # elif event.type == spawn_enemy_event and game_running:  # Check if it's time to spawn a new enemy
        #     # Create a new enemy and add it to the enemies group
        #     for enemy_info in enemy_wave_1_spawn_info:
        #         enemies.add(enemy_info)

    bg.update(dt, game_running)
    bg.draw(screen)

    if game_running:
        elapsed_seconds = (pygame.time.get_ticks() - plane.start_time) // 1000
        plane.update(dt, elapsed_seconds)
        Bullet.update_all(dt)
        plane.draw(screen)
        plane.healthbar(screen)
        Bullet.draw_all(screen)
        bullets.update(dt)
        bad_bullets.update(dt)

        enemy_spawn_counter += dt
        if enemy_spawn_counter >= enemy_spawn_delay:
            # If enough time has passed, spawn a new enemy and reset the counter
            if enemy_spawn_index < len(enemy_wave_1_spawn_info):  # Check if there are still enemies to spawn
                enemies.add(enemy_wave_1_spawn_info[enemy_spawn_index])  # Add the next enemy
                enemy_spawn_index += 1  # Move to the next enemy
            enemy_spawn_counter = 0

        for enemy in enemies:
            enemy.update(SCREEN_WIDTH, SCREEN_HEIGHT)
            enemy.draw(screen)  # Draw the enemy in every iteration of the game loop

    else:
        title_screen.update(screen)

    pygame.display.flip()

pygame.quit()