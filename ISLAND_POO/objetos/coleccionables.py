import pygame

# Clase de Coleccionable (General)
class Collectible:
    def __init__(self, position):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/estrella.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=position)
        self.collected = False

# Clase del Diamante (Coleccionable Especial)
class Diamond:
    def __init__(self, position):
        self.image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/diamante.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=position)
        self.collected = False
