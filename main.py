import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("A Wonderful Easter")

# Game variables
player_speed = 2
egg_speed = 0.3
egg_drop_interval = random.randint(1000, 3000)
missed_eggs = 0
difficulty_increase_interval = 20000  # milliseconds, interval to increase difficulty
last_difficulty_increase = pygame.time.get_ticks()  # Last time the difficulty was increased

max_missed_eggs = 5

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

playerImg = pygame.image.load('player.png')
eggImg = pygame.image.load('egg.png')
backgroundImg = pygame.image.load('background.png')
playerImg = pygame.transform.scale(playerImg, (150, 150))
eggImg = pygame.transform.scale(eggImg, (80, 90))
backgroundImg = pygame.transform.scale(backgroundImg, (800, 600))

# Player start position
playerX = screen_width / 2
playerY = screen_height - 200
playerX_change = 0

# Egg start position
eggX = random.randint(0, screen_width)
eggY = 0

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (x, y))
    missed_text = font.render("Missed: " + str(missed_eggs) + "/" + str(max_missed_eggs), True, white)
    screen.blit(missed_text, (x, y + 30))  # Adjust y + 30 or as needed to position correctly

def player(x, y):
    screen.blit(playerImg, (x, y))

def egg(x, y):
    screen.blit(eggImg, (x, y))

def is_collision(eggX, eggY, playerX, playerY):
    distance = ((eggX - playerX)**2 + (eggY - playerY)**2)**0.5
    if distance < 50:
        return True
    else:
        return False

def game_over():
    over_text = font.render("GAME OVER", True, white)
    screen.blit(over_text, (250, 250))

running = True
last_egg_drop = pygame.time.get_ticks()

while running:
    screen.fill(black)
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    current_time = pygame.time.get_ticks()
    if current_time - last_difficulty_increase > difficulty_increase_interval:
        egg_speed += 0.5
        if egg_drop_interval > 200:  # Ensure the drop interval doesn't become too small
            egg_drop_interval -= 50
        last_difficulty_increase = current_time

    # Player Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 150:  # Adjust according to the scaled player image width
        playerX = screen_width - 150

    # Egg Movement
    eggY += egg_speed

    # Check for collision
    collision = is_collision(eggX, eggY, playerX, playerY)
    if collision:
        score += 1
        eggY = 0  # Reset egg to the top
        eggX = random.randint(0, screen_width)  # Move egg to a new random X position
    elif eggY > screen_height-150:
        missed_eggs += 1
        eggY = 0  # Reset egg to the top
        eggX = random.randint(0, screen_width)  # Move egg to a new random X position

    if missed_eggs >= max_missed_eggs:
        game_over()
        pygame.display.update()
        pygame.time.wait(2000)
        break

    player(playerX, playerY)
    egg(eggX, eggY)
    show_score(10, 10)
    pygame.display.update()
