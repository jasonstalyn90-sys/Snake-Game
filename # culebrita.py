# culebrita.py
import pygame
import random
import sys

# --- Configuración ---
CELL_SIZE = 20
GRID_WIDTH = 30   # ancho en celdas
GRID_HEIGHT = 20  # alto en celdas
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10  # velocidad base (frames por segundo)
POINTS_PER_APPLE = 10

# Colores (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# --- Inicialización ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Culebrita - Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 56)

# --- Funciones auxiliares ---
def draw_rect_at_grid(pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_score(score, high_score):
    text = font.render(f"Puntos: {score}  |  Mejor: {high_score}", True, WHITE)
    screen.blit(text, (8, 8))