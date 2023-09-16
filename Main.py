import pygame
from Classes import PlayerInfo, Anim
pygame.init()

# Set display dimensions and create the window
win_width, win_height = 500, 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Journey of the Prarie King")

# Class Instances
playerMaths = PlayerInfo()
gameAnim = Anim()

# Initial sprite and animation variables
spriteMain = gameAnim.idle[0]  # Set the initial sprite
animation_speed = 100  # Speed of animation (milliseconds)
last_update = pygame.time.get_ticks()  # Get the initial time
walkCount = 0  # Initialize walkCount

right = False
left = False 

# Set boundaries
screen_width = 500
screen_height = 500

# Define the border width (how close to the edge the player can get)
border_width = 5  # You can adjust this value as needed

def redrawGameWindow():
    global walkCount
    win.blit(gameAnim.bg, (0, 0))  # Blit the background first
    win.blit(spriteMain, (playerMaths.x, playerMaths.y))  # Blit the player sprite
    pygame.display.update()  # Update the display

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Check if it's time to update the animation frame
    if current_time - last_update >= animation_speed:
        last_update = current_time

        # Update the animation frame based on the direction (left or right)
        if right:
            spriteMain = gameAnim.idle[walkCount % len(gameAnim.idle)]
        elif left:
            spriteMain = gameAnim.leftIdle[walkCount % len(gameAnim.leftIdle)]

        # Increment the walkCount for the next frame
        walkCount += 1

    keys = pygame.key.get_pressed()

    # Player movement logic with adjusted boundaries
    if keys[pygame.K_LEFT]:
        playerMaths.x -= playerMaths.vel
        left = True
        right = False

    if keys[pygame.K_RIGHT]:
        playerMaths.x += playerMaths.vel
        left = False
        right = True

    if keys[pygame.K_UP]:
        playerMaths.y -= playerMaths.vel

    if keys[pygame.K_DOWN]:
        playerMaths.y += playerMaths.vel

    # Boundary checks to prevent the player from going out of the screen
    if playerMaths.x < border_width:
        playerMaths.x = border_width

    if playerMaths.x > win_width - playerMaths.width - border_width:
        playerMaths.x = win_width - playerMaths.width - border_width

    if playerMaths.y < border_width:
        playerMaths.y = border_width

    if playerMaths.y > win_height - playerMaths.height - border_width:
        playerMaths.y = win_height - playerMaths.height - border_width

    # Clear the screen
    win.fill((0, 0, 0))

    # Blit the background
    win.blit(gameAnim.bg, (0, 0))

    # Draw rectangles
    for i in range(0, win_width, 10):
        pygame.draw.rect(win, (255, 0, 0), (i, i, 10, 10), 1)

    # Blit the player sprite
    win.blit(spriteMain, (playerMaths.x, playerMaths.y))

    print("coords:", playerMaths.x, playerMaths.y)

    # Update the display
    pygame.display.update()

pygame.quit()
