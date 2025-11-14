import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_img = pygame.Surface((40, 40))
player_img.fill((0, 255, 0))
lanes = [100, 180, 260]
player_lane = 1
player_y = 500
jump = False
jump_height = 0

obstacles = []

def spawn_obstacle():
    lane = random.randint(0, 2)
    rect = pygame.Rect(lanes[lane], -40, 40, 40)
    obstacles.append(rect)

def draw_game():
    screen.fill((50, 50, 50))
    player_x = lanes[player_lane]
    if jump:
        y = player_y - jump_height
    else:
        y = player_y
    screen.blit(player_img, (player_x, y))

    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obs)

    pygame.display.flip()

def update_game():
    for obs in obstacles:
        obs.y += 5
    obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]

def check_collision():
    player_rect = pygame.Rect(lanes[player_lane], player_y - (jump_height if jump else 0), 40, 40)
    for obs in obstacles:
        if player_rect.colliderect(obs):
            return True
    return False
