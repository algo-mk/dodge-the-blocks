import pygame
import random
import sys
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚡ Dodge the Blocks ⚡")

clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 60, bold=True)

# Player setup
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size - 20]
player_speed = 7

# Enemy setup
enemy_size = 50
enemy_list = []
enemy_speed = 5
enemy_spawn_rate = 25

# Power-up
powerup_size = 30
powerup_pos = [random.randint(0, WIDTH - powerup_size), -1000]
powerup_active = False
powerup_timer = 0

# Game state
score = 0
lives = 3
game_over = False

# Colors
WHITE = (255, 255, 255)
DARK = (30, 30, 30)
GLOW_BLUE = (50, 150, 255)
GLOW_RED = (255, 60, 60)
YELLOW = (255, 255, 100)
GREEN = (0, 255, 180)

def draw_gradient_background():
    for y in range(HEIGHT):
        color = (30 + y // 30, 30 + y // 40, 60 + y // 20)
        pygame.draw.line(win, color, (0, y), (WIDTH, y))

def draw_shadow_text(text, font, x, y, color=WHITE, shadow=(3, 3)):
    shadow_text = font.render(text, True, (0, 0, 0))
    win.blit(shadow_text, (x + shadow[0], y + shadow[1]))
    main_text = font.render(text, True, color)
    win.blit(main_text, (x, y))

def draw_glow_rect(pos, size, color, glow_strength=4):
    for i in range(glow_strength, 0, -1):
        alpha = max(20, 255 // (i * 2))
        glow_surface = pygame.Surface((size + i*2, size + i*2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*color, alpha), (0, 0, size + i*2, size + i*2), border_radius=8)
        win.blit(glow_surface, (pos[0] - i, pos[1] - i))
    pygame.draw.rect(win, color, (*pos, size, size), border_radius=8)

def draw_player(pos):
    draw_glow_rect(pos, player_size, GLOW_BLUE)

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        draw_glow_rect(enemy, enemy_size, GLOW_RED)

def drop_enemies():
    if random.randint(1, enemy_spawn_rate) == 1:
        x = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x, 0])

def update_enemy_positions():
    global lives, score
    for enemy in enemy_list[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)
            score += 1
        elif detect_collision(player_pos, enemy):
            if not powerup_active:
                enemy_list.remove(enemy)
                lives -= 1

def detect_collision(p1, p2):
    px, py = p1
    ex, ey = p2
    return (ex < px + player_size and ex + enemy_size > px and
            ey < py + player_size and ey + enemy_size > py)

def draw_powerup(pos, t):
    pulse = 5 * math.sin(t / 200)
    size = powerup_size + pulse
    x = pos[0] + powerup_size // 2
    y = pos[1] + powerup_size // 2
    pygame.draw.circle(win, YELLOW, (x, y), int(size // 2))

def reset_game():
    global enemy_list, score, lives, game_over, player_pos, powerup_active, powerup_timer, powerup_pos
    enemy_list = []
    score = 0
    lives = 3
    game_over = False
    player_pos = [WIDTH // 2, HEIGHT - player_size - 20]
    powerup_active = False
    powerup_timer = 0
    powerup_pos = [random.randint(0, WIDTH - powerup_size), -1000]

# Main loop
while True:
    clock.tick(FPS)
    time_now = pygame.time.get_ticks()
    draw_gradient_background()

    if not game_over:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed

        # Enemies
        drop_enemies()
        update_enemy_positions()

        # Power-up
        powerup_pos[1] += 5
        if powerup_pos[1] > HEIGHT:
            powerup_pos = [random.randint(0, WIDTH - powerup_size), -1000]
        if detect_collision(player_pos, powerup_pos):
            powerup_active = True
            powerup_timer = time_now
            powerup_pos = [random.randint(0, WIDTH - powerup_size), -1000]

        if powerup_active and time_now - powerup_timer > 5000:
            powerup_active = False

        # Draw
        draw_player(player_pos)
        draw_enemies(enemy_list)
        draw_powerup(powerup_pos, time_now)

        # HUD
        draw_shadow_text(f"Score: {score}", font, 10, 10)
        draw_shadow_text(f"Lives: {lives}", font, 10, 40)
        if powerup_active:
            draw_shadow_text("Shield ON", font, WIDTH - 160, 10, GREEN)

        if lives <= 0:
            game_over = True

    else:
        draw_shadow_text("GAME OVER", big_font, WIDTH//2 - 180, HEIGHT//2 - 100, GLOW_RED)
        draw_shadow_text(f"Final Score: {score}", font, WIDTH//2 - 100, HEIGHT//2 - 20)
        draw_shadow_text("Press R to Restart or Q to Quit", font, WIDTH//2 - 180, HEIGHT//2 + 40, YELLOW)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
