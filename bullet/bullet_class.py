import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управление боевыми снарядами корабля."""

    def __init__(self, ai_settings, screen, starship):
        """Создает снаряды в текущей позиции корабля."""
        super().__init__()
        self.screen = screen

        # Создание снаряда в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = starship.rect.centerx
        self.rect.top = starship.rect.top

        # Сохранение позиции снаряда в вещественном формате
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Перемещает снаряды в вещественном формате."""
        # Обновление позиции в вещественном формате
        self.y -= self.speed_factor
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)