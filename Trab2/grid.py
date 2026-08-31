import pygame
from abc import ABC, abstractmethod

# Classe base abstrata
class obj(ABC):
    def __init__(self, x, y, sprites=None):
        self.x = x
        self.y = y
        self.sprites = sprites if sprites else []

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(s, (self.x, self.y))

    @abstractmethod
    def update(self, dt):
        pass

# Representa cada célula individual do Tetris
class Cell(obj):
    def __init__(self, x, y, cell_size, color=(50, 50, 50)):
        super().__init__(x, y)
        self.size = cell_size
        self.color = color

    def draw(self, screen):
# Desenha o bloco com uma borda simples
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size - 1, self.size - 1))

    def update(self, dt):
        pass

# Gerencia a grade do jogo
class Grid(obj):
    def __init__(self, x, y, rows=20, cols=10, cell_size=25):
        super().__init__(x, y)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
# Matriz vazia (0 = vazio, cores para blocos fixos)
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
# Desenha as células já fixadas na grade
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid[r][c] if self.grid[r][c] else (40, 40, 40)
                cell_x = self.x + c * self.cell_size
                cell_y = self.y + r * self.cell_size
                cell = Cell(cell_x, cell_y, self.cell_size, color)
                cell.draw(screen)

    def update(self, dt):
        pass

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        lines_cleared = self.rows - len(new_grid)
        
        while len(new_grid) < self.rows:
            new_grid.insert(0, [None for _ in range(self.cols)])
            
        self.grid = new_grid
        return lines_cleared