import pygame
from pygame.sprite import Sprite

class StarShip(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения корабля и получение фигуры.
        self.image = pygame.image.load('image/starship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Пусть каждый новый корабль появляется у нижнего края экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра коробля
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

    def update(self):
        """Обновляет позицию корабля с учетом флага."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.starship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.starship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.starship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.starship_speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_starship(self):
        """Размещает корабль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
