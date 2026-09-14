import pygame
from abc import ABC, abstractmethod
from util import EventHandler, centered_text


class Player:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos); self.members = 20; self.radius = 30
        self.state = MovingState(self); self.shot_cooldown = 0
        EventHandler().subscribe("GateChosen", self.apply_gate)
        EventHandler().subscribe("PlayerDamaged", self.take_damage)
    def update(self, dt, keys):
        self.state.update(dt, keys); self.shot_cooldown -= dt
        if self.members > 0 and self.shot_cooldown <= 0:
            EventHandler().notify("Shoot", {"pos": self.pos.copy(), "damage": max(1, self.members // 8)})
            self.shot_cooldown = max(.16, .55 - self.members * .006)
    def draw(self, screen, font): self.state.draw(screen, font)
    def apply_gate(self, operation):
        op, value = operation
        if op == "+": self.members += value
        elif op == "-": self.members = max(1, self.members - value)
        elif op == "x": self.members *= value
        elif op == "/": self.members = max(1, self.members // value)
    def take_damage(self, amount):
        if isinstance(self.state, InvincibleState): return
        self.members -= amount
        if self.members <= 0:
            self.members = 0; self.state = DefeatedState(self); EventHandler().notify("GameOver")
        else: self.state = InvincibleState(self)


class PlayerState(ABC):
    def __init__(self, player): self.player = player
    @abstractmethod
    def update(self, dt, keys): pass
    def draw(self, screen, font):
        p = self.player
        pygame.draw.circle(screen, self.color, p.pos, p.radius)
        pygame.draw.circle(screen, (245, 245, 245), p.pos, p.radius, 2)
        centered_text(screen, font, p.members, (p.pos.x, p.pos.y - 2))


class MovingState(PlayerState):
    color = (55, 155, 235)
    def update(self, dt, keys):
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player.pos.x = max(55, min(745, self.player.pos.x + direction * 330 * dt))


class InvincibleState(MovingState):
    color = (245, 205, 70)
    def __init__(self, player): super().__init__(player); self.remaining = 1.0
    def update(self, dt, keys):
        super().update(dt, keys); self.remaining -= dt
        if self.remaining <= 0: self.player.state = MovingState(self.player)
    def draw(self, screen, font):
        if int(self.remaining * 12) % 2 == 0: super().draw(screen, font)


class DefeatedState(PlayerState):
    color = (100, 100, 100)
    def update(self, dt, keys): pass
