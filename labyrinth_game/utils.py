#!/usr/bin/env python3

import math

from labyrinth_game.constants import (
    COMMANDS,
    DAMAGE_RANGE,
    DEATH_THRESHOLD,
    EVENT_PROBABILITY,
    EVENT_TYPES_COUNT,
    ROOMS,
)
from labyrinth_game.player_actions import get_input


def pseudo_random(seed: int, modulo: int) -> int:
    """Генерит псевдослучайное число через sin."""
    x = math.sin(seed * 9.1111) * 10000.0
    frac = x - math.floor(x)
    return int(frac * modulo)

def trigger_trap(game_state: dict) -> None:
    # ловушка - Loss предмета или урон
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']

    if inventory:
        # теряем случайный предмет
        index = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли: {lost_item}")
    else:
        # урон игроку
        damage = pseudo_random(steps, DAMAGE_RANGE)
        if damage < DEATH_THRESHOLD:
            print("Ловушка оказалась смертельной. Вы проиграли!")
            game_state['game_over'] = True
        else:
            print("Вам удалось уцелеть!")

def random_event(game_state: dict) -> None:
    """Рандомые события"""
    steps = game_state['steps_taken']

    if pseudo_random(steps, EVENT_PROBABILITY) != 0:
        return  # ничего не произошло

    event_type = pseudo_random(steps + 1, EVENT_TYPES_COUNT)
    room_name = game_state['current_room']
    inventory = game_state['player_inventory']

    if event_type == 0:
        # находка
        print("Вы замечаете на полу блестящую монетку!")
        ROOMS[room_name]['items'].append('coin')
    elif event_type == 1:
        # испуг
        print("Вы слышите странный шорох в темноте...")
        if 'sword' in inventory:
            print("Вы взмахиваете мечом и отпугиваете существо!")
    else:
        # ловушка в trap_room без факела
        if room_name == 'trap_room' and 'torch' not in inventory:
            print("В темноте вы не заметили ловушку!")
            trigger_trap(game_state)


def describe_current_room(game_state: dict) -> None:
    """показывает где мы находимся"""
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        items_str = ', '.join(room['items'])
        print(f"Заметные предметы: {items_str}")

    exits_str = ', '.join(room['exits'].keys())
    print(f"Выходы:{exits_str}")
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help() -> None:
    print("\n\n Доступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")


def solve_puzzle(game_state: dict) -> None:
    from labyrinth_game.player_actions import get_input

    room_name = game_state['current_room']
    room = ROOMS[room_name]

    if room_name == 'treasure_room' and 'treasure_chest' in room['items']:
        attempt_open_treasure(game_state)
        return

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ")

    # варианты ответов которые тоже считаются правильными
    alt = {'10': ['10', 'десять', 'ten'], '5': ['5', 'пять', 'five']}
    alt['шаг шаг шаг'] = ['шаг шаг шаг']
    alt['резонанс'] = ['резонанс', 'голод']

    correct_answers = alt.get(answer, [answer.lower()])
    is_correct = user_answer in [a.lower() for a in correct_answers]

    if is_correct:
        print("Верно! Загадка решена.")
        ROOMS[room_name]['puzzle'] = None
        if room_name == 'hall':
            print("Пьедестал открывается, внутри древняя карта!")
        elif room_name == 'library':
            print("Свиток рассыпается, но вы запомнили подсказку!")
        elif room_name == 'cellar':
            print("Надпись исчезает, открывая тайник!")
        else:
            print("Вы получаете награду за смекалку!")
    else:
        print("Неверно. Попробуйте снова.")
        # в trap_room неверный ответ вызывает ловушку
        if room_name == 'trap_room':
            print("Неверный ответ активировал ловушку!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    """Откр. сундука"""
    room = ROOMS['treasure_room']
    inventory = game_state['player_inventory']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт. У вас нет ключа.")
    choice = get_input("Ввести код? (да/нет): ")

    if choice == 'да':
        puzzle = room['puzzle']
        if puzzle:
            print(puzzle[0])
            code = get_input("Код: ")
            if code == puzzle[1].lower():
                print("Код верный! Сундук открыт!")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")
