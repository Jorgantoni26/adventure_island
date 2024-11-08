import pygame


WIDTH, HEIGHT = 1300, 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))
class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/personaje.png"), (40, 40))
        self.rect = self.image.get_rect(topleft=(50, 250 - 60))
        self.speed = 5
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.velocity_y = 0

    def move(self, dx):
        self.rect.x += dx * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_speed

    def update(self):
        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity

            if self.rect.y >= HEIGHT - 60:
                self.rect.y = HEIGHT - 60
                self.is_jumping = False
                self.velocity_y = 0

    def reset_position(self):
        self.rect.topleft = (50, HEIGHT - 60)


    
    
    def check_victory(self, house):
        return self.rect.colliderect(house.rect)