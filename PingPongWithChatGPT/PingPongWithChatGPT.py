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
reloj = pygame.time.Clock()

# Raquetas
raqueta1 = pygame.Rect(50, ALTO // 2 - 70, 10, 140)
raqueta2 = pygame.Rect(ANCHO - 60, ALTO // 2 - 70, 10, 140)

# Bola
bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
bola_dx = velocidad * random.choice((1, -1))
bola_dy = velocidad * random.choice((1, -1))

# Función para dibujar la pantalla y objetos del juego
def dibujar():
    pantalla.fill(BLANCO)
    pygame.draw.rect(pantalla, NEGRO, raqueta1)
    pygame.draw.rect(pantalla, NEGRO, raqueta2)
    pygame.draw.ellipse(pantalla, NEGRO, bola)
    pygame.draw.aaline(pantalla, NEGRO, (ANCHO // 2, 0), (ANCHO // 2, ALTO))

    # Marcador
    fuente = pygame.font.Font(None, 48)
    marcador1 = fuente.render(str(jugador1_puntos), True, NEGRO)
    marcador2 = fuente.render(str(jugador2_puntos), True, NEGRO)
    pantalla.blit(marcador1, (ANCHO // 4, 10))
    pantalla.blit(marcador2, (3 * ANCHO // 4 - 30, 10))

    pygame.display.flip()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
        bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
        bola_dx = velocidad * random.choice((1, -1))
        bola_dy = velocidad * random.choice((1, -1))
    if bola.right >= ANCHO:
        jugador1_puntos += 1
        bola = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
        bola_dx = velocidad * random.choice((1, -1))
        bola_dy = velocidad * random.choice((1, -1))

    # Colisiones con los bordes
    if bola.top <= 0 or bola.bottom >= ALTO:
        bola_dy *= -1

    dibujar()
    reloj.tick(60)


