import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Jump and Run')

# Clock to control frame rate
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player properties
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_x = 100
player_y = HEIGHT - PLAYER_HEIGHT - 10  # Start on the ground
player_vel_y = 0
GRAVITY = 0.8
JUMP_STRENGTH = -15

# Ground level
GROUND_Y = HEIGHT - 10

# Obstacles
obstacle_width = 20
obstacle_height = 50
obstacle_speed = 5
obstacles = []

def create_obstacle():
    x = WIDTH
    y = GROUND_Y - obstacle_height
    rect = pygame.Rect(x, y, obstacle_width, obstacle_height)
    obstacles.append(rect)

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)

def draw_window():
    SCREEN.fill(WHITE)
    # Draw player
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, player_rect)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(SCREEN, BLACK, obs)

    # Draw score
    score_surf = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_surf, (10, 10))

    pygame.display.flip()

def handle_obstacles():
    global score
    for obs in list(obstacles):
        obs.x -= obstacle_speed
        if obs.x + obs.width < 0:
            obstacles.remove(obs)
            score += 1  # increase score when obstacle leaves screen
    # Add new obstacle randomly
    if len(obstacles) == 0 or obstacles[-1].x < WIDTH - 200:
        if random.random() < 0.02:
            create_obstacle()

def check_collisions(player_rect):
    for obs in obstacles:
        if player_rect.colliderect(obs):
            return True
    return False

running = True

while running:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y >= GROUND_Y - PLAYER_HEIGHT:
                player_vel_y = JUMP_STRENGTH

    # Apply gravity
    player_vel_y += GRAVITY
    player_y += player_vel_y

    if player_y > GROUND_Y - PLAYER_HEIGHT:
        player_y = GROUND_Y - PLAYER_HEIGHT
        player_vel_y = 0

    # Update obstacles
    handle_obstacles()

    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    if check_collisions(player_rect):
        print("Game Over! Final Score:", score)
        running = False

    draw_window()

pygame.quit()
