import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Game Test")
clock = pygame.time.Clock()

lanes = [100, 180, 260]
player_lane = 1
player_y = 500
jump = False
jump_height = 0
obstacles = []
player_img = pygame.Surface((40, 40))
player_img.fill((0, 255, 0))

def spawn_obstacle():
    lane = random.randint(0, 2)
    rect = pygame.Rect(lanes[lane], -40, 40, 40)
    obstacles.append(rect)

def draw_game():
    screen.fill((30, 30, 30))
    x = lanes[player_lane]
    y = player_y - jump_height if jump else player_y
    screen.blit(player_img, (x, y))
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obs)
    pygame.display.flip()

def update_game():
    for obs in obstacles:
        obs.y += 5
    obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]

def check_collision():
    rect = pygame.Rect(lanes[player_lane], player_y - jump_height, 40, 40)
    for obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

pygame.time.set_timer(pygame.USEREVENT, 1500)
jump_timer = 0
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            spawn_obstacle()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_lane = max(0, player_lane - 1)
    if keys[pygame.K_RIGHT]:
        player_lane = min(2, player_lane + 1)
    if keys[pygame.K_UP] and not jump:
        jump = True
        jump_timer = pygame.time.get_ticks()

    if jump:
        t = (pygame.time.get_ticks() - jump_timer) / 200.0
        if t < 1:
            jump_height = int(50 * (1 - (t - 1) ** 2))
        else:
            jump = False
            jump_height = 0

    update_game()
    draw_game()

    if check_collision():
        print("💥 Game Over!")
        pygame.time.wait(2000)
        running = False

pygame.quit()
