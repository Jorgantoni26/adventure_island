import pygame
import sys
from jugador.jugador import Player
from objetos.coleccionables import Collectible, Diamond
from objetos.obstaculos import Snail, Bird, Rock
from decorativos.decorativos import House, Tree
from funciones.escenario import show_start_screen, display_score_and_lives, display_game_over, display_victory
import time
import sqlite3

# Registra el tiempo de inicio al comienzo del juego
start_time = time.time()
# Al finalizar la partida (cuando el jugador gana)
end_time = time.time()
elapsed_time = end_time - start_time  # Tiempo en segundos

# Guardar puntaje junto con el tiempo transcurrido
def save_score(name, score, elapsed_time):
    conn = sqlite3.connect("ADVENTURE.ISLAND.db")
    cursor = conn.cursor()

    # Verificar si el puntaje merece estar en el Top 10
    cursor.execute("SELECT COUNT(*) FROM ranking")
    count = cursor.fetchone()[0]

    if count < 10:
        # Si hay menos de 10 registros, agregar el nuevo puntaje
        cursor.execute("INSERT INTO ranking (nombre_jugador, puntaje, tiempo) VALUES (?, ?, ?)", (name, score, elapsed_time))
    else:
        # Si hay 10 registros, verificar si el nuevo puntaje es mejor que el último
        cursor.execute("SELECT id, puntaje, tiempo FROM ranking ORDER BY puntaje ASC, tiempo DESC LIMIT 1")
        worst_score_id, worst_score, worst_time = cursor.fetchone()

        if score > worst_score or (score == worst_score and elapsed_time < worst_time):
            # Elimina el puntaje más bajo y agrega el nuevo puntaje
            cursor.execute("DELETE FROM ranking WHERE id = ?", (worst_score_id,))
            cursor.execute("INSERT INTO ranking (nombre_jugador, puntaje, tiempo) VALUES (?, ?, ?)", (name, score, elapsed_time))

    conn.commit()
    conn.close()

def display_top_10(screen):
    conn = sqlite3.connect("ADVENTURE.ISLAND.db")
    cursor = conn.cursor()

    # Selecciona el Top 10 en orden descendente de puntaje
    cursor.execute("SELECT nombre_jugador, puntaje, tiempo FROM ranking ORDER BY puntaje DESC, tiempo ASC LIMIT 10")
    top_scores = cursor.fetchall()
    conn.close()

    # Configuración para mostrar el texto en pantalla
    font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))  # Limpia la pantalla

    # Muestra los primeros 5 jugadores en la primera columna
    y_offset = 50
    for index in range(5):
        if index < len(top_scores):
            name, score, elapsed_time = top_scores[index]
            text = f"{index + 1}. {name} - Puntaje: {score} - Tiempo: {int(elapsed_time)}s"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 40

    # Muestra los siguientes 5 jugadores en la segunda columna
    y_offset = 50
    for index in range(5, 10):
        if index < len(top_scores):
            name, score, elapsed_time = top_scores[index]
            text = f"{index + 1}. {name} - Puntaje: {score} - Tiempo: {int(elapsed_time)}s"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (600, y_offset))  # Ajusta aquí la posición x de la segunda columna
            y_offset += 40

    pygame.display.flip()
    pygame.time.delay(2000)

def run_game():
    pygame.init()

    # Configuración de pantalla
    WIDTH, HEIGHT = 1300, 250
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adventure Island")

    # Pantalla de inicio y elección del jugador
    action, player_name = show_start_screen(screen, WIDTH, HEIGHT)
    
    # Verifica si el jugador quiere ver el ranking antes de iniciar el juego
    if action == "view_ranking":
        display_top_10(screen)  # Muestra el ranking
        pygame.time.delay(5000)  # Pausa para visualizar el ranking
        action, player_name = show_start_screen(screen, WIDTH, HEIGHT)  # Regresa a la pantalla de inicio después de ver el ranking

    # Solo continúa si la acción es iniciar el juego
    if action != "start_game":
        return 

    # Variables de juego
    score = 0
    lives = 3

    # Configuración inicial de objetos del juego
    clock = pygame.time.Clock()
    player = Player()
    house = House(WIDTH, HEIGHT)  # Instancia la casa con los valores de ancho y alto
    collectibles = [Collectible(pos) for pos in [(100, HEIGHT - 50), (400, HEIGHT - 80), (650, HEIGHT - 50), (1000, HEIGHT - 50)]]
    diamonds = [Diamond(pos) for pos in [(200, 100), (800, 100)]]
    trees = [Tree(1000, HEIGHT - 60), Tree(380, HEIGHT - 60)]
    snails = [Snail(600, HEIGHT - 30), Snail(200, HEIGHT - 30)]
    birds = [Bird(50), Bird(100)]
    rocks = [Rock(300, HEIGHT - 30), Rock(600, HEIGHT - 30), Rock(900, HEIGHT - 30), Rock(450, HEIGHT - 30)]
    start_ticks = pygame.time.get_ticks()  #para parar el temporizador

    while True:
        time_passed = pygame.time.get_ticks() - start_ticks
        time_left = 15000 - time_passed  # 30 segundos
        if time_left <= 0:
            display_game_over(screen)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        
        # Verificar si el jugador ha perdido o ganado
        if lives <= 0:
            display_game_over(screen)
            pygame.display.flip()
            pygame.time.delay(3000)
            break
        # Detectar colisión con la casa para ganar el juego
        if player.rect.colliderect(house.rect):
            end_time = time.time()
            elapsed_time = end_time - start_time
            save_score(player_name, score, elapsed_time)
            display_victory(screen)
            pygame.display.flip()
            pygame.time.delay(3000)
            display_top_10(screen)
            break

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

        # Detectar colisiones con obstáculos y reducir vidas
        for snail in snails:
            if player.rect.colliderect(snail.rect):
                lives -= 1
                player.reset_position()

        for bird in birds:
            if player.rect.colliderect(bird.rect):
                lives -= 1
                player.reset_position()

        for rock in rocks:
            if player.rect.colliderect(rock.rect):
                player.reset_position()

        # Detectar colisiones con coleccionables y sumar puntos
        for collectible in collectibles:
            if player.rect.colliderect(collectible.rect) and not collectible.collected:
                collectible.collected = True
                score += 10
                print("¡Estrella obtenida! Puntos:", score)

        for diamond in diamonds:
            if player.rect.colliderect(diamond.rect) and not diamond.collected:
                diamond.collected = True
                score += 20
                print("¡Diamante obtenido! Puntos:", score)

        # Dibuja todos los elementos en la pantalla
        screen.fill((135, 206, 235))

        # Dibuja la casa
        screen.blit(house.image, house.rect)
        for tree in trees:
            tree.draw(screen)

        # Dibuja cada coleccionable si no ha sido recogido
        for collectible in collectibles:
            if not collectible.collected:
                screen.blit(collectible.image, collectible.rect)

        for diamond in diamonds:
            if not diamond.collected:
                screen.blit(diamond.image, diamond.rect)

        # Dibuja cada obstáculo
        for snail in snails:
            snail.update()
            screen.blit(snail.image, snail.rect)

        for bird in birds:
            bird.update()
            screen.blit(bird.image, bird.rect)

        for rock in rocks:
            screen.blit(rock.image, rock.rect)

        # Dibuja el jugador
        screen.blit(player.image, player.rect)

        # Dibuja el puntaje y las vidas
        display_score_and_lives(screen, score, lives, HEIGHT)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_game()
