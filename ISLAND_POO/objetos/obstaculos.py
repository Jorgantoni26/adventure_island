import pygame
import random

# Clase del Caracol (Obstáculo)
class Snail:
    def __init__(self, x, y):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/caracol.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        screen_width = pygame.display.get_surface().get_width()
    
    # Rebotar cuando llegue a un borde
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed = -self.speed  # Cambia de dirección

# Clase del Pájaro (Obstáculo)
class Bird:
    def __init__(self, y):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/pajaro.png"), (40, 30))
        self.rect = self.image.get_rect(topleft=(random.randint(0, pygame.display.get_surface().get_width()), y))
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > pygame.display.get_surface().get_width():
            self.rect.x = -self.rect.width

# Clase de la Piedra (Obstáculo)
class Rock:
    def __init__(self, x, y):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/piedra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
