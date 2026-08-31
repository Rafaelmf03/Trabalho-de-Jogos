import pygame
import random
from grid import Grid, Cell

pygame.init()
pygame.font.init()

# Configurações da Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris - Trab2")

font = pygame.font.Font(None, 36)

# Formatos de Tetraminós (Formas geométricas)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[1, 0, 0], [1, 1, 1]], # L
    [[0, 0, 1], [1, 1, 1]]  # J
]

COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128), (255, 165, 0), (0, 0, 255)]

class Piece:
    def __init__(self, col, row):
        idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        self.col = col
        self.row = row

    def rotate(self):
        self.shape = [list(r) for r in zip(*self.shape[::-1])]

# Instância da Grade
grid = Grid(x=250, y=50, rows=20, cols=10, cell_size=25)
current_piece = Piece(3, 0)

score = 0
level = 1
clock = pygame.time.Clock()
fall_time = 0

def valid_move(piece, grid, offset_col=0, offset_row=0):
    for r, row in enumerate(piece.shape):
        for c, val in enumerate(row):
            if val:
                new_col = piece.col + c + offset_col
                new_row = piece.row + r + offset_row
                if new_col < 0 or new_col >= grid.cols or new_row >= grid.rows:
                    return False
                if new_row >= 0 and grid.grid[new_row][new_col] is not None:
                    return False
    return True

def lock_piece(piece, grid):
    for r, row in enumerate(piece.shape):
        for c, val in enumerate(row):
            if val:
                grid.grid[piece.row + r][piece.col + c] = piece.color

# Loop principal
running = True
while running:
    dt = clock.tick(30)
    fall_time += dt

# Queda automática por tempo/nível
    if fall_time > max(100, 500 - (level * 40)):
        if valid_move(current_piece, grid, offset_row=1):
            current_piece.row += 1
        else:
            lock_piece(current_piece, grid)
            cleared = grid.clear_lines()
            score += cleared * 100
            level = 1 + score // 500
            current_piece = Piece(3, 0)
            if not valid_move(current_piece, grid):
                running = False # Game Over
        fall_time = 0

# Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# --- Controle por TECLADO ---
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT and valid_move(current_piece, grid, offset_col=-1):
                current_piece.col -= 1
            elif event.key == pygame.K_RIGHT and valid_move(current_piece, grid, offset_col=1):
                current_piece.col += 1
            elif event.key == pygame.K_DOWN and valid_move(current_piece, grid, offset_row=1):
                current_piece.row += 1
            elif event.key == pygame.K_UP:
                current_piece.rotate()
                if not valid_move(current_piece, grid):
                    for _ in range(3): current_piece.rotate() # Desfaz se inválido

# --- Controle por MOUSE ---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clique Esquerdo = Mover para a esquerda
                if valid_move(current_piece, grid, offset_col=-1):
                    current_piece.col -= 1
            elif event.button == 3: # Clique Direito = Mover para a direita
                if valid_move(current_piece, grid, offset_col=1):
                    current_piece.col += 1
            elif event.button == 2: # Botão do Meio (Scroll) = Girar peça
                current_piece.rotate()
                if not valid_move(current_piece, grid):
                    for _ in range(3): current_piece.rotate()

# Desenho da tela
    screen.fill((20, 20, 20))
    grid.draw(screen)

# Desenha a peça atual caindo
    for r, row in enumerate(current_piece.shape):
        for c, val in enumerate(row):
            if val:
                cell_x = grid.x + (current_piece.col + c) * grid.cell_size
                cell_y = grid.y + (current_piece.row + r) * grid.cell_size
                cell = Cell(cell_x, cell_y, grid.cell_size, current_piece.color)
                cell.draw(screen)

# Textos na tela
    score_text = font.render(f"Pontos: {score}", True, (255, 255, 255))
    level_text = font.render(f"Nivel: {level}", True, (255, 255, 255))
    controls_text = font.render("Mouse: Esq/Direito move, Scroll gira", True, (150, 150, 150))
    
    screen.blit(score_text, (50, 50))
    screen.blit(level_text, (50, 100))
    screen.blit(controls_text, (50, 500))

    pygame.display.flip()

pygame.quit()