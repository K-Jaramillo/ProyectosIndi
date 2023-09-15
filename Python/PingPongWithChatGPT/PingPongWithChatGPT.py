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
sensibilidad = 1.0
velocidad = 5
jugador1_puntos = 0
jugador2_puntos = 0
contador_jugador1 = 0
contador_jugador2 = 0
reloj = pygame.time.Clock()
inversion_colores = False
inicio = True
boton_switch_presionado = False  # Declaración de la variable boton_switch_presionado

# Raquetas
raqueta1 = pygame.Rect(50, ALTO // 2 - 70, 10, 140)
raqueta2 = pygame.Rect(ANCHO - 60, ALTO // 2 - 70, 10, 140)

# Bola
bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
bola_dx = velocidad * random.choice((1, -1))
bola_dy = velocidad * random.choice((1, -1))

# Función para dibujar la pantalla y objetos del juego
def dibujar():
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)
    pygame.draw.rect(pantalla, NEGRO if not inversion_colores else BLANCO, raqueta1)
    pygame.draw.rect(pantalla, NEGRO if not inversion_colores else BLANCO, raqueta2)
    pygame.draw.ellipse(pantalla, NEGRO if not inversion_colores else BLANCO, bola)
    pygame.draw.aaline(pantalla, NEGRO if not inversion_colores else BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO))

    # Marcador
    fuente = pygame.font.Font(None, 20)
    contador_marcador1 = fuente.render(f"Rondas: {contador_jugador1}", True, NEGRO if not inversion_colores else BLANCO)
    contador_marcador2 = fuente.render(f"Rondas: {contador_jugador2}", True, NEGRO if not inversion_colores else BLANCO)
    pantalla.blit(contador_marcador1, (ANCHO // 4, 30))
    pantalla.blit(contador_marcador2, (2.8 * ANCHO // 4, 30))

    # Botón de inversión de colores (Switch)
    switch_color = BLANCO if boton_switch_presionado else NEGRO
    switch_texto = "Modo Oscuro" if boton_switch_presionado else "Modo Claro"
    pygame.draw.rect(pantalla, switch_color, (ANCHO - 120, 10, 100, 40))
    fuente = pygame.font.Font(None, 24)
    texto_boton = fuente.render(switch_texto, True, BLANCO)
    pantalla.blit(texto_boton, (ANCHO - 110, 20))

    pygame.display.flip()

# Función para invertir los colores globalmente
def invertir_colores_globalmente():
    global inversion_colores
    inversion_colores = not inversion_colores

# Función para manejar eventos de juego
def manejar_eventos():
    global inicio
    global jugador1_puntos, jugador2_puntos, contador_jugador1, contador_jugador2
    global bola, bola_dx, bola_dy
    global boton_switch_presionado  # Declaración de la variable boton_switch_presionado

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if inicio:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inicio = False
        else:
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
                        pantalla_reinicio(2)
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
                        pantalla_reinicio(1)
                    else:
                        bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
                        bola_dx = velocidad * random.choice((1, -1))
                        bola_dy = velocidad * random.choice((1, -1))

            # Colisiones con los bordes
            if bola.top <= 0 or bola.bottom >= ALTO:
                bola_dy *= -1

            # Manejar el clic del botón "Switch"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if ANCHO - 120 <= x <= ANCHO - 20 and 10 <= y <= 50:
                        boton_switch_presionado = not boton_switch_presionado
                        invertir_colores_globalmente()
                        dibujar()

# Pantalla de inicio
def pantalla_inicio():
    global inicio
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)
    fuente = pygame.font.Font(None, 30)
    texto = fuente.render("Presiona ESPACIO para comenzar", True, NEGRO if not inversion_colores else BLANCO)
    pantalla.blit(texto, (ANCHO // 4, ALTO // 2))
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)
    pygame.display.flip()
    esperando_inicio = True
    while esperando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inicio = False
                esperando_inicio = False

# Pantalla de reinicio
def pantalla_reinicio(ganador):
    global inicio
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)
    fuente = pygame.font.Font(None, 30)
    texto = fuente.render(f"Jugador {ganador} ha ganado 3 rondas.", True, NEGRO if not inversion_colores else BLANCO)
    pantalla.blit(texto, (ANCHO // 4, ALTO // 2 - 30))
    texto2 = fuente.render("Presiona ESPACIO para reiniciar", True, NEGRO if not inversion_colores else BLANCO)
    pantalla.blit(texto2, (ANCHO // 4, ALTO // 2 + 10))
    pygame.draw.rect(pantalla, NEGRO, (ANCHO - 120, 10, 100, 40))
    fuente = pygame.font.Font(None, 24)
    texto_boton = fuente.render("Switch", True, BLANCO)
    pantalla.blit(texto_boton, (ANCHO - 110, 20))
    pantalla.fill(BLANCO if not inversion_colores else NEGRO)
    pygame.display.flip()
    esperando_reinicio = True
    while esperando_reinicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                global jugador1_puntos, jugador2_puntos, contador_jugador1, contador_jugador2
                jugador1_puntos = 0
                jugador2_puntos = 0
                contador_jugador1 = 0
                contador_jugador2 = 0
                inicio = True  # Asegúrate de establecer 'inicio' en True
                esperando_reinicio = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if ANCHO - 120 <= x <= ANCHO - 20 and 10 <= y <= 50:
                        invertir_colores_globalmente()  # Invertir colores globalmente al hacer clic en el botón en la pantalla de reinicio
                        pantalla_inicio()  # Llamar a pantalla_inicio() cuando se haga clic en el botón

# Bucle principal del juego
pantalla_inicio()  # Espera a que el jugador presione ESPACIO para iniciar
while True:
    manejar_eventos()
    dibujar()
    reloj.tick(60)

