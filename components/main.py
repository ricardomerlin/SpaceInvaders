import pygame
from plane import Plane
# from enemy import Enemy
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
# enemy = Enemy()

bg = Background('../images/space.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)

title_screen = TitleScreen()

clock = pygame.time.Clock()
running = True
game_running = False

while running:
    dt = clock.tick(60) / 1000.0
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_running:
                title_screen.start_game()
                plane.start_time = pygame.time.get_ticks()  # Set start_time when the game starts
                game_running = True
                
    bg.update(dt, game_running)
    bg.draw(screen)

    print('Game running:', game_running)
    
    if game_running == True:
        elapsed_seconds = (pygame.time.get_ticks() - plane.start_time) // 1000
        print('Elapsed seconds from the main.py:', elapsed_seconds)
        plane.update(dt, elapsed_seconds)
        Bullet.update_all(dt)
        plane.draw(screen)
        plane.healthbar(screen)
        Bullet.draw_all(screen)
    
    else:
        title_screen.update(screen)

    pygame.display.flip()

pygame.quit()
