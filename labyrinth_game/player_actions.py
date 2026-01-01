#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS


def show_inventory(game_state: dict) -> None:
    inventory = game_state['player_inventory']
    if inventory:
        items_str = ', '.join(inventory)
        print(f"Инвентарь: {items_str}")
    else:
        print("Инвентарь пуст.")


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    """Идем в указанную сторону"""
    from labyrinth_game.utils import describe_current_room, random_event

    current_room = game_state['current_room']
    exits = ROOMS[current_room]['exits']

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    # treasure_room требует  ключ
    if next_room == 'treasure_room':
        if 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_items:
        room_items.remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case 'torch':
            print("Вы зажигаете факел. Стало светлее!")
        case 'sword':
            print("Вы взмахиваете мечом. Чувствуете себя увереннее!")
        case 'bronze_box':
            print("Вы открываете бронзовую шкатулку...")
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Внутри вы нашли ржавый ключ!")
            else:
                print("Шкатулка пуста.")
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")
