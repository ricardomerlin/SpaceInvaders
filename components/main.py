import pygame
from plane import Plane
from enemy_1 import Enemy_1
from bullet import Bullet
from background import Background
from title_screen import TitleScreen

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# bullets = pygame.sprite.Group()

bad_bullets = pygame.sprite.Group()
enemies_1 = pygame.sprite.Group()
enemies_2 = pygame.sprite.Group()
enemies_3 = pygame.sprite.Group()


plane_1_standard = pygame.image.load('../sprites/plane_1_standard.png')
plane_1_slow = pygame.image.load('../sprites/plane_1_slow.png')
plane_1_fast = pygame.image.load('../sprites/plane_1_fast.png')

plane_2_standard = pygame.image.load('../sprites/plane_2_standard.png')
plane_2_slow = pygame.image.load('../sprites/plane_2_slow.png')
plane_2_fast = pygame.image.load('../sprites/plane_2_fast.png')

plane_3_standard = pygame.image.load('../sprites/plane_3_standard.png')
plane_3_slow = pygame.image.load('../sprites/plane_3_slow.png')
plane_3_fast = pygame.image.load('../sprites/plane_3_fast.png')

x = 440
y = 800

plane = Plane(screen, x, y, bad_bullets, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast)

bg = Background('../images/space.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

running = True
game_running = False

enemy_speed = 2
enemy_wave_1_spawn_info = [Enemy_1(x=300, y=250, speed=2, movement_type="circular"), Enemy_1(x=500, y=250, speed=2, movement_type="linear"), Enemy_1(x=700, y=250, speed=2, movement_type="circular_opposite")]
enemy_wave_2_spawn_info = [Enemy_1(x=300, y=250, speed=2, movement_type="circular"), Enemy_1(x=500, y=250, speed=2, movement_type="linear"), Enemy_1(x=700, y=250, speed=2, movement_type="circular_opposite")]


spawn_enemy_event = pygame.USEREVENT + 1

enemy_spawn_delay = 3
enemy_spawn_counter = 0
enemy_spawn_index = 0

enemy_kill_counter = 0

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_running:
                title_screen.start_game()
                plane.start_time = pygame.time.get_ticks()
                game_running = True

    bg.update(dt, game_running)
    bg.draw(screen)

    if game_running:
        elapsed_seconds = (pygame.time.get_ticks() - plane.start_time) // 1000
        plane.update(dt, elapsed_seconds)
        Bullet.update_all(dt)
        plane.draw(screen)
        plane.healthbar(screen)
        Bullet.draw_all(screen)
        Bullet.bullets.update(dt)
        bad_bullets.update(dt)


        enemy_spawn_counter += dt
        if enemy_spawn_counter >= enemy_spawn_delay:
            if enemy_spawn_index < len(enemy_wave_1_spawn_info):
                enemies_1.add(enemy_wave_1_spawn_info[enemy_spawn_index])
                enemy_spawn_index += 1
                print('enemies_1 length:', len(enemies_1))
            enemy_spawn_counter = 0
            

        print(enemy_kill_counter)
        enemies_to_remove = []
        for enemy in enemies_1:
            if enemy.killed == True:
                enemy_kill_counter += 1
                enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            enemies_1.remove(enemy)

        print(enemy_spawn_counter)
        print('enemy spawn index: {enemy_spawn_index}')

        if 3 <= enemy_kill_counter < 6:
            enemy_spawn_index = 0
            for enemy in enemy_wave_2_spawn_info:
                enemies_2.add(enemy)




        for enemy in list(enemies_1) or list(enemies_2) or list(enemies_3):
            enemy.hit()
            enemy.update()
            enemy.draw(screen)


    else:
        title_screen.update(screen)

    pygame.display.flip()

pygame.quit()
