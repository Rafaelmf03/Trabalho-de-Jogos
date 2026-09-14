import pygame


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class EventHandler:
    """Canal simples de eventos usado para a comunicação entre objetos."""
    def __init__(self): self.observers = {}
    def subscribe(self, event_type, callback): self.observers.setdefault(event_type, []).append(callback)
    def notify(self, event_type, data=None):
        for callback in self.observers.get(event_type, []): callback(data)
    def clear(self): self.observers.clear()


def circle_collision(p1, r1, p2, r2):
    return pygame.Vector2(p1).distance_to(pygame.Vector2(p2)) <= r1 + r2


def centered_text(screen, font, text, pos, color=(255, 255, 255)):
    image = font.render(str(text), True, color)
    screen.blit(image, image.get_rect(center=pos))
