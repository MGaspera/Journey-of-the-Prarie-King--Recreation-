import pygame
from Classes import PlayerInfo, Anim
pygame.init()

win = pygame.display.set_mode((500, 500))
# This line creates a window of 500 width, 500 height

#Class Instances
playerMaths = PlayerInfo() 
gameAnim = Anim()

pygame.display.set_caption("Journey of the Prarie King")

def redrawGameWindow():
    global walkCount
    
    win.blit(gameAnim.bg, (0,0))  



run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and playerMaths.x > playerMaths.vel:
        playerMaths.x -= playerMaths.vel
        left = True
        right = False

    if keys[pygame.K_RIGHT] and playerMaths.x < 500 - playerMaths.vel - playerMaths.width:
        playerMaths.x += playerMaths.vel
        left = False
        right = True

    if keys[pygame.K_UP] and playerMaths.y > playerMaths.vel:
        playerMaths.y -= playerMaths.vel

    if keys[pygame.K_DOWN] and playerMaths.y < 500 - playerMaths.height - playerMaths.vel:
        playerMaths.y += playerMaths.vel
    
    redrawGameWindow()

pygame.quit()  # If we exit the loop this will execute and close our game