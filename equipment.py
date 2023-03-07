from dataclasses import dataclass
from typing import Optional
from random import uniform
from marshmallow_dataclass import class_schema
import marshmallow
import json
import codecs

from config import ROUND


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        # расчёт наносимого повреждения
        damage = uniform(self.min_damage, self.max_damage)
        return round(damage, ROUND)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    # Содержит 2 списка - с оружием и с броней
    # описание общей структуры equipment.json
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self):
        self.equipment_ = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        """
        Возвращает объект оружия по имени
        """
        for weapon in self.equipment_.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name) -> Optional[Armor]:
        """
        Возвращает объект брони по имени
        """
        for armor in self.equipment_.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        """
        Возвращает список названий оружия
        """
        return [
            weapon.name for weapon in self.equipment_.weapons
        ]

    def get_armors_names(self) -> list:
        """
        Возвращает список названий брони
        """
        return [
            armor.name for armor in self.equipment_.armors
        ]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        Загрузка json в переменную EquipmentData
        """
        with codecs.open('./data/equipment.json', 'r', 'utf-8-sig') as file:
            data = json.load(file)
            equipment_schema = class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
