import json


class GameStats():
    """Отслеживание статистики игры."""

    def __init__(self, ai_settings):
        """Инициализация."""
        self.settings = ai_settings
        self.reset_stats()

        self.high_score = 0
        self.get_stored_high_score()
        self.save_high_score()

        # Игра в активном состоянии, если True. Запускается в неактивном состоянии, если в начале игры False
        self.game_active = False

    def reset_stats(self):
        """Инициализация статистики, изменяющейся в ходе игры."""
        self.starships_left = self.settings.starship_limit
        self.score = 0
        self.level = 1

    def get_stored_high_score(self):
        """Получает хранимое значение лучшего счета, если оно есть."""
        filename = 'high_score'
        try:
            with open(filename) as file:
                self.high_score = json.load(file)
        except FileNotFoundError:
            return None
        else:
            return self.high_score

    def save_high_score(self):
        filename = 'high_score'
        with open(filename, 'w') as file:
            json.dump(self.high_score, file)
        return self.high_score
