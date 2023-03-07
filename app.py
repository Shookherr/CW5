# Курсовая работа №5. Шумихин Алексей. 07.03.23
import sys
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from base import Arena
from unit import EnemyUnit, PlayerUnit
from equipment import Equipment
from classes import unit_classes

# Check Python version
if sys.version_info.major < 3:
    print(f'This Python version {sys.version_info.major}.{sys.version_info.minor} is outdated.'
          ' Please install Python version 3.xx(preferably 3.10 or newest).')
    exit(1)

app = Flask(__name__)

heroes = {
    'player': ...,
    'enemy': ...
}

arena = Arena()    # инициализация класса арены

# Инициализация глобальных списков
equipment = Equipment()
weapons = equipment.get_weapons_names()
armors = equipment.get_armors_names()


def result_parser(result: str) -> tuple:
    """
    Костылик
    для красивого фронта и чтоб не ломать остальной код
    """

    if '\n' in result:  # заплатка на пропуск хода
        res = result.split('\n')

        if res[1] == 'Ничья':
            res1 = 'Ничья'
            res2 = 'Ничья'
        elif res[1] == 'Игрок победил':
            res1 = f' {heroes["player"].name} победил'
            res2 = f' {heroes["enemy"].name} проиграл'
        elif res[1] == 'Противник победил':
            res1 = f' {heroes["player"].name} проиграл'
            res2 = f' {heroes["enemy"].name} победил'
        else:
            return res[0], res[1]
    else:
        res1 = f'{heroes["player"].unit_class.name} {heroes["player"].name} пропускает ход'
        res2 = result

    return res1, res2


@app.route("/")
def menu_page():
    """
    Рендер главного меню (шаблон index.html)
    """
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """
    Запуск функции start_game экземпляра класса арена с необходимыми аргументами
    Рендер экрана боя (шаблон fight.html)
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    Кнопка нанесения удара
    обновление экрана боя (нанесение удара) (шаблон fight.html)
    если игра идет - вызов метода player.hit() экземпляра класса арены
    если игра не идет - пропуск срабатывания метода (просто рендер шаблона с текущими данными)
    """

    (res1, res2) = result_parser(arena.player_hit())

    return render_template('fight.html', heroes=heroes, result=res1, turn_result=res2)


@app.route("/fight/use-skill")
def use_skill():
    """
    Кнопка использования скилла:
    логика практически идентична предыдущему эндпоинту
    """
    (res1, res2) = result_parser(arena.player_use_skill())

    return render_template('fight.html', heroes=heroes, result=res1, turn_result=res2)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Кнопка пропуск хода:
    """
    if not arena.game_is_running:
        return render_template("index.html")

    (res1, res2) = result_parser(arena.next_turn())

    return render_template('fight.html', heroes=heroes, result=res1, turn_result=res2)


@app.route("/fight/end-fight")
def end_fight():
    """
    Кнопка завершить игру - переход в главное меню
    """
    return render_template("index.html")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    Кнопка выбор героя. 2 метода GET и POST
    GET отрисовка формы.
    POST отправка формы и редирект на эндпоинт choose enemy
    """

    if request.method == 'GET':
        header = 'Выберите героя'
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверка, что класс с таким именем существует
        if not (unit_class_name in unit_classes.keys()):
            return f'Class "{unit_class_name}" not exists'

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Проверка наличия брони и оружия
        if not (armor_name in armors):
            return f'Armor "{armor_name}" not exists'
        if not (weapon_name in weapons):
            return f'Armor "{weapon_name}" not exists'

        armor = equipment.get_armor(armor_name)
        weapon = equipment.get_weapon(weapon_name)

        player.equip_armor(armor)
        player.equip_weapon(weapon)
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    Кнопка выбор соперников. 2 метода GET и POST
    также на GET отрисовка формы, а на POST отправка формы и редирект на начало битвы
    """
    if request.method == 'GET':
        header = 'Выберите противника'
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверка, что класс с таким именем существует
        if not (unit_class_name in unit_classes.keys()):
            return f'Class "{unit_class_name}" not exists'

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Проверка наличия брони и оружия
        if not (armor_name in armors):
            return f'Armor "{armor_name}" not exists'
        if not (weapon_name in weapons):
            return f'Armor "{weapon_name}" not exists'

        armor = equipment.get_armor(armor_name)
        weapon = equipment.get_weapon(weapon_name)

        enemy.equip_armor(armor)
        enemy.equip_weapon(weapon)
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(port=25000)
