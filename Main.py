import pygame
import time
from Classes import Screen, Player, Bullet

pygame.init()

win = pygame.display.set_mode((500, 500), 0, 0)
pygame.display.set_caption("JourneyOfThePrairieKing")

# Class instances
playerSprite = Player()
gameScreen = Screen()

# Initial sprite and animation variables
spriteMain = playerSprite.idle[0]  # Set the initial sprite
animationSpeed = 100  # Speed of animation (milliseconds)
lastUpdate = pygame.time.get_ticks()  # Get the initial time
walkCount = 0  # Initialize walkCount
playerHitbox = pygame.Rect(playerSprite.x + 20, playerSprite.y + 35, playerSprite.width - 10, playerSprite.height - 10)
playerAnimationState = "idle"  # Initialize playerAnimationState

def createWalls():
    # Create Rect objects for the walls and store them in variables
    left = pygame.Rect(0, 0, 10, 500)
    top = pygame.Rect(0, 0, 500, 10)
    bottom = pygame.Rect(0, 490, 500, 10)
    right = pygame.Rect(490, 0, 10, 500)

    return left, top, bottom, right

def redrawGameWindow():
    global walkCount, bullets
    win.blit(gameScreen.bg, (0, 0))  # Blit the background first

    left, top, bottom, right = createWalls()

    pygame.draw.rect(win, (84, 80, 69), left)
    pygame.draw.rect(win, (84, 80, 69), top)
    pygame.draw.rect(win, (84, 80, 69), bottom)
    pygame.draw.rect(win, (84, 80, 69), right)

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()  # Update bullet position
        bullet.draw(win)  # Draw bullet on the screen

    playerHitbox = pygame.Rect(playerSprite.x + 20, playerSprite.y + 35, playerSprite.width - 10, playerSprite.height - 10)
    pygame.draw.rect(win, (255, 0, 0), playerHitbox, 2)  # Red outline
    win.blit(spriteMain, (playerSprite.x, playerSprite.y))  # Blit the player sprite
    pygame.display.update()  # Update the display


def updateAnimation(currentTime):
    global walkCount, lastUpdate, playerAnimationState, spriteMain

    # Check if it's time to update the animation frame
    if currentTime - lastUpdate >= animationSpeed:
        lastUpdate = currentTime

        # Default sprite when not moving
        spriteMain = playerSprite.idle[walkCount % len(playerSprite.idle)]
        playerAnimationState = "idle"

        if keys[pygame.K_a]:  # Moving left
            spriteMain = playerSprite.leftIdle[walkCount % len(playerSprite.leftIdle)]
            playerAnimationState = "walk"
        elif keys[pygame.K_d]:  # Moving right
            spriteMain = playerSprite.move[walkCount % len(playerSprite.move)]
            playerAnimationState = "walk"
        elif keys[pygame.K_w] or keys[pygame.K_s]:  # Moving up or down
            spriteMain = playerSprite.move[walkCount % len(playerSprite.move)]
            playerAnimationState = "walk"

        # Increment the walkCount for the next frame
        walkCount += 1



right = False
left = False 

# Set boundaries
screenWidth = 500
screenHeight = 500

# Define the borderWidth (how close to the edge the player can get)
borderWidth = 5  

# Create a list to store bullets
bullets = []

lastShotTime = 0
run = True
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    currentTime = pygame.time.get_ticks()

    # Calculate the center of the player's hitbox
    centerX = playerSprite.x + playerSprite.width // 2
    centerY = playerSprite.y + playerSprite.height // 2

    keys = pygame.key.get_pressed()
    left, top, bottom, right = createWalls()

    nextX = playerSprite.x
    nextY = playerSprite.y

    if keys[pygame.K_a]:
        nextX -= playerSprite.vel
        playerAnimationState = "walk"
    elif keys[pygame.K_d]:
        nextX += playerSprite.vel
        playerAnimationState = "walk"

    if keys[pygame.K_w]:
        nextY -= playerSprite.vel
    elif keys[pygame.K_s]:
        nextY += playerSprite.vel

    nextPlayerHitbox = pygame.Rect(nextX + 20, nextY + 35, playerSprite.width - 10, playerSprite.height - 10)

    if not nextPlayerHitbox.colliderect(left) and not nextPlayerHitbox.colliderect(right):
        playerSprite.x = nextX

    if not nextPlayerHitbox.colliderect(top) and not nextPlayerHitbox.colliderect(bottom):
        playerSprite.y = nextY

    if keys[pygame.K_a]:
        left = True
        right = False
    elif keys[pygame.K_d]:
        left = False
        right = True
    else:
        left = False
        right = False

    bulletDirection = (0, 0)

    if keys[pygame.K_LEFT]:
        bulletDirection = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        bulletDirection = (1, 0)
    if keys[pygame.K_UP]:
        bulletDirection = (0, -1)
    elif keys[pygame.K_DOWN]:
        bulletDirection = (0, 1)

    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        bulletDirection = (-1, -1)
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        bulletDirection = (-1, 1)
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        bulletDirection = (1, -1)
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        bulletDirection = (1, 1)

    timeSinceLastShot = currentTime - lastShotTime

    if timeSinceLastShot >= 250 and bulletDirection != (0, 0):
        startX = centerX + 10
        startY = centerY + 20
        newBullet = Bullet(startX, startY, bulletDirection)
        bullets.append(newBullet)
        lastShotTime = currentTime

    bullets = [bullet for bullet in bullets if bullet.y > 0]

    win.fill((0, 0, 0))
    win.blit(gameScreen.bg, (0, 0))

    # Update the animation
    updateAnimation(currentTime)

    win.blit(spriteMain, (playerSprite.x, playerSprite.y))
    redrawGameWindow()

pygame.quit()