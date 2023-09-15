import pygame
import os

class PlayerInfo():
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.vel = 5

class Anim():
    def __init__(self):
        self.walk= [pygame.image.load(os.path.join("./Assets/Necro/Move/", f'Move ({i}).png')) for i in range(1, 22)]
        self.death= [pygame.image.load(os.path.join("./Assets/Necro/Death/", f'Death ({i}).png')) for i in range(1, 10)]
        self.idle= [pygame.image.load(os.path.join("./Assets/Necro/Idle/", f'Idle ({i}).png')) for i in range(1, 9)]
        self.ult= [pygame.image.load(os.path.join("./Assets/Necro/Ult/", f'Ult ({i}).png')) for i in range(1, 14)]
        self.bg = pygame.image.load(os.path.join("./Assets/Bg", f'Ground.jpg'))