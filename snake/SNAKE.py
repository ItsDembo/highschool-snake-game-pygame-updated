#########################################
# Programmer: Ori Dembo
# Date: 21/11/2021
# File Name: snake_template.py
# Description: This program is a Snake Game.
#               It demonstrates how to move and lengthen the snake.
#########################################
import pygame
from math import sqrt

pygame.init()
from random import randint
from random import randrange

font = pygame.font.SysFont("Ariel Black", 40)
from time import sleep

# Window dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)  # Darker red for pressed state
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)  # Darker green for pressed state
YELLOW = (255, 255, 0)
ORANGE = (255, 102, 0)
BLUE = (0, 0, 255)
BROWN = (26, 9, 0)
outline = 0

# Game variables
dlay = 60
timechange = True
score = 0
time = 20

# Button dimensions and states
rectX, rectY, rectW, rectH = WIDTH - 150, 50, 100, 50  # Info button in top right
cirX, cirY, cirR = WIDTH // 2, HEIGHT - 100, 50  # Start button in bottom middle
hardX, hardY, hardW, hardH = 50, 50, 100, 50  # Hard mode button in top left
info_pressed = False
start_pressed = False
hard_pressed = False

# Helper function for distance calculation
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

##############       snake's properties    #####################

BODY_SIZE = 10
HSPEED = 20
VSPEED = 20

speedX = 0
speedY = -VSPEED

# Initialize snake segments
segx = [int(WIDTH / 2.)] * 3
segy = [HEIGHT - 5, HEIGHT + VSPEED, HEIGHT + 2 * VSPEED]

# Food positions
foodX = randrange(20, WIDTH - 20, BODY_SIZE)
BadfoodX = randrange(20, WIDTH - 20, BODY_SIZE)
foodY = randrange(20, HEIGHT - 20, BODY_SIZE)
BadfoodY = randrange(20, HEIGHT - 20, BODY_SIZE)

hardMode = False
lastDirection = "UP"  # Track last direction for proper body segment orientation

###############loading images and sounds #####################
backgroundEnd = pygame.image.load("images/GameOver.png")
backgroundEnd = pygame.transform.scale(backgroundEnd, (800, 600))
backgroundEnd = backgroundEnd.convert_alpha()

backgroundGame = pygame.image.load("images/snakebackground.jpg")
backgroundGame = pygame.transform.scale(backgroundGame, (800, 600))
backgroundGame = backgroundGame.convert_alpha()

backgroundStart = pygame.image.load("images/snakeGameStart.png")
backgroundStart = pygame.transform.scale(backgroundStart, (800, 600))
backgroundStart = backgroundStart.convert_alpha()

backgroundINFO = pygame.image.load("images/infoScreenSnake.png")
backgroundINFO = pygame.transform.scale(backgroundINFO, (800, 600))
backgroundINFO = backgroundINFO.convert_alpha()

# Load and set up sounds
pygame.mixer.music.load("images/snakeTheme.wav")
pygame.mixer.music.set_volume(0.5)
appleSound = pygame.mixer.Sound("images/apple.wav")
badappleSound = pygame.mixer.Sound("images/SNAKEYUCK.wav")
appleSound.set_volume(0.8)
badappleSound.set_volume(0.8)
gameOverSound = pygame.mixer.Sound("images/SnakeGameOverSound.wav")
gameOverSound.set_volume(0.8)

# Load snake head images
snakeHL = pygame.image.load("images/snakeHeadLeft.png")
snakeHR = pygame.image.load("images/SnakeHeadRight.png")
snakeHU = pygame.image.load("images/SnakeHeadUp.png")
snakeHD = pygame.image.load("images/snakeHeadDown.png")
snakeBY = pygame.image.load("images/snakeBodyD.png")
snakeBX = pygame.image.load("images/snakeBodyR.png")

# Scale snake head images
snakeHR = pygame.transform.scale(snakeHR, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHL = pygame.transform.scale(snakeHL, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHU = pygame.transform.scale(snakeHU, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHD = pygame.transform.scale(snakeHD, (BODY_SIZE + 20, BODY_SIZE + 20))
SL = snakeHU

# Load and scale other images
infoBTTN = pygame.image.load("images/info.png")
infoBTTN = pygame.transform.scale(infoBTTN, (BODY_SIZE + 50, BODY_SIZE + 50))

snakeBY = pygame.transform.scale(snakeBY, (BODY_SIZE + 10, BODY_SIZE + 10))
snakeBX = pygame.transform.scale(snakeBX, (BODY_SIZE + 10, BODY_SIZE + 10))

apple = pygame.image.load("images/apple.png")
Badapple = pygame.image.load("images/badapple.png")
apple = pygame.transform.scale(apple, (BODY_SIZE + 20, BODY_SIZE + 20))
Badapple = pygame.transform.scale(Badapple, (BODY_SIZE + 20, BODY_SIZE + 20))

##################                functions              ##########################

def endGameScreen():
    """Display game over screen with final score"""
    screen.blit(backgroundEnd, (0, 0))
    endTxt2 = font.render('your score was:' + str(score), 1, YELLOW)
    screen.blit(endTxt2, (305, HEIGHT // 2 + 100))
    pygame.display.update()

def startGameScreen():
    """Display start screen with buttons"""
    screen.blit(backgroundStart, (0, 0))
    
    # Draw buttons with pressed state colors
    screen.blit(infoBTTN, (rectX, rectY))
    
    # Start button color changes when pressed
    circle_color = DARK_RED if start_pressed else RED
    pygame.draw.circle(screen, circle_color, (cirX, cirY), cirR, 0)
    startTxt = font.render('START', 1, BLACK)
    screen.blit(startTxt, (cirX - 45, cirY - 15))
    
    # Hard mode button color changes when pressed or active
    hard_color = DARK_GREEN if hard_pressed or hardMode else GREEN
    pygame.draw.rect(screen, hard_color, (hardX, hardY, hardW, hardH))
    hardTxt = font.render('Hard Mode', 1, BLACK)
    screen.blit(hardTxt, (hardX + 5, hardY + 10))
    
    pygame.display.update()

def instructionsScreen():
    """Display instructions screen"""
    screen.blit(backgroundINFO, (0, 0))
    pygame.display.update()

def redraw():
    """Update game display"""
    screen.blit(backgroundGame, (0, 0))
    
    # Draw snake head
    screen.blit(SL, (segx[0] - 15, segy[0] - 15))
    
    # Draw food
    screen.blit(apple, (foodX - 20, foodY - 20))
    if hardMode:
        screen.blit(Badapple, (BadfoodX - 20, BadfoodY - 20))

    # Draw score and time
    scoretxt = font.render('score:' + str(score), 1, WHITE)
    timeleft = font.render('time left:' + str(timeLeft), 1, WHITE)
    screen.blit(scoretxt, (10, 550))
    screen.blit(timeleft, (630, 550))

    # Draw snake body with proper orientation
    for i in range(1, len(segx)):
        if lastDirection in ["LEFT", "RIGHT"]:
            screen.blit(snakeBX, (segx[i] - 10, segy[i] - 10))
        else:
            screen.blit(snakeBY, (segx[i] - 10, segy[i] - 10))
            
    pygame.display.update()

######################## INTRO & INSTRUCTION SECTION ##########################

introScreen = True
showRules = False
while introScreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            introScreen = False
            gameOver = False
            inPlay = False
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            
            # Info button
            if mouseX > rectX and mouseX < rectX + rectW and mouseY > rectY and mouseY < rectY + rectH:
                info_pressed = True
                showRules = True
                while showRules:
                    for event in pygame.event.get():
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LCTRL]:
                            showRules = False
                            info_pressed = False
                        if event.type == pygame.QUIT:
                            showRules = False
                            introScreen = False
                            gameOver = False
                            inPlay = False
                            pygame.quit()
                            exit()
                    instructionsScreen()
            
            # Hard mode button
            if mouseX > hardX and mouseX < hardX + hardW and mouseY > hardY and mouseY < hardY + hardH:
                hard_pressed = True
                hardMode = not hardMode  # Toggle hard mode
                pygame.time.delay(100)  # Brief delay to show pressed state
                hard_pressed = False
            
            # Start button
            if distance(mouseX, mouseY, cirX, cirY) < cirR:
                start_pressed = True
                pygame.time.delay(100)  # Brief delay to show pressed state
                introScreen = False
                starttime = pygame.time.get_ticks() // 1000
                
        if event.type == pygame.MOUSEBUTTONUP:
            info_pressed = False
            start_pressed = False
                
    startGameScreen()

########################          MAIN              ##########################

inPlay = True
resetTime = pygame.time.get_ticks() // 1000

if inPlay:
    pygame.mixer.music.play(loops=-1)

print("Use the arrows to control the snake.")
while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            gameOver = False
            pygame.quit()
            exit()

    continuousTime = pygame.time.get_ticks() // 1000
    keys = pygame.key.get_pressed()
    
    # Handle movement and update direction
    if keys[pygame.K_LEFT] and speedX == 0:
        speedX = -HSPEED
        speedY = 0
        SL = snakeHL
        lastDirection = "LEFT"

    if keys[pygame.K_RIGHT] and speedX == 0:
        speedX = HSPEED
        speedY = 0
        SL = snakeHR
        lastDirection = "RIGHT"

    if keys[pygame.K_UP] and speedY == 0:
        speedX = 0
        speedY = -VSPEED
        SL = snakeHU
        lastDirection = "UP"

    if keys[pygame.K_DOWN] and speedY == 0:
        speedX = 0
        speedY = VSPEED
        SL = snakeHD
        lastDirection = "DOWN"

    # Handle wrapping in normal mode
    if not hardMode:
        if segx[0] < 0: segx[0] = WIDTH
        if segy[0] < 0: segy[0] = HEIGHT
        if segx[0] > WIDTH: segx[0] = 0
        if segy[0] > HEIGHT: segy[0] = 0

    # Check for collision with self
    for i in range(1, len(segx)):
        if segx[0] == segx[i] and segy[0] == segy[i]:
            inPlay = False
            gameOver = True

    # Handle food collection
    if distance(foodX, foodY, segx[0], segy[0]) < 25:
        foodX = randrange(20, WIDTH - 20, BODY_SIZE)
        foodY = randrange(20, HEIGHT - 20, BODY_SIZE)
        segx.append(segx[-1])
        segy.append(segy[-1])
        score += 1
        timechange = True
        resetTime = pygame.time.get_ticks() // 1000
        appleSound.play()

    elapsed = continuousTime - resetTime
    timeLeft = abs(elapsed - 20)

    # Increase difficulty with score
    if score in (5, 10, 15, 20) and timechange:
        dlay -= 10
        timechange = False

    # Hard mode specific logic
    if hardMode:
        if (score == -2 and distance(BadfoodX, BadfoodY, segx[0], segy[0]) < 20) or timeLeft == 0:
            inPlay = False
            gameOver = True

        if segx[0] < 0 or segx[0] > WIDTH or segy[0] < 0 or segy[0] > HEIGHT:
            inPlay = False
            gameOver = True

        if distance(BadfoodX, BadfoodY, segx[0], segy[0]) < 20:
            BadfoodX = randrange(20, WIDTH - 20, BODY_SIZE)
            BadfoodY = randrange(20, HEIGHT - 20, BODY_SIZE)
            timechange = False
            if len(segx) > 3:  # Prevent snake from getting too short
                segx.pop()
                segy.pop()
            score -= 1
            badappleSound.play()

    # Move snake segments
    for i in range(len(segx) - 1, 0, -1):
        segx[i] = segx[i - 1]
        segy[i] = segy[i - 1]
        
    # Move head
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY
    
    redraw()
    pygame.time.delay(dlay)

####################### GAME OVER SECTION ###############################

if gameOver:
    gameOverSound.play()
    
while gameOver:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            introScreen = True
            gameOver = False
        if event.type == pygame.QUIT:
            gameOver = False
            pygame.quit()
            exit()
            
    pygame.mixer.music.stop()
    endGameScreen()
    pygame.time.delay(dlay)

pygame.quit()
