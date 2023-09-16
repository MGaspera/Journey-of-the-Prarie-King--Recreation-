import pygame
import os
import math



class player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 30
        self.height = 50
        self.vel = 0.1

        self.walk= [pygame.image.load(os.path.join("./Assets/Necro/Move/", f'Move-({i}).png')) for i in range(1, 22)]
        self.death= [pygame.image.load(os.path.join("./Assets/Necro/Death/", f'Death-({i}).png')) for i in range(1, 10)]
        self.idle= [pygame.image.load(os.path.join("./Assets/Necro/Idle/", f'Idle-({i}).png')) for i in range(1, 9)]
        self.ult= [pygame.image.load(os.path.join("./Assets/Necro/Ult/", f'Ult-({i}).png')) for i in range(1, 14)]

        self.leftIdle = [pygame.transform.flip(image, True, False) for image in self.idle]

    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False):
            pass

class screen():
    def __init__(self):
        self.bg = pygame.image.load(os.path.join("./Assets/Bg", f'Ground.jpg'))

class bullet:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 0.1
        self.direction = direction
        self.rotation_angle = 0  # Initial rotation angle
        self.original_image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Create a transparent surface for the bullet
        pygame.draw.polygon(self.original_image, (99, 10, 4), [(10, 0), (0, 20), (20, 20)])  # Create a triangular bullet
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Move the bullet in the specified direction
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]
        self.rect.center = (self.x, self.y)

        # Rotate the bullet (you can adjust the rotation speed by changing the angle increment)
        self.rotation_angle += 0.1  # Adjust the rotation speed here

        # Rotate the bullet image
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)

    def draw(self, win):
        win.blit(self.image, self.rect)
