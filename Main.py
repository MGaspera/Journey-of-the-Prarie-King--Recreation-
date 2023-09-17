import pygame
import time
import random
from Classes import Screen, Player, Bullet, Enemy

# Initialize pygame
pygame.init()

# Create the game window
win = pygame.display.set_mode((500, 500), 0, 0)
pygame.display.set_caption("JourneyOfThePrairieKing")


ENEMY_SPAWN_MIN_INTERVAL = 125  # 1/8th of a second (in milliseconds)
ENEMY_SPAWN_MAX_INTERVAL = 500  # 1/2 of a second (in milliseconds)
ENEMY_START_X = random.randint(0, 500 - 55)  # Initial x-coordinate for off-screen spawning
ENEMY_START_Y = random.randint(0, 500 - 55)  # Initial y-coordinate (random within screen height)
ENEMY_PURSUE_DISTANCE = 100  # Distance from the player to start pursuing
ENEMY_MOVE_SPEED = 2  # Speed at which enemies move
lastEnemySpawnTime = pygame.time.get_ticks()



# Create instances of the game objects
playerSprite = Player()  # Player character
gameScreen = Screen()    # Game screen background
enemies = []
playerHitbox = pygame.Rect(playerSprite.x + 20, playerSprite.y + 35, playerSprite.width - 10, playerSprite.height - 10)

# Initial sprite and animation variables
spriteMain = playerSprite.idle[0]  # Set the initial sprite
animationSpeed = 100  # Speed of animation (milliseconds)
lastUpdate = pygame.time.get_ticks()  # Get the initial time
animationTimer = pygame.time.get_ticks()
walkCount = 0  # Initialize walkCount
playerAnimationState = "idle"  # Initialize playerAnimationState

# Function to create wall Rect objects
def createWalls():
    # Create Rect objects for the walls and store them in variables
    left = pygame.Rect(0, 0, 10, 500)
    top = pygame.Rect(0, 0, 500, 10)
    bottom = pygame.Rect(0, 490, 500, 10)
    right = pygame.Rect(490, 0, 10, 500)

    return left, top, bottom, right

# Function to redraw the game window
def redrawGameWindow():
    global walkCount, bullets
    win.blit(gameScreen.bg, (0, 0))  # Blit the background first

    left, top, bottom, right = createWalls()

    pygame.draw.rect(win, (84, 80, 69), left)
    pygame.draw.rect(win, (84, 80, 69), top)
    pygame.draw.rect(win, (84, 80, 69), bottom)
    pygame.draw.rect(win, (84, 80, 69), right)

    # Draw a green rectangle around the player to represent the no-spawn zone
    # no_spawn_rect = pygame.Rect(playerSprite.x - 100, playerSprite.y - 100, 200, 200)
    # pygame.draw.rect(win, (0, 255, 0), no_spawn_rect, 2)  # Green outline

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()  # Update bullet position
        bullet.draw(win)  # Draw bullet on the screen

    # Draw BoD enemies and handle death animations
    for enemy in enemies:
        if enemy.alive:
            if enemy.direction == 1:
                win.blit(enemy.images[walkCount % len(enemy.images)], (enemy.x, enemy.y))
            else:
                win.blit(enemy.left_images[walkCount % len(enemy.left_images)], (enemy.x, enemy.y))
        else:
            if walkCount // 10 < len(enemy.death_images):
                win.blit(enemy.death_images[walkCount // 10], (enemy.x, enemy.y))
            else:
                enemies.remove(enemy)



    win.blit(spriteMain, (playerSprite.x, playerSprite.y))  # Blit the player sprite
    pygame.display.update()  # Update the display


def updateAnimation():
    global playerAnimationState, spriteMain, animationTimer, walkCount, keys

    # Calculate the time passed since the last animation frame change
    currentTime = pygame.time.get_ticks()
    timePassed = currentTime - animationTimer

    # Debug output to check playerAnimationState
    #print(f"Player Animation State: {playerAnimationState}")

    # Check if it's time to update the animation frame
    if timePassed >= animationSpeed:
        animationTimer = currentTime  # Reset the animation timer

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




# Initialize movement flags
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

# Constants for frame rate and time step
FPS = 60
TIME_STEP = 1000 / FPS  # Time step in milliseconds

# Main game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # Check collision between bullet and enemies
        for enemy in enemies:
            if enemy.alive and playerHitbox.colliderect(enemy.rect):
                bullet.kill()  # Remove the bullet
                enemy.die()    # Mark the enemy as dead


    #print(type(playerHitbox))
    #print(type(Enemy))


    # Player-enemy collision detection
    for enemy in enemies:
        if enemy.alive:
            enemy.pursue_player(playerSprite.x, playerSprite.y)
            if enemy.direction == 1:
                win.blit(enemy.images[walkCount % len(enemy.images)], (enemy.x, enemy.y))
            else:
                win.blit(enemy.left_images[walkCount % len(enemy.left_images)], (enemy.x, enemy.y))
        else:
            if enemy.death_animation_frame < len(enemy.death_images):
                win.blit(enemy.death_images[enemy.death_animation_frame], (enemy.x, enemy.y))
                enemy.death_animation_frame += 1
            else:
                enemies.remove(enemy)

    # Calculate time passed since the last frame
    currentTime = pygame.time.get_ticks()
    deltaTime = currentTime - lastUpdate
    lastUpdate = currentTime

    # Calculate the center of the player's hitbox
    centerX = playerSprite.x + playerSprite.width // 2
    centerY = playerSprite.y + playerSprite.height // 2

    keys = pygame.key.get_pressed()
    left, top, bottom, right = createWalls()

    nextX = playerSprite.x
    nextY = playerSprite.y

    # Handle player movement
    if keys[pygame.K_a]:
        nextX -= playerSprite.vel * deltaTime / TIME_STEP
        playerAnimationState = "walk"
    elif keys[pygame.K_d]:
        nextX += playerSprite.vel * deltaTime / TIME_STEP
        playerAnimationState = "walk"

    if keys[pygame.K_w]:
        nextY -= playerSprite.vel * deltaTime / TIME_STEP
    elif keys[pygame.K_s]:
        nextY += playerSprite.vel * deltaTime / TIME_STEP

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

    # Handle shooting in different directions
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

    # Create bullets based on the player's input and shooting cooldown
    if timeSinceLastShot >= 250 and bulletDirection != (0, 0):
        startX = centerX + 10
        startY = centerY + 20
        newBullet = Bullet(startX, startY, bulletDirection)
        bullets.append(newBullet)
        lastShotTime = currentTime

    # Remove bullets that have gone off-screen
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Spawn BoD enemies
    if currentTime - lastEnemySpawnTime >= random.randint(ENEMY_SPAWN_MIN_INTERVAL, ENEMY_SPAWN_MAX_INTERVAL):
        ENEMY_START_X = random.randint(0, 500 - 55)
        ENEMY_START_Y = random.randint(0, 500 - 55)
        newEnemy = Enemy(57, 55, "./Assets/Enemies/BoD/Walk", "./Assets/Enemies/BoD/Death", ENEMY_MOVE_SPEED, "BoDWalk", "BoDeath", ENEMY_START_X, ENEMY_START_Y)
        enemies.append(newEnemy)
        lastEnemySpawnTime = currentTime  # Update the last spawn time



    # Update BoD enemy behavior
    for enemy in enemies:
        if enemy.alive:
            if enemy.direction == 1:
                win.blit(enemy.images[walkCount % len(enemy.images)], (enemy.x, enemy.y))
            else:
                win.blit(enemy.left_images[walkCount % len(enemy.left_images)], (enemy.x, enemy.y))
        else:
            if enemy.death_animation_frame < len(enemy.death_images):
                win.blit(enemy.death_images[enemy.death_animation_frame], (enemy.x, enemy.y))
                enemy.death_animation_frame += 1
            else:
                enemies.remove(enemy)


    # Clear the screen and update the animation
    win.fill((0, 0, 0))
    win.blit(gameScreen.bg, (0, 0))
    updateAnimation()
    win.blit(spriteMain, (playerSprite.x, playerSprite.y))

    # Draw BoD enemies and handle death animations
    for enemy in enemies:
        if enemy.alive:
            if enemy.direction == 1:
                win.blit(enemy.images[walkCount % len(enemy.images)], (enemy.x, enemy.y))
            else:
                win.blit(enemy.left_images[walkCount % len(enemy.left_images)], (enemy.x, enemy.y))
        else:
            if walkCount // 10 < len(enemy.death_images):
                win.blit(enemy.death_images[walkCount // 10], (enemy.x, enemy.y))
            else:
                enemies.remove(enemy)

    redrawGameWindow()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit pygame when the game loop exits
pygame.quit()
