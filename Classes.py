import pygame
import os
import random

# Define the Enemy class
class Enemy:
    def __init__(self, width, height, image_folder_walk, image_folder_death, speed, walkAssetName, deathAssetName, start_x, start_y):
        self.width = width
        self.height = height
        self.images = [pygame.image.load(os.path.join(image_folder_walk, f'{walkAssetName}-({i}).png')) for i in range(1, 9)]
        self.death_images = [pygame.image.load(os.path.join(image_folder_death, f'{deathAssetName}-({i}).png')) for i in range(1, 11)]
        self.left_images = [pygame.transform.flip(image, True, False) for image in self.images]
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.direction = 1
        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.death_animation_frame = 0
        self.pursuing = False  # Initialize pursuing flag

    def wandering(self):
        pass


    def pursue_player(self, player_x, player_y):
            ENEMY_PURSUE_DISTANCE = 100
            if not self.pursuing:
                if abs(self.x - player_x) <= ENEMY_PURSUE_DISTANCE:
                    self.pursuing = True
            if self.pursuing:
                if self.x < player_x:
                    self.direction = 0.8
                else:
                    self.direction = -0.8
                self.x += self.speed * self.direction

                # Move vertically towards the player's y-coordinate
                if self.y < player_y:
                    self.direction = 0.8
                else:
                    self.direction = -0.8
                self.y += self.speed * self.direction


# Subclass: Bringer of Death
class BoD(Enemy):
    def __init__(self):
        super().__init__(width=57,
                         height=55,
                         image_folder_walk="./Assets/Enemies/BoD/Walk",
                         image_folder_death="./Assets/Enemies/BoD/Death",
                         deathAssetName="BoDeath",
                         walkAssetName="BoDWalk",
                         speed=3)


# Define the Player class
class Player:
    def __init__(self):
        self.x = 0  # Initial x-coordinate
        self.y = 0  # Initial y-coordinate
        self.width = 30  # Width of the player character
        self.height = 50  # Height of the player character
        self.vel = 3 # Velocity for player movement

        # Lists of player character images for different animations
        self.idle = [pygame.image.load(os.path.join("./Assets/Necro/Idle/", f'Idle-({i}).png')) for i in range(1, 17)]
        self.death = [pygame.image.load(os.path.join("./Assets/Necro/Death/", f'Death-({i}).png')) for i in range(1, 10)]
        self.move = [pygame.image.load(os.path.join("./Assets/Necro/Move/", f'Move-({i}).png')) for i in range(1, 9)]
        self.leftIdle = [pygame.transform.flip(image, True, False) for image in self.idle]  # Flipped idle images

    # Function to handle collision with other sprite groups (not implemented yet)
    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False):
            pass

# Define the Screen class
class Screen:
    def __init__(self):
        # Load the game screen background image
        self.bg = pygame.image.load(os.path.join("./Assets/Bg", f'Ground.jpg'))

# Define the Bullet class
class Bullet:
    # Define constants for bullet directions
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    def __init__(self, x, y, direction):
        self.x = x  # Initial x-coordinate of the bullet
        self.y = y  # Initial y-coordinate of the bullet
        self.speed = 5  # Speed of the bullet
        self.direction = direction  # Initial direction of the bullet
        self.rotationAngle = 0  # Initial rotation angle of the bullet
        self.originalImage = pygame.Surface((20, 20), pygame.SRCALPHA)  # Create a transparent surface for the bullet
        pygame.draw.polygon(self.originalImage, (200, 10, 4), [(10, 0), (0, 20), (20, 20)])  # Create a triangular bullet
        self.image = self.originalImage  # Initialize the bullet image
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Get the bullet's rect for positioning
        

    def update(self):
        # Move the bullet in the specified direction
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]
        self.rect.center = (self.x, self.y)  # Update the bullet's position based on (x, y)

        # Rotate the bullet (you can adjust the rotation speed by changing the angle increment)
        self.rotationAngle += 0.1  # Adjust the rotation speed here

        # Rotate the bullet image
        self.image = pygame.transform.rotate(self.originalImage, self.rotationAngle)

    def draw(self, win):
        # Draw the bullet on the game window
        win.blit(self.image, self.rect)
