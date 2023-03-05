from __future__ import annotations
from abc import ABC, abstractmethod

from config import FURYPUNCH_STAMINA, FURYPUNCH_DAMAGE, HARDSHOT_STAMINA, HARDSHOT_DAMAGE


# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения АБСТРАКТНЫЙ
    """
    def __init__(self):
        self.user = None
        self.target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina >= self.stamina

    def use(self, user, target) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f'{self.user.name} попытался использовать {self.name} но у него не хватило выносливости.'


class FuryPunch(Skill):
    name = 'Свирепый Пинок'
    stamina = FURYPUNCH_STAMINA
    damage = FURYPUNCH_DAMAGE

    def skill_effect(self) -> str:
        """
        Логика использования скилла -> return str
        в классе доступны экземпляры user и target - можно использовать любые их методы
        именно здесь происходит уменьшение стамины у игрока применяющего умение и
        уменьшение здоровья цели.
        Результат применения возвращается строкой.
        """
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage

        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона противнику.'

class HardShot(Skill):
    name = 'Мощный Укол'
    stamina = HARDSHOT_STAMINA
    damage = HARDSHOT_DAMAGE

    # Дублировано с FuryPunch.skill_effect() сознательно
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.hp -= self.damage

        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона противнику.'
