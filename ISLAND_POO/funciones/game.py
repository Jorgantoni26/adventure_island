import pygame
import sys
from jugador.jugador import Player
from objetos.coleccionables import Collectible ,Diamond
from objetos.obstaculos import Tree, Snail, Bird, Rock
from decorativos.decorativos import House  
from funciones.escenario import show_start_screen

# Función principal del juego
def run_game():
    pygame.init()

    # Configuración de pantalla
    WIDTH, HEIGHT = 1300, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adventure Island")

    screen = show_start_screen(screen, WIDTH, HEIGHT)
    clock  = pygame.time.Clock()
    player = Player()

    # Crea todos los objetos del juego
    house = House(WIDTH, HEIGHT)  # Instancia la casa con los valores de ancho y alto
    collectibles = [Collectible(pos) for pos in [(100, HEIGHT - 50), (400, HEIGHT - 80), (650, HEIGHT - 50), (1000, HEIGHT - 50)]]
    diamond = [Diamond(pos) for pos in [(200, 100), (800, 100)]]
    trees = [Tree(1000, HEIGHT - 130), Tree(300, HEIGHT - 130)]
    snail = [Snail(600, HEIGHT - 70), Snail(200, HEIGHT - 70)]
    bird = [Bird(50), Bird(100)]
    rock = [Rock(300, HEIGHT - 80)]

    # Loop del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Actualiza el jugador y otros elementos del juego
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_SPACE]:
            player.jump()

        player.update()

        # Dibuja todos los elementos en la pantalla
        screen.fill((135, 206, 235))  # Color del cielo

        # Dibuja la casa
        screen.blit(house.image, house.rect)

        # Dibuja cada objeto en pantalla
        for collectible in collectibles:
            if not collectible.collected:
                screen.blit(collectible.image, collectible.rect)

        pygame.display.flip()
        clock.tick(60)
