from typing import Optional

from config import STAMINA_PER_ROUND_VALUE, ROUND
from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:   # есть такой класс?
            instance = super().__call__(*args, **kwargs)    # создание
            cls._instances[cls] = instance
        return cls._instances[cls]  # возврат существующего класса


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = STAMINA_PER_ROUND_VALUE
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """
        НАЧАЛО ИГРЫ -> None
        присваивание экземпляру класса атрибуты "игрок" и "противник"
        а также установка True для свойства "началась ли игра"
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        """
        ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        и возвращение результата строкой:
        Возможны три результата:
        - Игрок проиграл битву;
        - Игрок выиграл битву;
        - Ничья и сохранение его в атрибуте (self.battle_result).
        Если здоровье игроков в порядке, то ничего не происходит.
        """
        pl_hp = self.player.hp  # здоровье игрока
        en_hp = self.enemy.hp   # здоровье компьютера
        if pl_hp > 0.0 and en_hp > 0.0:
            return None

        if pl_hp <= 0.0 and en_hp <= 0.0:
            self.battle_result = 'Ничья'
        elif pl_hp <= 0.0:
            self.battle_result = 'Противник победил'
        else:
            self.battle_result = 'Игрок победил'

        return self._end_game()

    def _stamina_regeneration(self):
        """
        Регенерация выносливости для игрока и врага за кон
        в этом методе к количеству выносливости игрока и врага прибавляется константное значение.
        Главное - чтобы оно не превысило максимальные значения (используется if)
        """
        units = (self.player, self.enemy)

        for unit in units:
            unit.stamina += self.STAMINA_PER_ROUND

            if unit.stamina > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina

            unit.stamina = round(unit.stamina, ROUND)

    def next_turn(self) -> str:
        """
        СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        срабатывает, когда игрок пропускает ход, или когда игрок наносит удар.
        Создаётся поле result и проверяется, что вернется в результате функции self._check_players_hp.
        Если result -> его возврат
        если же результата пока нет и после завершения хода игра продолжается,
        тогда запускается процесс регенерации выносливости для игроков (self._stamina_regeneration)
        и вызывается функция self.enemy.hit(self.player) - ответный удар врага
        """
        result = self._check_players_hp()   # проверка здоровья игроков в начале кона
        if result is not None:
            return result   # собственно, конец игры
        if self.game_is_running:    # игра продолжается? - можно и не проверять
            result = self.enemy.hit(self.player)     # атака противника
            self._stamina_regeneration()    # восстановление игроков
            return result

    def _end_game(self) -> str:
        """
        КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        очистка синглтона - self._instances = {},
        остановка игры (game_is_running),
        возврат результата.
        """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """
        КНОПКА УДАР ИГРОКА -> return result: str
        получение результата от функции self.player.hit
        запуск следующего хода
        возврат результата удара строкой
        """

        result = self.player.hit(self.enemy)    # удар игрока
        turn_result = self.next_turn()
        return f'{result}\n{turn_result}'

    def player_use_skill(self) -> str:
        """
        КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        получение результата от функции self.use_skill
        включение следующего хода
        возврат строкой результата удара
        """
        result = self.player.use_skill(self.enemy)  # удар игрока
        turn_result = self.next_turn()
        return f'{result}\n{turn_result}'
