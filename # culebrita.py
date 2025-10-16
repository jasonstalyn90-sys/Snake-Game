# culebrita.py
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

# --- Lógica principal del juego ---
def run_game():
    # snake: lista de posiciones (x, y) - cabeza es índice 0
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = (1, 0)  # dx, dy  -> empieza moviéndose a la derecha
    next_direction = direction

    food = random_food_position(snake)
    score = 0
    high_score = 0

    speed_increment_threshold = 50  # cada cuántos puntos aumentamos la velocidad
    extra_speed = 0

    game_over = False

    global FPS
    current_fps = FPS

    while True:
        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and game_over:
                    # reiniciar partida
                    return True  # señal para reiniciar
                # Cambiar dirección (no permitir giro 180º)
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Rebote con paredes? (opción: que choque y muera)
            # Aquí implementamos que chocar con la pared termina el juego
            out_of_bounds = (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
            )

            # Colisión con el propio cuerpo
            collision_self = new_head in snake

            if out_of_bounds or collision_self:
                game_over = True
            else:
                snake.insert(0, new_head)  # nueva cabeza
                # Comer la comida
                if new_head == food:
                    score += POINTS_PER_APPLE
                    # generar nueva comida en posición aleatoria que no choque con la serpiente
                    food = random_food_position(snake)
                    # ajustar velocidad según puntaje
                    extra_speed = score // speed_increment_threshold
                    current_fps = FPS + extra_speed
                else:
                    snake.pop()  # quitar la cola (se mueve sin crecer)

                if score > high_score:
                    high_score = score

        # --- Dibujado ---
        screen.fill(BLACK)
        draw_grid()

        # dibujar comida
        draw_rect_at_grid(food, RED)
        # dibujar serpiente
        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else (0, 220 - min(200, i*8), 0)  # cabeza más brillante
            draw_rect_at_grid(segment, color)

        draw_score(score, high_score)

        if game_over:
            # Mensaje de game over
            over_text = big_font.render("¡Game Over!", True, WHITE)
            instr_text = font.render("Presiona R para reiniciar o Esc para salir", True, WHITE)
            rect = over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
            rect2 = instr_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
            screen.blit(over_text, rect)
            screen.blit(instr_text, rect2)

        pygame.display.flip()

        # --- Control de frames ---
        clock.tick(current_fps)

# --- Ciclo principal para permitir reinicios ---
if __name__ == "__main__":
    while True:
        restart = run_game()
        if not restart:
            break