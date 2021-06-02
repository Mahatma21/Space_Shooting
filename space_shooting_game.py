import pygame
from pygame import mixer
import random
import math


def player(x, y):
    win.blit(playerImg, (x, y))


def enemy(x, y, enemyImg):
    win.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    win.blit(bulletImg, (x + PLAYER_SIZE / 2 - BULLET_SIZE / 2, y + BULLET_SIZE))


def isCollision(avatar1X, avatar1Y, avatar2X, avatar2Y, max_distance):
    distance = math.sqrt(
        math.pow(avatar1X - avatar2X, 2) + math.pow(avatar1Y - avatar2Y, 2))

    if distance <= max_distance:
        return True
    return False


def show_score(x, y):
    score = score_font.render(f"Score: {score_value}", True, (235, 235, 235))
    win.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (235, 0, 0))
    win.blit(over_text, (230, 250))


def info_text1():
    info_text = info_font.render("- Arrow key to move", True, (235, 235, 0))
    win.blit(info_text, (170, 230))


def info_text2():
    info_text = info_font.render("- Space to shoot", True, (235, 235, 0))
    win.blit(info_text, (170, 280))


def info_text3():
    info_text = info_font.render("Press ENTER to continue", True, (0, 235, 0))
    win.blit(info_text, (170, 500))


def alert_text():
    alert_text = alert_font.render(
        "Don't to close with them !", True, (235, 235, 0))
    win.blit(alert_text, (120, 270))


# Initialize the pygame
mixer.init()
pygame.init()

WIDTH = 800
HEIGHT = 600

ICON = pygame.image.load("Belajar_Pygame/icon.png")

PLAYER_SIZE = 64
PLAYER_CHANGE = 4
PLAYER_LIMIT = HEIGHT / 2 - PLAYER_SIZE / 2

enemy_x_change = 2
ENEMY_Y_CHANGE = 37.5
ENEMY_SIZE = PLAYER_SIZE
NUM_OF_ENEMIES = 6
ENEMY_IMG = ("Belajar_Pygame/enemy1.png", "Belajar_Pygame/enemy2.png")
ENEMY_SPEED_INCREASE = 0.0005

BULLET_SIZE = 24
BULLET_CHANGE = 6

SCORE_X = 10
SCORE_Y = 10

# Background
BACKGROUND = pygame.image.load("Belajar_Pygame/spaceBackground.png")
# Sound
bullet_sound = mixer.Sound("Belajar_Pygame/laser.wav")
bullet_sound.set_volume(0.1)
collision_sound = mixer.Sound("Belajar_Pygame/explosion.wav")
collision_sound.set_volume(0.1)

# Create a window
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Change the title and icon
pygame.display.set_caption("First Game")
pygame.display.set_icon(ICON)

# Player
playerImg = pygame.image.load('Belajar_Pygame/spaceship.png')
playerImg = pygame.transform.smoothscale(
    playerImg, (PLAYER_SIZE, PLAYER_SIZE))
playerX = (WIDTH / 2) - (PLAYER_SIZE / 2)
playerY = (HEIGHT * 3 / 4) - (PLAYER_SIZE / 2)
playerX_plus = 0
playerX_minus = 0
playerY_plus = 0
playerY_minus = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
# Create multiple enemy
for i in range(NUM_OF_ENEMIES):
    enemyImg.append(pygame.image.load(random.choice(ENEMY_IMG)))
    enemyImg[i] = pygame.transform.smoothscale(
        enemyImg[i], (ENEMY_SIZE, ENEMY_SIZE))
    enemyX.append(random.randint(0, WIDTH - ENEMY_SIZE))
    enemyY.append(random.randint(0, (HEIGHT * 1 / 4) - ENEMY_SIZE))
    enemyX_change.append(enemy_x_change)
    enemyY_change.append(ENEMY_Y_CHANGE)

# bullet
bulletImg = pygame.image.load('Belajar_Pygame/bullet.png')
bulletImg = pygame.transform.smoothscale(
    bulletImg, (BULLET_SIZE, BULLET_SIZE))
bulletX = 0
bulletY = 0
bullet_state = 'ready'

# Score
score_font = pygame.font.Font('Belajar_Pygame/pixel_font.ttf', 32)
score_value = 0

# Game over font
over_font = pygame.font.Font("Belajar_Pygame/pixel_font.ttf", 64)
isGameOver = False

# Info font
info_font = pygame.font. Font("Belajar_Pygame/pixel_font.ttf", 32)

# Alert font
alert_font = pygame.font.Font("Belajar_Pygame/pixel_font.ttf", 40)

# Game run or not
running = True

# Info loop
info_running = True
while running and info_running:
    win.blit(BACKGROUND, (0, 0))
    info_text1()
    info_text2()
    info_text3()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                info_running = False

    pygame.display.update()

# Alert loop
alert_count = 0
while running and alert_count <= 3000:
    win.fill((0, 0, 0))
    alert_text()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    alert_count += 1

    pygame.display.update()

# Turn on the backsound if still running
if running:
    mixer.music.set_volume(0.2)
    mixer.music.load("Belajar_Pygame/backsound.wav")
    mixer.music.play(-1)

# Game loop
while running:
    # Background color
    # win.fill((33, 33, 33))
    # Background image
    win.blit(BACKGROUND, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_minus = -PLAYER_CHANGE
            if event.key == pygame.K_RIGHT:
                playerX_plus = PLAYER_CHANGE
            if event.key == pygame.K_UP:
                playerY_minus = -PLAYER_CHANGE
            if event.key == pygame.K_DOWN:
                playerY_plus = PLAYER_CHANGE
            # Shooting bullet
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound.play()
                bulletY = playerY
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_minus = 0
            if event.key == pygame.K_RIGHT:
                playerX_plus = 0
            if event.key == pygame.K_UP:
                playerY_minus = 0
            if event.key == pygame.K_DOWN:
                playerY_plus = 0

    playerX += playerX_minus + playerX_plus
    playerY += playerY_minus + playerY_plus

    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH - PLAYER_SIZE:
        playerX = WIDTH - PLAYER_SIZE

    if playerY <= PLAYER_LIMIT:
        playerY = PLAYER_LIMIT
    elif playerY >= HEIGHT - PLAYER_SIZE:
        playerY = HEIGHT - PLAYER_SIZE

    # Enemy movement
    # If the enemy hit the player
    if isGameOver:
        for i in range(NUM_OF_ENEMIES):
            # Turn off the backsound
            mixer.music.stop()
            # Move the enemy to out of window
            enemyY[i] = HEIGHT + ENEMY_SIZE + 100
            enemy(enemyX[i], enemyY[i], enemyImg[i])
            # Show the game over text
            game_over_text()
    # If the player still not collise by the enemy
    else:
        for i in range(NUM_OF_ENEMIES):

            # Enemy X movement direction
            if enemyX[i] <= 0:
                enemyX[i] = 0
                enemyX_change[i] = enemy_x_change
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= WIDTH - ENEMY_SIZE:
                enemyX[i] = WIDTH - ENEMY_SIZE
                enemyX_change[i] = -enemy_x_change
                enemyY[i] += enemyY_change[i]

            # Enemy Y movement direction
            if enemyY[i] <= 0:
                enemyY[i] = 0
                enemyY_change[i] = ENEMY_Y_CHANGE
            elif enemyY[i] >= HEIGHT - ENEMY_SIZE:
                enemyY[i] = HEIGHT - ENEMY_SIZE
                enemyY_change[i] = -ENEMY_Y_CHANGE

            # Enemy movement
            enemyX[i] += enemyX_change[i]

            # Enemy and bullet collision
            enemy_collision = isCollision(
                enemyX[i],
                enemyY[i],
                bulletX, bulletY, BULLET_SIZE)
            if enemy_collision:
                collision_sound.play()
                bullet_state = 'ready'
                bulletY = 0 - BULLET_SIZE
                score_value += 1
                enemyX[i] = random.randint(0, WIDTH - ENEMY_SIZE)
                enemyY[i] = random.randint(0, (HEIGHT * 1 / 4) - ENEMY_SIZE)

            # Player and enemy collision
            player_collision = isCollision(
                playerX, playerY, enemyX[i],
                enemyY[i],
                PLAYER_SIZE)
            if player_collision:
                isGameOver = True
                break

            # Blit enemy img
            enemy(enemyX[i], enemyY[i], enemyImg[i])

    # Bullet movement
    if bulletY <= 0 - BULLET_SIZE:
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= BULLET_CHANGE

    # Increase the enemy speed
    enemy_x_change += ENEMY_SPEED_INCREASE

    # Blit player img
    player(playerX, playerY)

    # Blit score text
    show_score(SCORE_X, SCORE_Y)

    pygame.display.update()
