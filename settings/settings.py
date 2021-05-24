import pygame


class Settings_AI:
    """Класс для хранения настроек игры."""

    def __init__(self):
        """Инициализирует статические настройки игры."""

        # Параметры экрана:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)  # Задание цвета фонового окна
        self.icon = pygame.image.load('image/icon.png')

        # Параметры корабля
        self.starship_speed_factor = 1.5
        self.starship_limit = 3

        # Параметры снарядов
        self.bullet_speed_factor = 2
        self.bullet_width = 5
        self.bullet_height = 7
        self.bullet_color = 20, 200, 60
        self.bullets_allowed = 100

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 - вправо, -1 - влево

        # Настройки звезд
        self.star_width = 2
        self.star_height = 2
        self.star_color = 255, 255, 255
        self.stars_drop_speed = 1
        self.stars_increment_x = 0.5
        self.stars_allowed = 50

        # Темп ускорения игры
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Инициализирует динамические настройки игры."""
        self.starship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 2000

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев."""
        self.starship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
