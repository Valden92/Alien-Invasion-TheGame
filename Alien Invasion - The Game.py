import pygame
from pygame.sprite import Group
from settings.settings import Settings_AI
from ship.ship_class import StarShip
from game_stats import GameStats
from button.button import Button
from scoreboard import Scoreboard
import function as gf


def run_game():
    """Инициализирует игру и создает объект экрана."""
    pygame.init()
    ai_settings = Settings_AI()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_icon(ai_settings.icon)
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # Создание кнопки Play
    play_button = Button(screen, "Press P for Start")

    # Создание экземпляров статистики и вывода счета
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание корабля
    starship = StarShip(ai_settings, screen)

    # Создание групп хранения
    bullets = Group()
    stars = Group()
    aliens = Group()
    gf.create_star_sky(ai_settings, screen, stars)
    gf.create_fleet(ai_settings, screen, starship, aliens)

    # Запуск основного цикла игры
    while True:
        clock.tick(300)
        gf.check_events(ai_settings, screen, stats, sb, starship, bullets, aliens, play_button, stars)
        gf.update_screen(ai_settings, screen, stats, sb, stars, starship,
                         aliens, bullets, play_button)
        if stats.game_active:
            starship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, starship, aliens, bullets)
            gf.stars_update(stars, ai_settings, screen)
            gf.update_aliens(ai_settings, stats, sb, screen, starship, aliens, bullets)


run_game()
