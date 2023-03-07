from marshmallow_dataclass import dataclass

from skills import Skill, FuryPunch, HardShot
from config import WARRIOR_MAX_HEALTH, WARRIOR_MAX_STAMINA, WARRIOR_ATTACK, WARRIOR_STAMINA, WARRIOR_ARMOR, \
    THIEF_MAX_HEALTH, THIEF_MAX_STAMINA, THIEF_ATTACK, THIEF_STAMINA, THIEF_ARMOR


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name='Громила',
    max_health=WARRIOR_MAX_HEALTH,
    max_stamina=WARRIOR_MAX_STAMINA,
    attack=WARRIOR_ATTACK,
    stamina=WARRIOR_STAMINA,
    armor=WARRIOR_ARMOR,
    skill=FuryPunch()
)

ThiefClass = UnitClass(
    name='Воришка',
    max_health=THIEF_MAX_HEALTH,
    max_stamina=THIEF_MAX_STAMINA,
    attack=THIEF_ATTACK,
    stamina=THIEF_STAMINA,
    armor=THIEF_ARMOR,
    skill=HardShot()
)


unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
