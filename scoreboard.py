import pygame.font
from pygame.sprite import Group
from ship.life_class import ShipLife


class Scoreboard:
    """Класс для вывода игровой информации и статистики."""

    def __init__(self, ai_settings, screen, stats):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = ai_settings
        self.stats = stats

        # Настройки шрифта для вывода счета
        self.text_color = 225, 225, 225
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lifes()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней чайсти экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Выводит счет, рекорд и число оставшихся кораблей на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lifes.draw(self.screen)

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        # Рекорд выравнивается по центру с верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует счетчик уровня в изображение."""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.settings.bg_color)
        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lifes(self):
        """Количество оставшихся жизней."""
        self.lifes = Group()
        for life_num in range(self.stats.starships_left):
            life = ShipLife()
            life.rect.x = 20 + life_num * life.rect.width
            life.rect.y = 10
            self.lifes.add(life)
