#!/usr/bin/env python3

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

# направления для быстрого перемешения
DIRECTIONS = ('north', 'south', 'east', 'west', 'up', 'down')

def process_command(game_state: dict, command: str) -> None:
    parts = command.split(maxsplit=1)
    cmd = parts[0] if parts else ''
    arg = parts[1] if len(parts) > 1 else ''

    if cmd in DIRECTIONS:  # north/south/etc без go
        move_player(game_state, cmd)
        return

    match cmd:
        case 'look':
            describe_current_room(game_state)
        case 'go':
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление: go <direction>")
        case 'take':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет: take <item>")
        case 'use':
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет: use <item>")
        case 'inventory':
            show_inventory(game_state)
        case 'help':
            show_help()
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'quit' | 'exit':
            print("До свидания!")
            game_state['game_over'] = True
        case '':
            pass
        case _:
            print("Неизвестная команда. Введите help для списка команд.")


def main() -> None:
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
