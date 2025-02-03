#########################################
# Programmer: Ori Dembo
# Date: 21/11/2021
# File Name: snake_template.py
# Description: A Snake Game implementation in Pygame.
#             The player controls a snake that grows by eating apples.
#             Features both normal and hard modes with different mechanics.
#########################################
#fix timer for in game 
# Required imports
import pygame
from math import sqrt
pygame.init()
from random import randint
from random import randrange
from time import sleep

# Initialize font
font = pygame.font.SysFont("Ariel Black", 40)

# Window setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)      # Used for button pressed state
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)    # Used for button pressed state
YELLOW = (255, 255, 0)
ORANGE = (255, 102, 0)
BLUE = (0, 0, 255)
BROWN = (26, 9, 0)
outline = 0

# Game state variables
dlay = 60                   # Game speed/delay
timechange = True           # Flag for time-based difficulty changes
score = 0
time = 20                   # Initial time limit

# UI Button configurations
# Info button positioned in top right
rectX, rectY, rectW, rectH = WIDTH - 150, 50, 100, 50  
# Start button positioned in bottom middle
cirX, cirY, cirR = WIDTH // 2, HEIGHT - 100, 50  
# Hard mode button positioned in top left
hardX, hardY, hardW, hardH = 50, 50, 100, 50  

# Button state trackers
info_pressed = False
start_pressed = False
hard_pressed = False

# Calculate distance between two points
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

################ Snake Configuration ################

# Snake size and movement constants
BODY_SIZE = 10
HSPEED = 20                 # Horizontal movement speed
VSPEED = 20                 # Vertical movement speed

# Initial movement direction (starts moving up)
speedX = 0
speedY = -VSPEED

# Initialize snake with 3 segments at starting position
segx = [int(WIDTH / 2.)] * 3
segy = [HEIGHT - 5, HEIGHT + VSPEED, HEIGHT + 2 * VSPEED]

# Initialize food positions with spacing from edges
foodX = randrange(20, WIDTH - 20, BODY_SIZE)
BadfoodX = randrange(20, WIDTH - 20, BODY_SIZE)
foodY = randrange(20, HEIGHT - 20, BODY_SIZE)
BadfoodY = randrange(20, HEIGHT - 20, BODY_SIZE)

# Saw configuration
sawX = randrange(20, WIDTH - 20)
sawY = 20
sawSpeed = 5
sawMovingDown = True

# Game mode and direction tracking
hardMode = False
lastDirection = "UP"        # Used for proper body segment orientation

################ Asset Loading ################

# Load and configure background images
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

# Load and configure audio
pygame.mixer.music.load("images/snakeTheme.wav")
pygame.mixer.music.set_volume(0.5)
appleSound = pygame.mixer.Sound("images/apple.wav")
badappleSound = pygame.mixer.Sound("images/SNAKEYUCK.wav")
appleSound.set_volume(0.8)
badappleSound.set_volume(0.8)
gameOverSound = pygame.mixer.Sound("images/SnakeGameOverSound.wav")
gameOverSound.set_volume(0.8)

# Load snake head images for each direction
snakeHL = pygame.image.load("images/snakeHeadLeft.png")
snakeHR = pygame.image.load("images/SnakeHeadRight.png")
snakeHU = pygame.image.load("images/SnakeHeadUp.png")
snakeHD = pygame.image.load("images/snakeHeadDown.png")
snakeBY = pygame.image.load("images/snakeBodyD.png")

# Load saw image
saw = pygame.image.load("images/saw.png")
saw = pygame.transform.scale(saw, (BODY_SIZE + 20, BODY_SIZE + 20))

# Scale snake head images to proper size
snakeHR = pygame.transform.scale(snakeHR, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHL = pygame.transform.scale(snakeHL, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHU = pygame.transform.scale(snakeHU, (BODY_SIZE + 20, BODY_SIZE + 20))
snakeHD = pygame.transform.scale(snakeHD, (BODY_SIZE + 20, BODY_SIZE + 20))
SL = snakeHU                # Initial head direction

# Load and scale UI and gameplay images
infoBTTN = pygame.image.load("images/info.png")
infoBTTN = pygame.transform.scale(infoBTTN, (BODY_SIZE + 50, BODY_SIZE + 50))

snakeBY = pygame.transform.scale(snakeBY, (BODY_SIZE + 10, BODY_SIZE + 10))

apple = pygame.image.load("images/apple.png")
Badapple = pygame.image.load("images/badapple.png")
apple = pygame.transform.scale(apple, (BODY_SIZE + 20, BODY_SIZE + 20))
Badapple = pygame.transform.scale(Badapple, (BODY_SIZE + 20, BODY_SIZE + 20))

################ Game Screen Functions ################

def endGameScreen():
    """Display game over screen with final score"""
    screen.blit(backgroundEnd, (0, 0))
    endTxt2 = font.render('your score was:' + str(score), 1, YELLOW)
    screen.blit(endTxt2, (305, HEIGHT // 2 + 100))
    pygame.display.update()

def startGameScreen():
    """Display start screen with interactive buttons"""
    screen.blit(backgroundStart, (0, 0))
    
    # Draw info button
    screen.blit(infoBTTN, (rectX, rectY))
    
    # Draw start button with pressed state visual feedback
    circle_color = DARK_RED if start_pressed else RED
    pygame.draw.circle(screen, circle_color, (cirX, cirY), cirR, 0)
    startTxt = font.render('START', 1, BLACK)
    screen.blit(startTxt, (cirX - 45, cirY - 15))
    
    # Draw hard mode toggle with active/pressed state indication
    hard_color = DARK_GREEN if hard_pressed or hardMode else GREEN
    pygame.draw.rect(screen, hard_color, (hardX, hardY, hardW, hardH))
    hardTxt = font.render('Hard Mode', 1, BLACK)
    screen.blit(hardTxt, (hardX + 5, hardY + 10))
    
    pygame.display.update()

def instructionsScreen():
    """Display game instructions screen"""
    screen.blit(backgroundINFO, (0, 0))
    pygame.display.update()

def redraw():
    """Update game display with current state"""
    screen.blit(backgroundGame, (0, 0))
    
    # Draw snake head at current position
    screen.blit(SL, (segx[0] - 15, segy[0] - 15))
    
    # Draw food items
    screen.blit(apple, (foodX - 20, foodY - 20))
    if hardMode:
        screen.blit(Badapple, (BadfoodX - 20, BadfoodY - 20))
        screen.blit(saw, (sawX - 20, sawY - 20))

    # Draw score and remaining time
    scoretxt = font.render('score:' + str(score), 1, WHITE)
    timeleft = font.render('time left:' + str(timeLeft), 1, WHITE)
    screen.blit(scoretxt, (10, 550))
    screen.blit(timeleft, (630, 550))

    # Draw snake body segments with correct orientation
    for i in range(1, len(segx)):
            screen.blit(snakeBY, (segx[i] - 10, segy[i] - 10))
            
    pygame.display.update()

################ Game Loop Sections ################

# Start screen loop
introScreen = True
showRules = False
while introScreen:
    for event in pygame.event.get():
        # Handle game exit
        if event.type == pygame.QUIT:
            introScreen = False
            gameOver = False
            inPlay = False
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            
            # Handle info button click
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
            
            # Handle hard mode toggle
            if mouseX > hardX and mouseX < hardX + hardW and mouseY > hardY and mouseY < hardY + hardH:
                hard_pressed = True
                hardMode = not hardMode
                pygame.time.delay(100)  # Visual feedback delay
                hard_pressed = False
            
            # Handle start button click
            if distance(mouseX, mouseY, cirX, cirY) < cirR:
                start_pressed = True
                pygame.time.delay(100)  # Visual feedback delay
                introScreen = False
                starttime = pygame.time.get_ticks() // 1000
                
        # Reset button states on mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            info_pressed = False
            start_pressed = False
                
    startGameScreen()

################ Main Game Loop ################

inPlay = True
resetTime = pygame.time.get_ticks() // 1000

# Start background music when game begins
if inPlay:
    pygame.mixer.music.play(loops=-1)

print("Use the arrows to control the snake.")
while inPlay:
    # Handle game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            gameOver = False
            pygame.quit()
            exit()

    continuousTime = pygame.time.get_ticks() // 1000
    keys = pygame.key.get_pressed()
    
    # Handle directional input and update snake head orientation
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

    # Screen wrapping in normal mode
    if not hardMode:
        if segx[0] < 0: segx[0] = WIDTH
        if segy[0] < 0: segy[0] = HEIGHT
        if segx[0] > WIDTH: segx[0] = 0
        if segy[0] > HEIGHT: segy[0] = 0

    # Check for snake self-collision
    for i in range(1, len(segx)):
        if segx[0] == segx[i] and segy[0] == segy[i]:
            if hardMode:
                gameOverSound.play()
                endGameScreen()
                pygame.time.delay(2000)
            inPlay = False
            gameOver = True

    # Handle good apple collection
    if distance(foodX, foodY, segx[0], segy[0]) < 25:
        foodX = randrange(20, WIDTH - 20, BODY_SIZE)
        foodY = randrange(20, HEIGHT - 20, BODY_SIZE)
        segx.append(segx[-1])
        segy.append(segy[-1])
        score += 1
        timechange = True
        resetTime = pygame.time.get_ticks() // 1000
        appleSound.play()

    # Update time remaining
    elapsed = continuousTime - resetTime
    timeLeft = abs(elapsed - 20)

    # Check if timer ran out
    if timeLeft == 0:
        resetTime = pygame.time.get_ticks() // 1000
        segx.pop()
        segy.pop()
        score -= 1
        badappleSound.play()

    # Increase game speed at score milestones
    if score in (5, 20, 30, 40) and timechange:
        dlay -= 10
        timechange = False

    # Hard mode specific mechanics
    if hardMode:
        # Move saw up and down
        if sawMovingDown:
            sawY += sawSpeed
            if sawY >= HEIGHT - 20:
                sawMovingDown = False
        else:
            sawY -= sawSpeed
            if sawY <= 20:
                sawMovingDown = True

        # Check for saw collision
        if distance(sawX, sawY, segx[0], segy[0]) < 20:
            gameOverSound.play()
            endGameScreen()
            pygame.time.delay(2000)
            inPlay = False
            gameOver = True

        # Game over conditions for hard mode
        if (score == -2 and distance(BadfoodX, BadfoodY, segx[0], segy[0]) < 20) or timeLeft == 0:
            gameOverSound.play()
            endGameScreen()
            pygame.time.delay(2000)
            inPlay = False
            gameOver = True

        # No screen wrapping in hard mode
        if segx[0] < 0 or segx[0] > WIDTH or segy[0] < 0 or segy[0] > HEIGHT:
            gameOverSound.play()
            endGameScreen()
            pygame.time.delay(2000)
            inPlay = False
            gameOver = True

        # Handle bad apple collection
        if distance(BadfoodX, BadfoodY, segx[0], segy[0]) < 20:
            BadfoodX = randrange(20, WIDTH - 20, BODY_SIZE)
            BadfoodY = randrange(20, HEIGHT - 20, BODY_SIZE)
            timechange = False
            segx.pop()
            segy.pop()
            score -= 1
            badappleSound.play()

    # Update snake segment positions
    for i in range(len(segx) - 1, 0, -1):
        segx[i] = segx[i - 1]
        segy[i] = segy[i - 1]
        
    # Update snake head position
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY
    
    redraw()
    pygame.time.delay(dlay)

################ Game Over Loop ################
