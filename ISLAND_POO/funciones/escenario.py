import pygame
import sys

# Función para mostrar la pantalla de inicio

HEIGHT= 250

def show_start_screen(screen, WIDTH, HEIGHT):
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False
    font = pygame.font.Font(None, 36)
    
    # Crear botón para "Ver Ranking"
    ranking_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activa o desactiva la caja de texto
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                
                # Detecta clic en botón de "Ver Ranking"
                if ranking_button.collidepoint(event.pos):
                    return "view_ranking", None  # Retorna acción para mostrar el ranking

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return "start_game", text  # Devuelve la acción y el nombre ingresado
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Limpia la pantalla y configura el fondo
        screen.fill((255, 255, 255))

        # Muestra el texto dentro de la caja de entrada
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Mensaje de bienvenida
        welcome_surface = font.render("Bienvenido a Adventure Island!", True, (0, 0, 0))
        text_rect = welcome_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(welcome_surface, text_rect)

        # Instrucción para comenzar
        start_surface = font.render("Presiona Enter para comenzar", True, (0, 0, 0))
        start_rect = start_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(start_surface, start_rect)

        # Dibujar el botón de "Ver Ranking"
        pygame.draw.rect(screen, (128, 0, 128), ranking_button)
        ranking_text = font.render("Ver Ranking", True, (255, 255, 255))
        screen.blit(ranking_text, (ranking_button.x + 25, ranking_button.y + 10))

        # Actualiza la pantalla
        pygame.display.flip()

# Función para mostrar el puntaje y las vidas
def display_score_and_lives(screen, score, lives, time_left):
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Puntos: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))
    
    for i in range(lives):
        player_image = pygame.image.load("C:/Users/jorga/Downloads/Adventure island/island/personaje.png")
        player_image = pygame.transform.scale(player_image, (30, 30))
        screen.blit(player_image, (1300 - 50 - (i * 50), 10))

    timer_surface = font.render(f"Tiempo: {time_left // 1000}", True, (0, 0, 0))  # Convertir milisegundos a segundos
    screen.blit(timer_surface, (600, 10))  # Centrar el temporizador

    

# Función para mostrar Game Over
def display_game_over(screen):
    font = pygame.font.Font(None, 74)
    game_over_surface = font.render("GAME OVER", True, (0, 0, 0))
    text_rect = game_over_surface.get_rect(center=(1300 // 2, 250 // 2))
    screen.blit(game_over_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# Función para mostrar Victoria
def display_victory(screen):
    font = pygame.font.Font(None, 74)
    victory_surface = font.render("¡HAS GANADO!", True, (0, 0, 0))
    text_rect = victory_surface.get_rect(center=(1300 // 2, 250 // 2))
    screen.blit(victory_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)



