import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Класс, представляющий звезды."""

    def __init__(self, ai_settings, screen):
        """Инизиализирует звезду и задает начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = ai_settings

        # self.image = pygame.image.load('image/star.bmp')
        self.rect = pygame.Rect(0, 0, ai_settings.star_width, ai_settings.star_height)
        self.color = ai_settings.star_color
        self.drop_factor = ai_settings.stars_drop_speed
        self.increment = ai_settings.stars_increment_x

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает звезды."""
        self.y += self.drop_factor
        self.rect.y = self.y

    def check_star_y(self):
        """Проверяет координату "У" линии звезд."""
        if self.rect.y == 50:
            return True

    def draw_star(self):
        """Вывод звезды на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)