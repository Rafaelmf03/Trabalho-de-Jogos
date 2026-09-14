import pygame
from util import EventHandler, centered_text


class Gate:
    def __init__(self, x, operation):
        self.x = x; self.y = -80; self.operation = operation; self.width, self.height = 440, 70; self.used = False
    def update(self, dt):
        self.y += 125 * dt
        if self.y > 680: EventHandler().notify("DestroyObj", self)
    def contains(self, pos): return abs(pos.x - self.x) < self.width / 2 and abs(pos.y - self.y) < self.height / 2
    def draw(self, screen, font):
        color = (45, 185, 100) if self.operation[0] in "+x" else (215, 80, 75)
        rect = pygame.Rect(0, 0, self.width, self.height); rect.center = (self.x, self.y)
        pygame.draw.rect(screen, color, rect, border_radius=10); pygame.draw.rect(screen, (245, 245, 245), rect, 3, border_radius=10)
        centered_text(screen, font, f"{self.operation[0]}{self.operation[1]}", rect.center)
