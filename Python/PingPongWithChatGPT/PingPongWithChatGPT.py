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

# Velocidad de las raquetas
velocidad_raqueta = 5 * 0.7  # Reducida al 70%
sensibilidad_raquetas = velocidad_raqueta / 2  # Sensibilidad en la mitad de la velocidad

# Velocidad de la pelota
velocidad_pelota = [random.choice([-1, 1]) * 1, random.uniform(-1, 1)]

# Variables de estado del juego
estado_juego = "inicio"
puntos_jugador1 = 0
puntos_jugador2 = 0
puntos_para_ganar = 11  # Cantidad de puntos para ganar el juego

# Posiciones iniciales de las raquetas
posicion_raquetas = {
    "jugador1": [50, (pantalla_alto - alto_raqueta) // 2],
    "jugador2": [pantalla_ancho - 60, (pantalla_alto - alto_raqueta) // 2]
}

# Posición inicial de la pelota
posicion_pelota = [(pantalla_ancho - ancho_pelota) // 2, (pantalla_alto - alto_pelota) // 2]

# Función para reiniciar la dirección de la pelota
def reiniciar_direccion_pelota():
    direccion = random.choice([-1, 1])
    angulo = random.uniform(-math.pi / 4, math.pi / 4)
    velocidad_pelota[0] = direccion * math.cos(angulo)
    velocidad_pelota[1] = math.sin(angulo)

# Función para reiniciar el juego
def reiniciar_juego():
    global puntos_jugador1, puntos_jugador2, estado_juego
    puntos_jugador1 = 0
    puntos_jugador2 = 0
    reiniciar_posicion_pelota()
    estado_juego = "juego"

# Variable para controlar el seguimiento de la raqueta izquierda
seguimiento_activado = False

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if estado_juego == "inicio":
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
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Verificar si se presionó la tecla ESPACIO para iniciar el juego
                elif evento.key == pygame.K_SPACE:
                    estado_juego = "juego"

                # Agregar el código para activar/desactivar el seguimiento aquí
                elif evento.key == pygame.K_t:
                    seguimiento_activado = not seguimiento_activado  # Alternar el estado del seguimiento

    elif estado_juego == "juego":
        # Limpiar pantalla
        pantalla.fill(color_fondo)

        # Dibujar línea en el centro
        pygame.draw.line(pantalla, color_linea, (pantalla_ancho // 2, 0), (pantalla_ancho // 2, pantalla_alto), 5)

        # Dibujar raquetas
        pygame.draw.rect(pantalla, color_raquetas, (posicion_raquetas["jugador1"][0], posicion_raquetas["jugador1"][1], ancho_raqueta, alto_raqueta))
        pygame.draw.rect(pantalla, color_raquetas, (posicion_raquetas["jugador2"][0], posicion_raquetas["jugador2"][1], ancho_raqueta, alto_raqueta))

        # Dibujar pelota
        pygame.draw.rect(pantalla, color_pelota, (posicion_pelota[0], posicion_pelota[1], ancho_pelota, alto_pelota))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Agregar el código para activar/desactivar el seguimiento aquí
                elif evento.key == pygame.K_t:
                    seguimiento_activado = not seguimiento_activado  # Alternar el estado del seguimiento

        # Desactivar el movimiento manual de la raqueta izquierda si el seguimiento está activado
        if seguimiento_activado:
            keys[pygame.K_w] = False
            keys[pygame.K_s] = False

        # Movimiento de las raquetas
        keys = pygame.key.get_pressed()

        # Jugador 1 (izquierda)
        if not seguimiento_activado:  # Solo permite movimiento manual si el seguimiento está desactivado
            if keys[pygame.K_w] and posicion_raquetas["jugador1"][1] > 0:
                posicion_raquetas["jugador1"][1] -= sensibilidad_raquetas
            if keys[pygame.K_s] and posicion_raquetas["jugador1"][1] < pantalla_alto - alto_raqueta:
                posicion_raquetas["jugador1"][1] += sensibilidad_raquetas
        else:
            # Implementar el seguimiento automático aquí
            pelota_y = posicion_pelota[1]
            raqueta_y = posicion_raquetas["jugador1"][1]
            if pelota_y < raqueta_y + alto_raqueta / 2:
                posicion_raquetas["jugador1"][1] -= sensibilidad_raquetas
            elif pelota_y > raqueta_y + alto_raqueta / 2:
                posicion_raquetas["jugador1"][1] += sensibilidad_raquetas

        # Jugador 2
        if keys[pygame.K_UP] and posicion_raquetas["jugador2"][1] > 0:
            posicion_raquetas["jugador2"][1] -= sensibilidad_raquetas
        if keys[pygame.K_DOWN] and posicion_raquetas["jugador2"][1] < pantalla_alto - alto_raqueta:
            posicion_raquetas["jugador2"][1] += sensibilidad_raquetas

        # Movimiento de la pelota
        posicion_pelota[0] += velocidad_pelota[0]
        posicion_pelota[1] += velocidad_pelota[1]

        # Colisión con las paredes superior e inferior
        if posicion_pelota[1] <= 0 or posicion_pelota[1] >= pantalla_alto - alto_pelota:
            velocidad_pelota[1] = -velocidad_pelota[1]

        # Colisión con las raquetas
        if (posicion_pelota[0] <= posicion_raquetas["jugador1"][0] + ancho_raqueta and
            posicion_pelota[1] >= posicion_raquetas["jugador1"][1] and
            posicion_pelota[1] <= posicion_raquetas["jugador1"][1] + alto_raqueta):
            velocidad_pelota[0] = abs(velocidad_pelota[0])  # Cambia la dirección horizontal de la pelota

        if (posicion_pelota[0] >= posicion_raquetas["jugador2"][0] - ancho_pelota and
            posicion_pelota[1] >= posicion_raquetas["jugador2"][1] and
            posicion_pelota[1] <= posicion_raquetas["jugador2"][1] + alto_raqueta):
            velocidad_pelota[0] = -abs(velocidad_pelota[0])  # Cambia la dirección horizontal de la pelota

        # Verificar si la pelota ha llegado al borde izquierdo (puntos para jugador 2)
        if posicion_pelota[0] <= 0:
            puntos_jugador2 += 1
            reiniciar_direccion_pelota()
            posicion_pelota = [(pantalla_ancho - ancho_pelota) // 2, (pantalla_alto - alto_pelota) // 2]

        # Verificar si la pelota ha llegado al borde derecho (puntos para jugador 1)
        if posicion_pelota[0] >= pantalla_ancho - ancho_pelota:
            puntos_jugador1 += 1
            reiniciar_direccion_pelota()
            posicion_pelota = [(pantalla_ancho - ancho_pelota) // 2, (pantalla_alto - alto_pelota) // 2]

        # Verificar fin del juego y reiniciar
        if puntos_jugador1 >= puntos_para_ganar or puntos_jugador2 >= puntos_para_ganar:
            estado_juego = "fin"

        # Actualizar marcador
        font = pygame.font.Font(None, 50)
        texto_puntos = font.render(f"{puntos_jugador1}   {puntos_jugador2}", True, color_texto)
        ancho_texto = texto_puntos.get_width()
        posicion_x = (pantalla_ancho - ancho_texto) // 2
        pantalla.blit(texto_puntos, (posicion_x, 20))
        pygame.display.flip()

    # ...

    elif estado_juego == "fin":
        # Limpiar pantalla
        pantalla.fill(color_fondo)
        # Determinar al ganador
        ganador = "Jugador 1" if puntos_jugador1 > puntos_jugador2 else "Jugador 2"
        # No mostrar resultado

        # Mostrar texto para reiniciar el juego o salir
        font = pygame.font.Font(None, 30)
        texto2 = font.render("Presiona ESPACIO para jugar de nuevo", True, color_texto)
        texto3 = font.render("Presiona ESC para salir del Juego", True, color_texto)
        pantalla.blit(texto2, (200, 350))
        pantalla.blit(texto3, (250, 400))
        pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                reiniciar_juego()
                estado_juego = "juego"
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
