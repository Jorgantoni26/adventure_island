import pygame
import random
import sys

# Configuración inicial
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1300, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Island")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clase del jugador
class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/personaje.png"), (40, 40))
        self.rect = self.image.get_rect(topleft=(50, HEIGHT - 80))  
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

            if self.rect.y >= HEIGHT - 80:
                self.rect.y = HEIGHT - 80
                self.is_jumping = False
                self.velocity_y = 0

    def reset_position(self):
        self.rect.topleft = (50, HEIGHT - 80)

# Función para mostrar la pantalla de inicio
def show_start_screen():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text  # Devuelve el nombre ingresado
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Mensaje de bienvenida
        welcome_surface = font.render("Bienvenido a Adventure Island!", True, BLACK)
        text_rect = welcome_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(welcome_surface, text_rect)

        start_surface = font.render("Presiona Enter para comenzar", True, BLACK)
        start_rect = start_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(start_surface, start_rect)

        pygame.display.flip()

# Clase estrella
class Collectible:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/estrella.png"), (25, 25))
        self.rect = self.image.get_rect(center=position)
        self.collected = False

# Clase del diamante
class Diamond:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/diamante.png"), (30, 30))
        self.rect = self.image.get_rect(center=position)
        self.collected = False  

# Clase del árbol
class Tree:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/arbol.png"), (50, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

# Clase del caracol (obstáculo)
class Snail:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/caracol.png"), (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.direction *= -1

# Clase de la casa
class House:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/casa.png"), (100, 100)) 
        self.rect = self.image.get_rect(topleft=(WIDTH - 150, HEIGHT - 100))

# Clase del pájaro (obstáculo)
class Bird:
    def __init__(self, y):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/pajaro.png"), (40, 30))
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH), y))
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width

# Clase de la piedra (obstáculo)
class Rock:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/piedra.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

# Función para mostrar puntos y vidas en la pantalla
def display_score_and_lives(score, lives, player_image, time_left):
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Puntos: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    for i in range(lives):
        screen.blit(player_image, (WIDTH - 50 - (i * 50), 10))

    timer_surface = font.render(f"Tiempo: {time_left // 1000}", True, (0, 0, 0))
    screen.blit(timer_surface, (WIDTH // 2 - 50, 10))

# Función para mostrar el cartel de Game Over
def display_game_over():
    font = pygame.font.Font(None, 74)
    game_over_surface = font.render("GAME OVER", True, BLACK)
    text_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_surface, text_rect)

# Función para mostrar el cartel de Victoria
def display_victory():
    font = pygame.font.Font(None, 74)
    victory_surface = font.render("¡HAS GANADO!", True, BLACK)
    text_rect = victory_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(victory_surface, text_rect)

# Función principal del juego
def main():
    player_name = show_start_screen()  # Captura el nombre del jugador
    clock = pygame.time.Clock()
    player = Player()
    house = House()

    # Posiciones fijas para las estrellas
    star_positions = [
        (100, HEIGHT - 50),
        (400, HEIGHT - 80),
        (650, HEIGHT - 50),
        (1000, HEIGHT - 50)
    ]
    collectibles = [Collectible(pos) for pos in star_positions]

    # Crear diamantes en posiciones específicas en el cielo
    diamond_positions = [
        (200, 100),
        (800, 100)   
    ]
    diamonds = [Diamond(pos) for pos in diamond_positions]

    # Crear árboles fijos en posiciones específicas
    trees = [
        Tree(1000, HEIGHT - 130),
        Tree(300, HEIGHT - 130),
        Tree(500, HEIGHT - 130),
        Tree(700, HEIGHT - 130)
    ]

    # Crear caracoles (obstáculos)
    snails = [Snail(600, HEIGHT - 70), Snail(200, HEIGHT - 70)]
    
    # Crear pájaros (obstáculos)
    birds = [Bird(50), Bird(100), Bird(150)]

    # Crear piedras (obstáculos)
    rocks = [Rock(300, HEIGHT - 80), Rock(700, HEIGHT - 80)]

    score = 0
    lives = 3
    start_ticks = pygame.time.get_ticks()  # Para el temporizador

    while True:
        time_passed = pygame.time.get_ticks() - start_ticks
        time_left = 30000 - time_passed  # 30 segundos
        if time_left <= 0:
            display_game_over()
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_SPACE]:
            player.jump()

        player.update()

        # Detección de colisiones con estrellas
        for collectible in collectibles:
            if collectible.rect.colliderect(player.rect) and not collectible.collected:
                collectible.collected = True
                score += 1

        # Detección de colisiones con diamantes
        for diamond in diamonds:
            if diamond.rect.colliderect(player.rect):
                diamonds.remove(diamond)
                score += 3  

        # Detección de colisiones con obstáculos
        for snail in snails:
            if snail.rect.colliderect(player.rect):
                lives -= 1
                player.reset_position()
                if lives <= 0:
                    display_game_over()
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    pygame.quit()
                    sys.exit()

        for bird in birds:
            if bird.rect.colliderect(player.rect):
                lives -= 1
                player.reset_position()
                if lives <= 0:
                    display_game_over()
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    pygame.quit()
                    sys.exit()

        # Actualizar caracoles y pájaros
        for snail in snails:
            snail.update()
        
        for bird in birds:
            bird.update()

        # Dibujar todo
        screen.fill(SKY_BLUE)

        # Dibujar elementos en la pantalla
        for collectible in collectibles:
            if not collectible.collected:
                screen.blit(collectible.image, collectible.rect)
        for diamond in diamonds:
            screen.blit(diamond.image, diamond.rect)

        for tree in trees:
            screen.blit(tree.image, tree.rect)
        
        for snail in snails:
            screen.blit(snail.image, snail.rect)

        for bird in birds:
            screen.blit(bird.image, bird.rect)

        for rock in rocks:
            screen.blit(rock.image, rock.rect)

        screen.blit(player.image, player.rect)
        screen.blit(house.image, house.rect)

        # Mostrar puntaje y vidas
        display_score_and_lives(score, lives, player.image, time_left)

        # Mostrar mensaje de victoria si se recolectan todos los diamantes
        if not diamonds:
            display_victory()
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
