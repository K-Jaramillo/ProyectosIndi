import pygame
import sys
import random

# Inicialización de pygame
pygame.init()

# Definición de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")

# Variables del juego
velocidad = 5
jugador1_puntos = 0
jugador2_puntos = 0
contador_jugador1 = 0  # Contador de veces que el jugador 1 llega a 7 puntos
contador_jugador2 = 0  # Contador de veces que el jugador 2 llega a 7 puntos
reloj = pygame.time.Clock()
inicio = True  # Variable para controlar la pantalla de inicio
inversion_colores = False  # Variable para controlar la inversión de colores

# Raquetas
raqueta1 = pygame.Rect(50, ALTO // 2 - 70, 10, 140)
raqueta2 = pygame.Rect(ANCHO - 60, ALTO // 2 - 70, 10, 140)

# Bola
bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
bola_dx = velocidad * random.choice((1, -1))
bola_dy = velocidad * random.choice((1, -1))

# Función para dibujar la pantalla y objetos del juego
def dibujar():
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)  # Invertir colores si es necesario
    pygame.draw.rect(pantalla, NEGRO if not inversion_colores else BLANCO, raqueta1)
    pygame.draw.rect(pantalla, NEGRO if not inversion_colores else BLANCO, raqueta2)
    pygame.draw.ellipse(pantalla, NEGRO if not inversion_colores else BLANCO, bola)
    pygame.draw.aaline(pantalla, NEGRO if not inversion_colores else BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO))

    # Marcador
    fuente = pygame.font.Font(None, 20)

    # Contador de veces que se llega a 7 puntos
    contador_marcador1 = fuente.render(f"Rondas: {contador_jugador1}", True, NEGRO if not inversion_colores else BLANCO)
    contador_marcador2 = fuente.render(f"Rondas: {contador_jugador2}", True, NEGRO if not inversion_colores else BLANCO)
    pantalla.blit(contador_marcador1, (ANCHO // 4, 30))
    pantalla.blit(contador_marcador2, (2.8 * ANCHO // 4, 30))

    # Botón de inversión de colores
    pygame.draw.rect(pantalla, NEGRO, (ANCHO - 120, 10, 100, 40))
    fuente = pygame.font.Font(None, 24)
    texto_boton = fuente.render("Switch", True, BLANCO)
    pantalla.blit(texto_boton, (ANCHO - 110, 20))

    pygame.display.flip()

# Pantalla de inicio
def pantalla_inicio():
    pantalla.fill(BLANCO)
    fuente = pygame.font.Font(None, 30)
    texto = fuente.render("Presiona ESPACIO para comenzar", True, NEGRO)
    pantalla.blit(texto, (ANCHO // 4, ALTO // 2))
    pygame.display.flip()
    esperando_inicio = True
    while esperando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando_inicio = False

# Función para invertir los colores
def invertir_colores():
    global inversion_colores
    inversion_colores = not inversion_colores

# Función para mostrar la pantalla de reinicio
def pantalla_reinicio(ganador):
    pantalla.fill(BLANCO)
    fuente = pygame.font.Font(None, 30)
    texto = fuente.render(f"Jugador {ganador} ha ganado.", True, NEGRO)
    pantalla.blit(texto, (ANCHO // 4, ALTO // 2 - 20))
    texto2 = fuente.render("Presiona ESPACIO para reiniciar", True, NEGRO)
    pantalla.blit(texto2, (ANCHO // 4, ALTO // 2 + 10))
    pygame.display.flip()
    esperando_reinicio = True
    while esperando_reinicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reiniciar variables del juego
                global jugador1_puntos, jugador2_puntos, contador_jugador1, contador_jugador2, inicio
                jugador1_puntos = 0
                jugador2_puntos = 0
                contador_jugador1 = 0
                contador_jugador2 = 0
                inicio = True
                esperando_reinicio = False

# Bucle principal del juego
while True:
    if inicio:
        pantalla_inicio()
        inicio = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if ANCHO - 120 <= x <= ANCHO - 20 and 10 <= y <= 50:
                    invertir_colores()


    # Movimiento de raquetas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and raqueta1.top > 0:
        raqueta1.y -= velocidad
    if teclas[pygame.K_s] and raqueta1.bottom < ALTO:
        raqueta1.y += velocidad
    if teclas[pygame.K_UP] and raqueta2.top > 0:
        raqueta2.y -= velocidad
    if teclas[pygame.K_DOWN] and raqueta2.bottom < ALTO:
        raqueta2.y += velocidad

    # Movimiento de la bola
    bola.x += bola_dx
    bola.y += bola_dy

    # Colisiones con las raquetas
    if bola.colliderect(raqueta1) or bola.colliderect(raqueta2):
        bola_dx *= -1

 # Puntuación
    if bola.left <= 0:
        jugador2_puntos += 1
        if jugador2_puntos == 7:
            contador_jugador2 += 1
            jugador2_puntos = 0
            if contador_jugador2 == 7:
                pantalla_reinicio(2)  # Mostrar pantalla de reinicio para el jugador 2
            else:
                bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
                bola_dx = velocidad * random.choice((1, -1))
                bola_dy = velocidad * random.choice((1, -1))
    if bola.right >= ANCHO:
        jugador1_puntos += 1
        if jugador1_puntos == 7:
            contador_jugador1 += 1
            jugador1_puntos = 0
            if contador_jugador1 == 7:
                pantalla_reinicio(1)  # Mostrar pantalla de reinicio para el jugador 1
            else:
                bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
                bola_dx = velocidad * random.choice((1, -1))
                bola_dy = velocidad * random.choice((1, -1))

    # Colisiones con los bordes
    if bola.top <= 0 or bola.bottom >= ALTO:
        bola_dy *= -1

    dibujar()
    reloj.tick(60)
