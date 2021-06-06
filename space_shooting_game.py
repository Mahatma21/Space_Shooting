import pygame
from pygame import mixer
import random
import math
import datetime


def redraw_window():
    # Draw the info text
    if isInfo:
        # Draw the background
        win.blit(BG, (0, 0))
        # Draw info text
        info1 = INFO_FONT.render("- ARROW KEYS to move", True, (235, 235, 235))
        info2 = INFO_FONT.render("- SPACE to shoot", True, (235, 235, 235))
        win.blit(info1, (170, 250))
        win.blit(info2, (170, 300))
        enter = ENTER_FONT.render("Press ENTER to continue", True, (0, 235, 0))
        win.blit(enter, (180, 500))
    elif isAlert:
        # Draw black background
        win.fill((10, 10, 10))
        # Draw alert text
        alert = ALERT_FONT.render(
            "Don't too close with THEM !", True, (235, 235, 0))
        win.blit(alert, (105, 270))
    else:
        # Draw the background
        win.blit(BG, (0, 0))
        # Draw the player
        win.blit(PLAYER_IMG, (playerX, playerY))
        # Draw the bullet if player is shooting
        if isShooting:  # Just draw the bullet when shooting
            win.blit(BULLET_IMG, (bulletX, bulletY))

        # Draw the enemy
        if not isGameOver:
            [win.blit(ENEMY_IMG[i], (enemyX[i], enemyY[i]))
             for i in range(NUM_OF_ENEMIES)]
        else:  # If game over
            # Draw the enemy that collise with player
            win.blit(ENEMY_IMG[enemy_collision_num],
                     (enemyX[enemy_collision_num],
                      enemyY[enemy_collision_num]))
            game_over = GAME_OVER_FONT.render(f"GAME OVER", True, (235, 0, 0))
            win.blit(game_over, (100, 250))

        # Drow player score
        score = SCORE_FONT.render(
            f"Score: {score_count}", True, (235, 235, 235))
        win.blit(score, (20, 20))

    pygame.display.update()


def isCollision(spriteA_X, spriteA_Y, spriteA_size, spriteB_X, spriteB_Y,
                spriteB_size):
    distance = math.sqrt(
        math.pow(abs(spriteA_X - spriteB_X),
                 2) + math.pow(abs(spriteA_Y - spriteB_Y),
                               2))
    if spriteA_X > spriteB_X:
        max_distance = spriteB_size
    # elif spriteA_X + spriteA_size < spriteB_X:
    else:
        max_distance = spriteA_size

    if distance <= max_distance:
        return True
    return False


# Init
pygame.init()
mixer.init(48000)
mixer.music.set_volume(0.4)

# Window Size
WIN_WIDTH = 800
WIN_HEIGHT = 600

# Game FPS
FPS = 60

# Player Constant
PLAYER_SIZE = 64
PLAYER_VEL = 7

# Enemy
# Enemy vel tidak ada karena akan ditambah seiring waktu
ENEMY_SIZE = PLAYER_SIZE
ENEMY_Y_VEL = 64
ENEMY_VEL_INCREASE = 0.005
NUM_OF_ENEMIES = 6

# Bullet Constant
BULLET_SIZE = 20
BULLET_VEL = 12

# Import
BG = pygame.transform.smoothscale(
    pygame.image.load("assets/spaceBackground.png"),
    (WIN_WIDTH, WIN_HEIGHT))
ICON = pygame.image.load("assets/icon.png")
PLAYER_IMG = pygame.transform.smoothscale(
    pygame.image.load("assets/spaceship.png"),
    (PLAYER_SIZE, PLAYER_SIZE))
BULLET_IMG = pygame.transform.smoothscale(
    pygame.image.load("assets/bullet.png"),
    (BULLET_SIZE, BULLET_SIZE))
ENEMY_IMG_CHOICE = (pygame.transform.smoothscale(
    pygame.image.load("assets/enemy1.png"),
    (ENEMY_SIZE, ENEMY_SIZE)), pygame.transform.smoothscale(
    pygame.image.load("assets/enemy2.png"),
    (ENEMY_SIZE, ENEMY_SIZE)))
ENEMY_IMG = tuple([random.choice(ENEMY_IMG_CHOICE)
                   for _ in range(NUM_OF_ENEMIES)])
GLOBAL_FONT = 'assets/pixel_font.ttf'
BS = mixer.music.load('assets/backsound.wav')
BULLET_SOUND = mixer.Sound('assets/laser.wav')
BULLET_SOUND.set_volume(0.2)
COLLISION_SOUND = mixer.Sound('assets/explosion.wav')
COLLISION_SOUND.set_volume(0.15)

# Font
SCORE_FONT = pygame.font.Font(GLOBAL_FONT, 32)
GAME_OVER_FONT = pygame.font.Font(GLOBAL_FONT, 112)
INFO_FONT = pygame.font.Font(GLOBAL_FONT, 40)
ENTER_FONT = pygame.font.Font(GLOBAL_FONT, 32)
ALERT_FONT = pygame.font.Font(GLOBAL_FONT, 40)

# Alert
ALERT_TIME = 2

# FPS clock
clock = pygame.time.Clock()

# Main window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space Shooting Game")
pygame.display.set_icon(ICON)

# Player Coordinates
# Player starting point
playerX = (WIN_WIDTH / 2) - PLAYER_SIZE
playerY = (WIN_HEIGHT * 0.75)

# Bullet Variable
bulletX = -BULLET_SIZE * 10
bulletY = -BULLET_SIZE * 10
isShooting = False

# Enemy
enemyVel = PLAYER_VEL * 0.75
isEnemyMoveLeft = [random.choice((True, False)) for _ in range(NUM_OF_ENEMIES)]
isEnemyMoveUp = [False for _ in range(NUM_OF_ENEMIES)]
# Enemy coordinates
# Enemy starting point
enemyX = [random.randint(0, WIN_WIDTH - ENEMY_SIZE)
          for _ in range(NUM_OF_ENEMIES)]
enemyY = [
    random.randint(0, (WIN_HEIGHT * 0.25) - ENEMY_SIZE)
    for _ in range(NUM_OF_ENEMIES)]

# Score
score_count = 0

# Game over
isGameOver = False
# Info
isInfo = True  # For infoloop
# Alert
isAlert = True  # For alertloop
# Mainloop
running = True
while running:
    # Game FPS set
    clock.tick(FPS)

    # Infoloop
    if isInfo:
        for event in pygame.event.get():
            # Closing action
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Continue action
                if event.key == pygame.K_RETURN:
                    isInfo = False
                    finish_dt = (datetime.datetime.now()
                                 + datetime.timedelta(seconds=ALERT_TIME))
    # Alertloop
    elif isAlert:
        for event in pygame.event.get():
            # Closing action
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Continue action
                if event.key == pygame.K_RETURN:
                    isAlert = False
                    # Play background music
                    mixer.music.play(-1)
        if datetime.datetime.now() > finish_dt:
            isAlert = False
            # Play background music
            mixer.music.play(-1)
    # Gameloop
    # Closing action
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not (isShooting or isGameOver):
                # Player shoot action
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        isShooting = True
                        # Play shooting sound effect
                        BULLET_SOUND.play()
                        # Set the bullet start coordinates
                        bulletX = playerX + (PLAYER_SIZE / 2) - (BULLET_SIZE / 2)
                        bulletY = playerY - BULLET_SIZE

        if not isGameOver:
            # Player moving action
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                playerX -= PLAYER_VEL
            if keys[pygame.K_RIGHT]:
                playerX += PLAYER_VEL
            if keys[pygame.K_UP]:
                playerY -= PLAYER_VEL
            if keys[pygame.K_DOWN]:
                playerY += PLAYER_VEL

            # Player Borders
            if playerX < 0:
                playerX = 0
            elif playerX > WIN_WIDTH - PLAYER_SIZE:
                playerX = WIN_WIDTH - PLAYER_SIZE
            if playerY < WIN_HEIGHT / 2:  # Up border
                playerY = WIN_HEIGHT / 2
            elif playerY > WIN_HEIGHT - PLAYER_SIZE:
                playerY = WIN_HEIGHT - PLAYER_SIZE

            # Enemy move
            for i in range(NUM_OF_ENEMIES):
                if isEnemyMoveLeft[i]:
                    enemyX[i] -= enemyVel
                else:  # Moving right
                    enemyX[i] += enemyVel
                # Enemy borders
                # Left border
                if enemyX[i] <= 0:
                    enemyX[i] = 0
                    isEnemyMoveLeft[i] = False
                    # Moving down or up
                    if isEnemyMoveUp[i]:
                        enemyY[i] -= ENEMY_Y_VEL
                    else:
                        enemyY[i] += ENEMY_Y_VEL
                # Right border
                elif enemyX[i] >= WIN_WIDTH - ENEMY_SIZE:
                    enemyX[i] = WIN_WIDTH - ENEMY_SIZE
                    isEnemyMoveLeft[i] = True
                    # Moving down or up
                    if isEnemyMoveUp[i]:
                        enemyY[i] -= ENEMY_Y_VEL
                    else:
                        enemyY[i] += ENEMY_Y_VEL
                # Up border
                if enemyY[i] <= 0:
                    enemyY[i] = 0
                    isEnemyMoveUp[i] = False
                # Down border
                elif enemyY[i] >= WIN_HEIGHT - ENEMY_SIZE:
                    enemyY[i] = WIN_HEIGHT - ENEMY_SIZE
                    isEnemyMoveUp[i] = True
            # Increase the enemy vel
            enemyVel += ENEMY_VEL_INCREASE

            # Moving player bullet
            if isShooting:
                bulletY -= BULLET_VEL
                # Bullet border
                if bulletY < 0 - BULLET_SIZE:
                    bulletY = -BULLET_SIZE * 10
                    isShooting = False

            # Collision
            for i in range(NUM_OF_ENEMIES):
                # Enemy and bullet collision
                if isCollision(
                        enemyX[i],
                        enemyY[i],
                        ENEMY_SIZE, bulletX, bulletY, BULLET_SIZE):
                    # Play collision sound
                    COLLISION_SOUND.play()
                    # Reset bullet coordinates
                    bulletX = -BULLET_SIZE * 10
                    bulletY = -BULLET_SIZE * 10
                    # Disappearing the bullet
                    isShooting = False

                    # Reset enemy coordinates
                    enemyX[i] = random.randint(0, WIN_WIDTH - ENEMY_SIZE)
                    enemyY[i] = random.randint(
                        0, (WIN_HEIGHT * 0.25) - ENEMY_SIZE)
                    # Reset enemy directions
                    isEnemyMoveLeft[i] = random.choice((True, False))
                    isEnemyMoveUp[i] = False

                    # Increase player score
                    score_count += 1
                # Player collision
                elif isCollision(enemyX[i], enemyY[i], ENEMY_SIZE, playerX, playerY, PLAYER_SIZE):
                    isGameOver = True
                    # Turn off background music
                    mixer.music.stop()
                    # Play collision sound
                    COLLISION_SOUND.play()
                    # pick the enemy number to still showed
                    enemy_collision_num = i
                    # Stop the collision for loop
                    break
    redraw_window()
