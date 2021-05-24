import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий пришельца."""

    def __init__(self, ai_settings, screen):
        """Инициализирует пришельца и задает начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = ai_settings

        self.image = pygame.image.load('image/alien.png')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в верхнем левом углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает пришельца."""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True