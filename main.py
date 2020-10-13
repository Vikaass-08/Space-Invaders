# ctrl + alt + l  == reformat the code
import pygame
from pygame import mixer
import random
import math

# initialize py_game
pygame.init()

# Display Screen with width = 800 & height = 600
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title & Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370  # Initial position along x axis
playerY = 480  # Initial position along y axis
playerX_change = 0  # Change along x-axis

# Score
score_value = 0  # Player score
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 0
textY = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))  # Initial position along x axis
    enemyY.append(random.randint(20, 100))  # Initial position along y axis
    enemyX_change.append(2)  # Change along x-axis
    enemyY_change.append(40)  # Change along y-axis

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0  # Initial position along x axis
bulletY = 480  # Initial position along y axis
bulletX_change = 0  # Change along x-axis
bulletY_change = 10  # Change along y-axis
# Ready state means you can't see the bullet on the screen
# Fire state means bullet is currently moving
bullet_state = "ready"

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over = over_font.render("GAME OVER", True, (250, 255, 250))
    screen.blit(over, (200, 250))


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (250, 255, 250))
    screen.blit(score, (x, y))


def player(x, y):
    # Draw the player on the screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    # Draw the player on the screen
    screen.blit(enemyImg[index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return True if distance < 27 else False


def reset(index):
    global bullet_state, bulletY, enemyX, enemyY
    bullet_state = "ready"
    bulletY = 480
    enemyX[index] = random.randint(0, 735)  # Initial position along x axis
    enemyY[index] = random.randint(20, 100)  # Initial position along y axis


# Event = Any action that takes place inside the display screen is an event
running = True

# This will keep the display screen open until running = True
while running:
    # RGB background color
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystrokes is pressed check whether it's left or right
        # Key-down is for key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        # key-up is for pressed key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # To keep  player inside the bounds
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(no_of_enemies):
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            score_value += 1
            reset(i)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)  # show current score on screen
    pygame.display.update()  # Constantly updating the screen
