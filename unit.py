from __future__ import annotations
from abc import ABC, abstractmethod

from config import ROUND
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита - Абстрактный
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.is_skill_used = ...

    @property
    def health_points(self) -> float:
        return round(self.hp, ROUND)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, ROUND)

    def equip_weapon(self, weapon: Weapon):
        """
        Выбор оружия для героя
        """
        self.weapon = weapon


    def equip_armor(self, armor: Armor):
        """
        Выбор брони для героя
        """
        self.armor = armor


    def _count_damage(self, target: BaseUnit) -> float:
        """
        Расчёт удара - урон игрока.
        """
        self.stamina -= self.weapon.stamina_per_hit     # уменьшение запаса сил нападающего при ударе
        damage = self.weapon.damage * self.unit_class.attack    # базовый урон

        stam_armor = target.armor.stamina_per_turn * target.unit_class.stamina  # затраты выносливости на броню
        # Есть ли силы у защищающегося использовать броню
        if target.stamina >= stam_armor:
            # Расчёт остатков сил у защищающегося
            target.stamina -= stam_armor
            if target.stamina < 0.0:
                target.stamina = 0.0    # перевыдохся
            # Расчётный итоговый урон с учётом брони и умения ею пользоваться
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, ROUND)   # округление - окончательный расчёт

        if damage < 0.0:
            damage = 0.0

        target.get_damage(damage)       # получение урона и расчёт остатков здоровья
        return damage

    def get_damage(self, damage: int):
        """
        Получение урона целью
        """
        # новое значение для аттрибута self.hp
        if damage > 0.0:
            self.hp -= damage
        if self.hp < 0.0:   # completely dead?
            self.hp = 0.0   # is dead...


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращает строку 'Навык использован'
        Если же умение не использовано, то тогда выполняет функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет строку, которая характеризует выполнение умения
        """
        if self.is_skill_used:
            return 'Навык использован'
        else:
            res = self.unit_class.skill.use(self,target)
            self.is_skill_used = True
            return res


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target),
        а также возвращается результат в виде строки.
        """
        # Использование спецудара
        if not self.is_skill_used:  # ещё не задействован
            if self.stamina >= self.unit_class.skill.stamina:   # силы есть на спецудар
                if randint(0, 100) < 10:    # то с вероятностью 0.1
                    return self.use_skill(target)   # применение спецудара

        if self.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'

        damage = self._count_damage(target)

        if damage > 0.0:
            return f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит ' \
                   f'{damage} урона.'

        return f'{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} соперника его' \
                   ' останавливает.'

class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'

        damage = self._count_damage(target)
        if damage > 0.0:
            return f'{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} ' \
                   'урона.'

        return  f'{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его' \
                ' останавливает.'
