import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()

# Definir dimensiones de la pantalla
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption("Ping Pong Game")

# Colores
color_fondo = (0, 0, 0)
color_texto = (255, 255, 255)
color_linea = (255, 255, 255)
color_raquetas = (255, 255, 255)
color_pelota = (255, 255, 255)

# Dimensiones de las raquetas y la pelota
ancho_raqueta = 10
alto_raqueta = 100
ancho_pelota = 10
alto_pelota = 10

# Velocidad de las raquetas y aceleración
velocidad_raqueta = 5
aceleracion_raqueta = 1

# Velocidad inicial de la pelota
angulo = random.uniform(-math.pi / 4, math.pi / 4)  # Ángulo aleatorio entre -45 y 45 grados
velocidad_pelota = [math.cos(angulo), math.sin(angulo)]  # Velocidad inicial en la dirección del ángulo

# Magnitud de velocidad constante
velocidad_constante = 1.0  # Ajusta este valor según tu preferencia

# Normalizar el vector de velocidad
norma = math.sqrt(velocidad_pelota[0] ** 2 + velocidad_pelota[1] ** 2)
velocidad_pelota[0] = (velocidad_pelota[0] / norma) * velocidad_constante
velocidad_pelota[1] = (velocidad_pelota[1] / norma) * velocidad_constante

# Posición inicial de la pelota
posicion_pelota = [(pantalla_ancho - ancho_pelota) // 2, (pantalla_alto - alto_pelota) // 2]

# Variables de estado del juego
estado_juego = "inicio"
puntos_jugador1 = 0
puntos_jugador2 = 0
puntos_para_ganar = 11  # Cantidad de puntos para ganar el juego

# Posiciones iniciales de las raquetas y velocidad
posicion_raqueta_jugador1 = [50, (pantalla_alto - alto_raqueta) // 2]
posicion_raqueta_jugador2 = [pantalla_ancho - 60, (pantalla_alto - alto_raqueta) // 2]
velocidad_raqueta_jugador1 = 0
velocidad_raqueta_jugador2 = 0

# Función para reiniciar la posición de la pelota
def reiniciar_posicion_pelota():
    global posicion_pelota, velocidad_pelota
    # Reinicia la posición de la pelota al centro
    posicion_pelota = [(pantalla_ancho - ancho_pelota) // 2, (pantalla_alto - alto_pelota) // 2]
    # Ahora, vamos a decidir aleatoriamente si la pelota se mueve hacia la derecha o hacia la izquierda
    direccion = random.choice([-1, 1])  # -1 para izquierda, 1 para derecha
    angulo = random.uniform(-math.pi / 4, math.pi / 4)  # Ángulo aleatorio entre -45 y 45 grados
    if direccion == 1:
        velocidad_pelota = [math.cos(angulo), math.sin(angulo)]  # Dirección hacia la derecha
    else:
        velocidad_pelota = [-math.cos(angulo), -math.sin(angulo)]  # Dirección hacia la izquierda

# Función para reiniciar el juego
def reiniciar_juego():
    global puntos_jugador1, puntos_jugador2, estado_juego
    puntos_jugador1 = 0
    puntos_jugador2 = 0
    reiniciar_posicion_pelota()
    estado_juego = "inicio"

# Función para la pantalla de inicio
def pantalla_inicio():
    global estado_juego
    # Limpiar pantalla
    pantalla.fill(color_fondo)
    # Dibujar texto de inicio
    font = pygame.font.Font(None, 36)
    texto1 = font.render("Presiona ESPACIO para empezar", True, color_texto)
    texto2 = font.render("Presiona ESC para salir", True, color_texto)
    pantalla.blit(texto1, (200, 250))
    pantalla.blit(texto2, (250, 300))
    pygame.display.flip()
    
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                estado_juego = "juego"
            # Verificar si se presionó la tecla ESCAPE para cerrar el programa
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# Función para la pantalla de juego
def pantalla_juego():
    global estado_juego, puntos_jugador1, puntos_jugador2, posicion_raqueta_jugador1, posicion_raqueta_jugador2, velocidad_raqueta_jugador1, velocidad_raqueta_jugador2, velocidad_pelota, posicion_pelota
    
    # Detectar colisión con raqueta del jugador 1
    if (posicion_pelota[0] <= posicion_raqueta_jugador1[0] + ancho_raqueta and
        posicion_pelota[1] >= posicion_raqueta_jugador1[1] and
        posicion_pelota[1] <= posicion_raqueta_jugador1[1] + alto_raqueta):
            velocidad_pelota[0] = abs(velocidad_pelota[0])  # Cambia la dirección horizontal de la pelota

# Detectar colisión con raqueta del jugador 2
    if (posicion_pelota[0] >= posicion_raqueta_jugador2[0] - ancho_pelota and
        posicion_pelota[1] >= posicion_raqueta_jugador2[1] and
        posicion_pelota[1] <= posicion_raqueta_jugador2[1] + alto_raqueta):
            velocidad_pelota[0] = -abs(velocidad_pelota[0])  # Cambia la dirección horizontal de la pelota
    # Limpiar pantalla
    pantalla.fill(color_fondo)

    # Dibujar línea en el centro
    pygame.draw.line(pantalla, color_linea, (pantalla_ancho // 2, 0), (pantalla_ancho // 2, pantalla_alto), 5)

    # Dibujar raquetas
    pygame.draw.rect(pantalla, color_raquetas, (posicion_raqueta_jugador1[0], posicion_raqueta_jugador1[1], ancho_raqueta, alto_raqueta))
    pygame.draw.rect(pantalla, color_raquetas, (posicion_raqueta_jugador2[0], posicion_raqueta_jugador2[1], ancho_raqueta, alto_raqueta))

    # Dibujar pelota
    pygame.draw.rect(pantalla, color_pelota, (posicion_pelota[0], posicion_pelota[1], ancho_pelota, alto_pelota))

    # Control de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Movimiento de las raquetas
    keys = pygame.key.get_pressed()
    
    # Jugador 1
    if keys[pygame.K_w] and posicion_raqueta_jugador1[1] > 0:
        velocidad_raqueta_jugador1 = -velocidad_raqueta
    elif keys[pygame.K_s] and posicion_raqueta_jugador1[1] < pantalla_alto - alto_raqueta:
        velocidad_raqueta_jugador1 = velocidad_raqueta
    else:
        velocidad_raqueta_jugador1 = 0
        
    # Jugador 2
    if keys[pygame.K_UP] and posicion_raqueta_jugador2[1] > 0:
        velocidad_raqueta_jugador2 = -velocidad_raqueta
    elif keys[pygame.K_DOWN] and posicion_raqueta_jugador2[1] < pantalla_alto - alto_raqueta:
        velocidad_raqueta_jugador2 = velocidad_raqueta
    else:
        velocidad_raqueta_jugador2 = 0

    # Aplicar velocidad a las raquetas
    posicion_raqueta_jugador1[1] += velocidad_raqueta_jugador1
    posicion_raqueta_jugador2[1] += velocidad_raqueta_jugador2

    # Movimiento de la pelota (velocidad constante)
    posicion_pelota[0] += velocidad_pelota[0]
    posicion_pelota[1] += velocidad_pelota[1]

    # Colisión con las paredes superior e inferior
    if posicion_pelota[1] <= 0 or posicion_pelota[1] >= pantalla_alto - alto_pelota:
        velocidad_pelota[1] = -velocidad_pelota[1]

    # Colisión con las paredes izquierda y derecha
    if posicion_pelota[0] <= 0 or posicion_pelota[0] >= pantalla_ancho - ancho_pelota:
        velocidad_pelota[0] = -velocidad_pelota[0]

    # Verificar si la pelota ha llegado al borde izquierdo (puntos para jugador 2)
    if posicion_pelota[0] <= 0:
        puntos_jugador2 += 1
        reiniciar_posicion_pelota()
    # Verificar si la pelota ha llegado al borde derecho (puntos para jugador 1)
    if posicion_pelota[0] >= pantalla_ancho - ancho_pelota:
        puntos_jugador1 += 1
        reiniciar_posicion_pelota()

    # Verificar fin del juego y reiniciar
    if puntos_jugador1 >= puntos_para_ganar or puntos_jugador2 >= puntos_para_ganar:
        reiniciar_juego()

    # Actualizar marcador
    font = pygame.font.Font(None, 36)
    texto_puntos = font.render(f"Jugador 1: {puntos_jugador1}  Jugador 2: {puntos_jugador2}", True, color_texto)
    pantalla.blit(texto_puntos, (280, 20))

    pygame.display.flip()

# Función para la pantalla de fin de juego
def pantalla_fin():
    global estado_juego
    # Limpiar pantalla
    pantalla.fill(color_fondo)
    # Determinar al ganador
    if puntos_jugador1 > puntos_jugador2:
        ganador = "Jugador 1"
    else:
        ganador = "Jugador 2"
    # Mostrar resultado
    font = pygame.font.Font(None, 48)
    texto = font.render(f"{ganador} gana!", True, color_texto)
    pantalla.blit(texto, (300, 250))
    texto2 = font.render("Presiona ESPACIO para jugar de nuevo", True, color_texto)
    pantalla.blit(texto2, (200, 350))
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                reiniciar_juego()
                estado_juego = "juego"

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if estado_juego == "inicio":
        pantalla_inicio()
    elif estado_juego == "juego":
        pantalla_juego()
    elif estado_juego == "fin":
        pantalla_fin()
