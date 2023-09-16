import pygame
import time
from Classes import screen, player, bullet as Bullet
pygame.init()

win = pygame.display.set_mode((500, 500), 0, 0)

pygame.display.set_caption("Journey of the Prairie King")

# Class Instances
sprite = player()
gameScreen = screen()

# Initial sprite and animation variables
spriteMain = sprite.idle[0]  # Set the initial sprite
animation_speed = 100  # Speed of animation (milliseconds)
last_update = pygame.time.get_ticks()  # Get the initial time
walkCount = 0  # Initialize walkCount

def redrawGameWindow():
    global walkCount, bullets
    win.blit(gameScreen.bg, (0, 0))  # Blit the background first

    # Draw left border rectangle
    pygame.draw.rect(win, (84, 80, 69), (0, 0, 10, 500))
    # Draw top border rectangle
    pygame.draw.rect(win, (84, 80, 69), (0, 0, 500, 10))
    # Draw bottom border rectangle
    pygame.draw.rect(win, (84, 80, 69), (0, 490, 500, 10))
    # Draw right border rectangle
    pygame.draw.rect(win, (84, 80, 69), (490, 0, 10, 500))

    # Update and draw bullets
    for bullet in bullets:
        bullet.update()  # Update bullet position
        bullet.draw(win)  # Draw bullet on the screen

    playerHitbox = pygame.Rect(sprite.x + 20, sprite.y + 35, sprite.width - 10, sprite.height - 10)
    pygame.draw.rect(win, (255, 0, 0), playerHitbox, 2)  # Red outline
    win.blit(spriteMain, (sprite.x, sprite.y))  # Blit the player sprite
    pygame.display.update()  # Update the display

right = False
left = False 

# Set boundaries
screen_width = 500
screen_height = 500

# Define the border width (how close to the edge the player can get)
border_width = 5  

# Create a list to store bullets
bullets = []

lastShotTime = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get the current time
    currentTime = pygame.time.get_ticks()

    # Check if it's time to update the animation frame
    if currentTime - last_update >= animation_speed:
        last_update = currentTime

        # Update the animation frame based on the direction (left or right)
        if right:
            spriteMain = sprite.idle[walkCount % len(sprite.idle)]
        elif left:
            spriteMain = sprite.leftIdle[walkCount % len(sprite.leftIdle)]

        # Increment the walkCount for the next frame
        walkCount += 1

    keys = pygame.key.get_pressed()

    # Player movement logic with adjusted boundaries
    if keys[pygame.K_a]:
        sprite.x -= sprite.vel
        left = True
        right = False

    if keys[pygame.K_d]:
        sprite.x += sprite.vel
        left = False
        right = True

    if keys[pygame.K_w]:
        sprite.y -= sprite.vel

    if keys[pygame.K_s]:
        sprite.y += sprite.vel

    bullet_direction = (0, 0)

    if keys[pygame.K_LEFT]:
        bullet_direction = (-1, 0)  # Move left
    elif keys[pygame.K_RIGHT]:
        bullet_direction = (1, 0)  # Move right

    if keys[pygame.K_UP]:
        bullet_direction = (0, -1)  # Move up
    elif keys[pygame.K_DOWN]:
        bullet_direction = (0, 1)  # Move down

    # Combine horizontal and vertical directions for diagonal movement
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        bullet_direction = (-1, -1)  # Move up-left
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        bullet_direction = (-1, 1)  # Move down-left
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        bullet_direction = (1, -1)  # Move up-right
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        bullet_direction = (1, 1)  # Move down-right

    # Calculate the time elapsed since the last shot
    time_since_last_shot = currentTime - lastShotTime

    # If enough time has passed (250 milliseconds) and there's a direction, allow the player to shoot
    if time_since_last_shot >= 250 and bullet_direction != (0, 0):
        # Create a new bullet with the current direction
        new_bullet = Bullet(sprite.x + sprite.width // 2 + 5, sprite.y + sprite.height // 2 + 5, bullet_direction)
        bullets.append(new_bullet)

        # Update the time of the last shot
        lastShotTime = currentTime

    # Update bullets
    for bullet in bullets:
        bullet.update()

    # Remove bullets that are out of bounds
    bullets = [bullet for bullet in bullets if bullet.y > 0]  # Adjust the condition as needed

    # Clear the screen
    win.fill((0, 0, 0))

    # Blit the background
    win.blit(gameScreen.bg, (0, 0))

    # Blit the player sprite
    win.blit(spriteMain, (sprite.x, sprite.y))

    # Update the display
    redrawGameWindow()

pygame.quit()
