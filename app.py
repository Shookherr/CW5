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
    "Player": ...,
    "Enemy": ...
}

arena =  Arena() # инициализация класса арены


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
    arena.start_game(player=heroes['Player'], enemy=heroes['Enemy'])
    return render_template('fight.html', heroes=heroes)

@app.route("/fight/hit")
def hit():
    """
    Кнопка нанесения удара
    обновление экрана боя (нанесение удара) (шаблон fight.html)
    если игра идет - вызов метода player.hit() экземпляра класса арены
    если игра не идет - пропуск срабатывания метода (просто рендер шаблона с текущими данными)
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Кнопка использования скилла:
    логика практически идентична предыдущему эндпоинту
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Кнопка пропуск хода:
    логика практически идентична предыдущему эндпоинту, но
    здесь вызывается функция следующего хода (arena.next_turn())
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    Кнопка завершить игру - переход в главное меню
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    Кнопка выбор героя. 2 метода GET и POST
    GET отрисовка формы.
    POST отправка формы и редирект на эндпоинт choose enemy
    """
    if request.method == 'GET':
        header = 'Выберите героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
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

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Обработка отсутствующей брони и оружия
        print(armor_name)
        print(type(armor_name))
        exit()
        print(weapon_name)
        exit()

        player.equip_armor(Equipment.get_armor(armor_name))
        player.equip_weapon(Equipment.get_weapon(weapon_name))
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
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
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

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Обработка отсутствующей брони и оружия

        enemy.equip_armor(Equipment.get_armor(armor_name))
        enemy.equip_weapon(Equipment.get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(port=25000)
