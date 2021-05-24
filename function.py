import sys
import pygame
from bullet.bullet_class import Bullet
from alien.alien_class import Alien
from star.star_class import Star
import random
from time import sleep


# ОБНОВЛЕНИЕ ЭКРАНА И ВЗАИМОДЕЙСТВИЕ С КЛАВИАТУРОЙ

def check_keydown_events(event, ai_settings, stats, sb, screen, aliens, starship, bullets, stars):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        starship.moving_right = True
    elif event.key == pygame.K_LEFT:
        starship.moving_left = True
    elif event.key == pygame.K_UP:
        starship.moving_up = True
    elif event.key == pygame.K_DOWN:
        starship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, starship, bullets)
    elif event.key == pygame.K_ESCAPE:
        stats.save_high_score()
        sys.exit()
    elif stats.game_active == False and event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, starship, bullets, aliens, stars)


def check_keyup_events(event, starship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        starship.moving_right = False
    elif event.key == pygame.K_LEFT:
        starship.moving_left = False
    elif event.key == pygame.K_UP:
        starship.moving_up = False
    elif event.key == pygame.K_DOWN:
        starship.moving_down = False


def check_events(ai_settings, screen, stats, sb, starship, bullets, aliens, play_button, stars):
    """Отслеживание событий клавиатуры и мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, aliens, starship, bullets, stars)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, starship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, starship, bullets, aliens, stars,
                              play_button, mouse_x, mouse_y)


def start_game(ai_settings, screen, stats, sb, starship, bullets, aliens, stars):
    """Сброс игры на начало."""
    stats.reset_stats()
    sb.prep_score()
    sb.prep_high_score()  # - непонятно зачем?
    sb.prep_level()
    sb.prep_lifes()
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()
    aliens.empty()
    bullets.empty()
    stars.empty()
    create_star_sky(ai_settings, screen, stars)
    create_fleet(ai_settings, screen, starship, aliens)
    starship.center_starship()


def check_play_button(ai_settings, screen, stats, sb, starship, bullets, aliens, stars,
                      play_button, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнокпи PLay."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Скрытие указателя мыши
        pygame.mouse.set_visible(False)
        start_game(ai_settings, screen, stats, sb, starship, bullets, aliens, stars)


def update_screen(ai_settings, screen, stats, sb, stars, starship,
                  aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран"""
    screen.fill(ai_settings.bg_color)  # Перерисовка экрана в соответсвиии с заданным цветом bg_color

    # Все снаряды выводятся позади изображений корабля
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for star in stars.sprites():
        star.draw_star()
    starship.blitme()
    aliens.draw(screen)
    sb.show_score()

    # Кнопка PLay отображается только в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def check_high_score(stats, sb):
    """Проверяет появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


# РАБОТА С ВЫЛЕТАЮЩИМИ СНАРЯДАМИ

def update_bullets(ai_settings, screen, stats, sb, starship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули"""
    bullets.update()
    # Удаление снарядов, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_alien_collisions(ai_settings, screen, stats, sb, starship, aliens, bullets)


def check_bullets_alien_collisions(ai_settings, screen, stats, sb, starship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами."""
    # Проверка попаданий в пришельцев
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Если весь флот уничтожен, то начинается новый уровень
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, starship, aliens)
        stats.level += 1
        sb.prep_level()


def fire_bullet(ai_settings, screen, starship, bullets):
    """Выпускает снаряд, если максимум еще не достигнут"""
    # Создание нового снаряда при включении его в группу bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, starship)
        bullets.add(new_bullet)


# РАБОТА С ПРОТИВНИКАМИ

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, starship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - starship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, starship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду
    # Интервал между приешльцами равен одной ширине пришельца

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, starship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещение его в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def ship_hit(ai_settings, stats, sb, screen, starship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.starships_left > 1:
        # Уменьшение ships_left
        stats.starships_left -= 1
        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()
        sb.prep_lifes()
        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, starship, aliens)
        starship.center_starship()
        # Пауза
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, starship, aliens, bullets):
    """Проверяет добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что и при столкновении с кораблем
            ship_hit(ai_settings, stats, sb, screen, starship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, starship, aliens, bullets):
    """Обновляет позиции всех пришельцев в флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка коллизий "Пришелец - корабль"
    if pygame.sprite.spritecollideany(starship, aliens):
        ship_hit(ai_settings, stats, sb, screen, starship, aliens, bullets)

    # Прверка пришельцев добравшихся до нижнего края экрана
    check_aliens_bottom(ai_settings, stats, sb, screen, starship, aliens, bullets)


# РАБОТА С ДВИЖЕНИЕМ ПРОТИВНИКОВ

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Двигает флот вниз и меняет его направление."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


# РАБОТА С БЭКГРАУНДОМ "ЗВЕЗДЫ"

def create_star(ai_settings, screen, stars):
    """Создает одну звезду в произвольной координате X."""
    star = Star(ai_settings, screen)
    star.rect.x = random.randint(0, ai_settings.screen_width)
    star.rect.y = 0
    stars.add(star)


def create_star_sky(ai_settings, screen, stars):
    """Создает ряд из звезд у верхнего края экрана."""
    for number in range(2):
        create_star(ai_settings, screen, stars)


def check_stars(ai_settings, screen, stars):
    for star in stars.copy():
        if star.check_star_y() and len(stars) < ai_settings.stars_allowed:
            create_star(ai_settings, screen, stars)


def stars_update(stars, ai_settings, screen):
    """Обновляет позиции звезд и удаляет старые звезды."""
    check_stars(ai_settings, screen, stars)
    stars.update()
    for star in stars.copy():
        if star.rect.y >= ai_settings.screen_height:
            stars.remove(star)