import pygame

# Clase de la Casa (Decoración)
class House:
    def __init__(self, width, height):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/casa.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=(width - 100, height))

# Clase del Árbol (Decoración)
class Tree:
    def __init__(self, x, y):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/arbol.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
