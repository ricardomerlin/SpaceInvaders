import pygame
from plane import Plane
from enemy_1 import Enemy_1
from enemy_2 import Enemy_2
from enemy_3 import Enemy_3
from bullet import Bullet
from badBullet import BadBullet
from missles import Missle
from monsterGoo import MonsterGoo
from background import Background
from title_screen import TitleScreen
from win_screen import WinScreen
from gameover_screen import GameOverScreen

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

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

plane = Plane(screen, x, y, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast)

bg = Background('../images/space.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
win_screen = WinScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

running = True
game_running = False
game_won = False
game_over = False

enemy_speed = 2

spawn_enemy_event = pygame.USEREVENT + 1

enemy_spawn_delay = 2
enemy_spawn_counter = 0

enemy_wave_1_spawn_index = 0
enemy_wave_2_spawn_index = 0
enemy_wave_3_spawn_index = 0

enemy_kill_counter = 0

win_displayed = False

game_started = False

def reset_game():
    global game_over, game_running, game_started, enemy_wave_1_spawn_info, enemy_wave_2_spawn_info, enemy_wave_3_spawn_info, enemy_wave_1_spawn_index, enemy_wave_2_spawn_index, enemy_wave_3_spawn_index, enemy_kill_counter, win_displayed
    game_over = False
    game_running = False
    game_started = False
    plane.health = 1000
    Bullet.bullets.empty()
    BadBullet.bullets.empty()
    Missle.missles.empty()
    MonsterGoo.goos.empty()
    enemies_1.empty()
    enemies_2.empty()
    enemies_3.empty()

    
    enemy_wave_1_spawn_info = [Enemy_1(300, 250, speed=2, movement_type="circular", screen_height=SCREEN_HEIGHT), Enemy_1(x=700, y=250, speed=2, movement_type="circular_opposite", screen_height=SCREEN_HEIGHT), Enemy_1(x=500, y=50, speed=2, movement_type="linear", screen_height=SCREEN_HEIGHT), Enemy_1(x=500, y=325, speed=2, movement_type="linear", screen_height=SCREEN_HEIGHT), Enemy_1(x=500, y=600, speed=2, movement_type="linear", screen_height=SCREEN_HEIGHT)]

    enemy_wave_2_spawn_info = [Enemy_2(x=500, y=100, speed=2, movement_type="linear", screen_height=SCREEN_HEIGHT), Enemy_2(x=500, y=250, speed=2, movement_type="linear_opposite", screen_height=SCREEN_HEIGHT), Enemy_2(x=500, y=400, speed=2, movement_type="linear_opposite", screen_height=SCREEN_HEIGHT), Enemy_2(x=200, y=300, speed=2, movement_type="downwards", screen_height=SCREEN_HEIGHT), Enemy_2(x=800, y=300, speed=2, movement_type="downwards", screen_height=SCREEN_HEIGHT)]

    enemy_wave_3_spawn_info = [Enemy_3(x=500, y=100, speed=1, movement_type="linear", screen_height=SCREEN_HEIGHT)]
    
    enemy_spawn_counter = 0
    enemy_wave_1_spawn_index = 0
    enemy_wave_2_spawn_index = 0
    enemy_wave_3_spawn_index = 0
    enemy_kill_counter = 0
    win_displayed = False
    
    title_screen.update(screen)




while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_running:
                    reset_game()
                    game_running = True
                    game_won = False
                    game_over = False
                    game_started = True
                    title_screen.start_game()
                    plane.start_time = pygame.time.get_ticks()

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
        BadBullet.draw_all(screen)
        BadBullet.bullets.update(dt)
        Missle.draw_all(screen)
        Missle.missles.update(dt)
        MonsterGoo.draw_all(screen)
        MonsterGoo.goos.update(dt)

        enemy_spawn_counter += dt
        if game_started:
            if enemy_spawn_counter >= enemy_spawn_delay:
                if enemy_wave_1_spawn_index < len(enemy_wave_1_spawn_info):
                    enemies_1.add(enemy_wave_1_spawn_info[enemy_wave_1_spawn_index])
                    enemy_wave_1_spawn_index += 1
                elif enemy_wave_2_spawn_index < len(enemy_wave_2_spawn_info):
                    enemies_2.add(enemy_wave_2_spawn_info[enemy_wave_2_spawn_index])
                    enemy_wave_2_spawn_index += 1
                elif enemy_wave_3_spawn_index < len(enemy_wave_3_spawn_info):
                    enemies_3.add(enemy_wave_3_spawn_info[enemy_wave_3_spawn_index])
                    enemy_wave_3_spawn_index += 1
                enemy_spawn_counter = 0

            for enemy in enemies_2:
                if enemy.killed:
                    enemy_kill_counter += 1
                    enemy.kill()

            for enemy in enemies_3:
                if enemy.killed:
                    enemy_kill_counter += 1
                    enemy.kill()

            if enemy_kill_counter >= (len(enemy_wave_1_spawn_info) + len(enemy_wave_2_spawn_info) + len(enemy_wave_3_spawn_info)) and not win_displayed:
                game_running = False
                game_won = True
                win_displayed = True
                enemy_kill_counter = 0


            for enemy in list(enemies_1) or list(enemies_2) or list(enemies_3):
                enemy.hit()
                enemy.update(dt)
                enemy.draw(screen)
            

            enemies_to_remove = []
            for enemy in enemies_1:
                if enemy.killed:
                    enemy_kill_counter += 1
                    enemy.kill()


        font = pygame.font.Font(None, 36)
        if plane.health <= 0:
            gameover_text = font.render('Game Over', True, (255, 0, 0))
            screen.blit(gameover_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
            pygame.display.update()
            game_over = True
            pygame.time.delay(2000)
            game_started = False
            plane.rect.x = x
            plane.rect.y = y
            plane.update(dt, 0)
            reset_game()

        if game_won:
            gameover_text = font.render('You Win!', True, (255, 0, 0))
            screen.blit(gameover_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            reset_game()

    else:
        if not game_over:
            title_screen.update(screen)
        else:
            game_over_screen.update(screen)
            

    pygame.display.flip()

pygame.quit()
