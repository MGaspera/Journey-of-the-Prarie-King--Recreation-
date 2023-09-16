import pygame
from Classes import PlayerInfo, Anim
pygame.init()

win = pygame.display.set_mode((500, 500), 0, 0)

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
left = False  # Initialize left to False

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
    if playerMaths.x < 0:
        playerMaths.x = 0

    if playerMaths.x > screen_width - playerMaths.width:
        playerMaths.x = screen_width - playerMaths.width

    if playerMaths.y < 0:
        playerMaths.y = 0

    if playerMaths.y > screen_height - playerMaths.height:
        playerMaths.y = screen_height - playerMaths.height

    # Clear the screen
    win.fill((0, 0, 0))

    # Blit the background
    win.blit(gameAnim.bg, (0, 0))

    # Draw rectangles
    for i in range(0, 1000, 10):
        pygame.draw.rect(win, (255, 0, 0), (i, i, 10, 10), 1)

    # Blit the player sprite
    win.blit(spriteMain, (playerMaths.x, playerMaths.y))

    print ("coords:", playerMaths.x, playerMaths.y)

    # Update the display
    pygame.display.update()

pygame.quit()
