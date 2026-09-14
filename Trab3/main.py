import pygame
import random
from player import Player
from bullet import Bullet
from enemy import Enemy
from gate import Gate
from util import EventHandler, circle_collision, centered_text

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Squad: escolha e sobreviva")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25, bold=True)
big_font = pygame.font.SysFont("arial", 48, bold=True)

objects = []
player = Player((WIDTH / 2, 510))
score = 0
game_over = False
gate_timer, enemy_timer = 1.2, 4.0
gate_choices = [("+", 12), ("/", 3), ("-", 50), ("/", 30), ("-", 15), ("-", 8), ("x", 2), ("/", 2), ("+", 25), ("x", 5), ("-", 15)]


def add_object(obj): objects.append(obj)
def remove_object(obj):
    if obj in objects: objects.remove(obj)
def shoot(data): add_object(Bullet(data["pos"], data["damage"]))
def add_score(enemy):
    global score
    score += 10
def end_game(_=None):
    global game_over
    game_over = True


events = EventHandler()
def configure_events():
    events.subscribe("CreateObj", add_object)
    events.subscribe("DestroyObj", remove_object)
    events.subscribe("Shoot", shoot)
    events.subscribe("EnemyDestroyed", add_score)
    events.subscribe("GameOver", end_game)
configure_events()


def spawn_gates():
    # Dois portões por vez obrigam o jogador a tomar uma decisão.
    left = random.choice(gate_choices)
    right = random.choice(gate_choices)
    while right == left: right = random.choice(gate_choices)
    add_object(Gate(180, left)); add_object(Gate(620, right))


def spawn_enemy():
    health = random.randint(3, 8) + score // 80
    add_object(Enemy((random.randint(70, 730), -30), health))


def check_collisions():
    for obj in objects[:]:
        if isinstance(obj, Gate) and not obj.used and obj.contains(player.pos):
            obj.used = True
            events.notify("GateChosen", obj.operation)
            events.notify("DestroyObj", obj)
        elif isinstance(obj, Enemy):
            if circle_collision(obj.pos, obj.radius, player.pos, player.radius):
                events.notify("PlayerDamaged", max(2, obj.health))
                events.notify("DestroyObj", obj)
                continue
            for projectile in objects[:]:
                if isinstance(projectile, Bullet) and circle_collision(obj.pos, obj.radius, projectile.pos, projectile.radius):
                    obj.hit(projectile.damage)
                    events.notify("DestroyObj", projectile)
                    break


running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            # Reiniciar com R evita menu e mantém a demonstração direta.
            objects.clear(); events.clear(); player = Player((WIDTH / 2, 510)); configure_events(); score = 0
            game_over = False; gate_timer, enemy_timer = 1.2, 4.0

    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(dt, keys)
        gate_timer -= dt; enemy_timer -= dt
        if gate_timer <= 0: spawn_gates(); gate_timer = 5.2
        if enemy_timer <= 0: spawn_enemy(); enemy_timer = max(1.2, 3.2 - score / 400)
        for obj in objects[:]: obj.update(dt)
        check_collisions()

    screen.fill((22, 30, 45))
    for y in range(0, HEIGHT, 80): pygame.draw.line(screen, (31, 42, 61), (0, y), (WIDTH, y), 1)
    for obj in objects: obj.draw(screen, font)
    player.draw(screen, font)
    centered_text(screen, font, f"Pontos: {score}", (100, 30))
    centered_text(screen, font, "A/D ou setas: escolha um portão", (WIDTH / 2, 30), (190, 205, 225))
    if game_over:
        centered_text(screen, big_font, "FIM DE JOGO", (WIDTH / 2, HEIGHT / 2 - 25), (255, 110, 100))
        centered_text(screen, font, "Pressione R para recomeçar", (WIDTH / 2, HEIGHT / 2 + 30))
    pygame.display.flip()

pygame.quit()
