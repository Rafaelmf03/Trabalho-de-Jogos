import pygame
from util import EventHandler


class Bullet:
    """Projétil criado pelo evento Shoot e removido pelo evento DestroyObj."""
    def __init__(self, pos, damage):
        self.pos = pygame.Vector2(pos); self.damage = damage; self.radius = 5; self.speed = 560
    def update(self, dt):
        self.pos.y -= self.speed * dt
        if self.pos.y < -20: EventHandler().notify("DestroyObj", self)
    def draw(self, screen, font=None): pygame.draw.circle(screen, (255, 222, 70), self.pos, self.radius)
