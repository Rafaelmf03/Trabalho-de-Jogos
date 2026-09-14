import pygame
from util import EventHandler, centered_text


class Enemy:
    """Estados: aproximando, atordoado e destruído."""
    def __init__(self, pos, health):
        self.pos = pygame.Vector2(pos); self.health = health; self.radius = 22; self.state = ApproachingState(self)
    def update(self, dt): self.state.update(dt)
    def draw(self, screen, font): self.state.draw(screen, font)
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.state = DestroyedState(self); EventHandler().notify("EnemyDestroyed", self); EventHandler().notify("DestroyObj", self)
        else: self.state = StunnedState(self)


class EnemyState:
    def __init__(self, enemy): self.enemy = enemy
    def draw(self, screen, font):
        e = self.enemy; pygame.draw.circle(screen, self.color, e.pos, e.radius); centered_text(screen, font, e.health, e.pos, (35, 25, 25))


class ApproachingState(EnemyState):
    color = (225, 75, 70)
    def update(self, dt): self.enemy.pos.y += 70 * dt


class StunnedState(EnemyState):
    color = (180, 100, 220)
    def __init__(self, enemy): super().__init__(enemy); self.remaining = .18
    def update(self, dt):
        self.remaining -= dt
        if self.remaining <= 0: self.enemy.state = ApproachingState(self.enemy)


class DestroyedState(EnemyState):
    color = (50, 50, 50)
    def update(self, dt): pass
