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
import random

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

plane_1_hit = pygame.image.load('../sprites/plane_1_hit.png')
plane_2_hit = pygame.image.load('../sprites/plane_2_hit.png')
plane_3_hit = pygame.image.load('../sprites/plane_3_hit.png')

x = 440
y = 800

plane = Plane(screen, x, y, plane_1_standard, plane_1_slow, plane_1_fast, plane_2_standard, plane_2_slow, plane_2_fast, plane_3_standard, plane_3_slow, plane_3_fast, plane_1_hit, plane_2_hit, plane_3_hit)

bg = Background('../images/space.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
win_screen = WinScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()

running = True
game_running = False
game_won = False
game_over = False

enemy_spawn_delay = 2
enemy_spawn_counter = 0

enemy_wave_1_spawn_index = 0
enemy_wave_2_spawn_index = 0
enemy_wave_3_spawn_index = 0

enemy_kill_counter = 0

win_displayed = False

game_started = False

score = 0

lose_cliche_selected = False
lose_random_cliche = ""

win_cliche_selected = False
win_random_cliche = ""

def reset_game():
    global game_over, game_running, game_started, enemy_wave_1_spawn_info, enemy_wave_2_spawn_info, enemy_wave_3_spawn_info, enemy_wave_1_spawn_index, enemy_wave_2_spawn_index, enemy_wave_3_spawn_index, enemy_kill_counter, score, win_displayed
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
    
    enemy_wave_1_spawn_info = [Enemy_1(300, 250, 2, "circular", SCREEN_HEIGHT), Enemy_1(700, 250, 2, "circular_opposite", SCREEN_HEIGHT), Enemy_1(500, 50, 2, "linear", SCREEN_HEIGHT), Enemy_1(500, 325, 2, "linear", SCREEN_HEIGHT), Enemy_1(500, 600, 2, "linear", SCREEN_HEIGHT)]

    enemy_wave_2_spawn_info = [Enemy_2(500, 100, 2, "linear", SCREEN_HEIGHT), Enemy_2(500, 250, 2, "linear_opposite", SCREEN_HEIGHT), Enemy_2(500, 400, 2, "linear_opposite", SCREEN_HEIGHT), Enemy_2(200, 300, 2, "downwards", SCREEN_HEIGHT), Enemy_2(800, 300, 2, "downwards", SCREEN_HEIGHT)]

    enemy_wave_3_spawn_info = [Enemy_3(500, 100, 1, "linear", SCREEN_HEIGHT)]
    
    enemy_wave_1_spawn_index = 0
    enemy_wave_2_spawn_index = 0
    enemy_wave_3_spawn_index = 0
    enemy_kill_counter = 0
    score = 0
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
                elif game_over:
                    lose_cliche_selected = False
                    reset_game()
                elif game_won:
                    win_cliche_selected = False
                    reset_game()


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

            for enemy in enemies_1:
                if enemy.killed:
                    enemy_kill_counter += 1
                    score += 100
                    enemy.kill()

            for enemy in enemies_2:
                if enemy.killed:
                    enemy_kill_counter += 1
                    score += 200
                    enemy.kill()

            for enemy in enemies_3:
                if enemy.killed:
                    enemy_kill_counter += 1
                    score += 500
                    enemy.kill()

            if enemy_kill_counter >= (len(enemy_wave_1_spawn_info) + len(enemy_wave_2_spawn_info) + len(enemy_wave_3_spawn_info)) and not win_displayed:
                game_won = True
                win_displayed = True
                enemy_kill_counter = 0

            for enemy in list(enemies_1) or list(enemies_2) or list(enemies_3):
                enemy.hit()
                enemy.update(dt)
                enemy.draw(screen)

        font = pygame.font.Font(None, 36)

        if plane.health <= 0:
            if not lose_cliche_selected:
                cliche_game_over = ["You'll get 'em next time!", "Better luck next time!", "You can do it!", "You're so close!", "Game over!"]
                random_int = random.randint(0, len(cliche_game_over) - 1)
                lose_random_cliche = cliche_game_over[random_int]
                lose_cliche_selected = True

            screen.fill((0, 0, 0))
            gameover_text = font.render(lose_random_cliche, True, (255, 0, 0))
            score_text = font.render('Score: ' + str(score), True, (255, 0, 0))
            space_down_text = font.render('Press Space to head back to the home screen', True, (255, 0, 0))
            
            gameover_text_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            space_down_text_rect = space_down_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

            screen.blit(gameover_text, gameover_text_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(space_down_text, space_down_text_rect)
            
            pygame.display.update()
            game_over = True
            game_started = False
            plane.rect.x = x
            plane.rect.y = y
            plane.update(dt, 0)


        if game_won:
            if not win_cliche_selected:
                cliche_game_won = ["You did it!", "You're a winner!", "You're a champion!", "You're a hero!", "You're a legend!"]
                random_int = random.randint(0, len(cliche_game_won) - 1)
                win_random_cliche = cliche_game_won[random_int]
                win_cliche_selected = True

            screen.fill((0, 0, 0))
            win_text = font.render(win_random_cliche, True, (255, 0, 0))
            score_text = font.render('Score: ' + str(score), True, (255, 0, 0))
            space_down_text = font.render('Press Space to head back to the home screen', True, (255, 0, 0))
            
            win_text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            space_down_text_rect = space_down_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

            screen.blit(win_text, win_text_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(space_down_text, space_down_text_rect)
            
            pygame.display.update()

    else:
        if not game_over:
            title_screen.update(screen)
        else:
            game_over_screen.update(screen)
            

    pygame.display.flip()

pygame.quit()
