# culebrita.py
import pygame
import random
import sys

# --- Configuración ---
TAMANO_CELDA = 20
ANCHO_CUADRICULA = 30   # ancho en celdas
ALTO_CUADRICULA = 20    # alto en celdas
ANCHO_VENTANA = TAMANO_CELDA * ANCHO_CUADRICULA
ALTO_VENTANA = TAMANO_CELDA * ALTO_CUADRICULA
FPS_BASE = 10  # velocidad base (frames por segundo)
PUNTOS_POR_COMIDA = 10

# Colores (R,G,B)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 180, 0)
ROJO = (200, 0, 0)
GRIS = (40, 40, 40)

# --- Inicialización ---
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Culebrita - Juego Snake")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 28)
fuente_grande = pygame.font.SysFont(None, 56)

# --- Funciones auxiliares ---
def dibujar_rectangulo_en_cuadricula(posicion, color):
    x, y = posicion
    rectangulo = pygame.Rect(x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
    pygame.draw.rect(pantalla, color, rectangulo)

def posicion_aleatoria_comida(serpiente):
    while True:
        posicion = (random.randint(0, ANCHO_CUADRICULA - 1), random.randint(0, ALTO_CUADRICULA - 1))
        if posicion not in serpiente:
            return posicion

def dibujar_cuadricula():
    for x in range(0, ANCHO_VENTANA, TAMANO_CELDA):
        pygame.draw.line(pantalla, GRIS, (x, 0), (x, ALTO_VENTANA))
    for y in range(0, ALTO_VENTANA, TAMANO_CELDA):
        pygame.draw.line(pantalla, GRIS, (0, y), (ANCHO_VENTANA, y))

def dibujar_puntaje(puntaje, mejor_puntaje):
    texto = fuente.render(f"Puntos: {puntaje}  |  Récord: {mejor_puntaje}", True, BLANCO)
    pantalla.blit(texto, (8, 8))

# --- Lógica principal del juego ---
def ejecutar_juego():
    inicio_x = ANCHO_CUADRICULA // 2
    inicio_y = ALTO_CUADRICULA // 2
    serpiente = [(inicio_x, inicio_y), (inicio_x - 1, inicio_y), (inicio_x - 2, inicio_y)]
    direccion = (1, 0)  # dx, dy -> comienza moviéndose a la derecha
    proxima_direccion = direccion

    comida = posicion_aleatoria_comida(serpiente)
    puntaje = 0
    mejor_puntaje = 0

    umbral_aumento_velocidad = 50  # cada cuántos puntos aumenta la velocidad
    velocidad_extra = 0

    juego_terminado = False

    global FPS_BASE
    fps_actual = FPS_BASE

    while True:
        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_r and juego_terminado:
                    return True  # reiniciar partida

                # Cambiar dirección (no permitir giro de 180º)
                if evento.key == pygame.K_UP and direccion != (0, 1):
                    proxima_direccion = (0, -1)
                elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                    proxima_direccion = (0, 1)
                elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                    proxima_direccion = (-1, 0)
                elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                    proxima_direccion = (1, 0)

        if not juego_terminado:
            direccion = proxima_direccion
            cabeza_x, cabeza_y = serpiente[0]
            dx, dy = direccion
            nueva_cabeza = (cabeza_x + dx, cabeza_y + dy)

            # Verificar si sale de los límites
            fuera_de_limites = (
                nueva_cabeza[0] < 0 or nueva_cabeza[0] >= ANCHO_CUADRICULA or
                nueva_cabeza[1] < 0 or nueva_cabeza[1] >= ALTO_CUADRICULA
            )

            # Colisión con sí misma
            colision_con_cuerpo = nueva_cabeza in serpiente

            if fuera_de_limites or colision_con_cuerpo:
                juego_terminado = True
            else:
                serpiente.insert(0, nueva_cabeza)

                # Comer comida
                if nueva_cabeza == comida:
                    puntaje += PUNTOS_POR_COMIDA
                    comida = posicion_aleatoria_comida(serpiente)
                    velocidad_extra = puntaje // umbral_aumento_velocidad
                    fps_actual = FPS_BASE + velocidad_extra
                else:
                    serpiente.pop()  # eliminar último segmento

                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje

        # --- Dibujar ---
        pantalla.fill(NEGRO)
        dibujar_cuadricula()

        # Dibuja la comida
        dibujar_rectangulo_en_cuadricula(comida, ROJO)
        # Dibuja la serpiente
        for i, segmento in enumerate(serpiente):
            color = VERDE if i == 0 else (0, 220 - min(200, i * 8), 0)
            dibujar_rectangulo_en_cuadricula(segmento, color)

        dibujar_puntaje(puntaje, mejor_puntaje)

        if juego_terminado:
            texto_final = fuente_grande.render("¡Fin del juego!", True, BLANCO)
            texto_instrucciones = fuente.render("Presiona R para reiniciar o Esc para salir", True, BLANCO)
            rect1 = texto_final.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 20))
            rect2 = texto_instrucciones.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))
            pantalla.blit(texto_final, rect1)
            pantalla.blit(texto_instrucciones, rect2)

        pygame.display.flip()
        reloj.tick(fps_actual)

# --- Bucle principal ---
if __name__ == "__main__":
    while True:
        reiniciar = ejecutar_juego()
        if not reiniciar:
            break