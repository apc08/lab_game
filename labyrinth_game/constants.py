#!/usr/bin/env python3

ROOMS = {
    'entrance': {
        'description': (
            'Вы в темном входе лабиринта. '
            'Стены покрыты мхом. На полу лежит старый факел.'
        ),
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': (
            'Большой зал с эхом. '
            'По центру стоит пьедестал с запечатанным сундуком.'
        ),
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". '
            'Введите ответ цифрой или словом.',
            '10'
        )
    },
    'trap_room': {
        'description': (
            'Комната с хитрой плиточной поломкой. '
            'На стене видна надпись: "Осторожно — ловушка".'
        ),
        'exits': {'west': 'entrance', 'south': 'secret_passage'},
        'items': ['rusty_key'],
        'puzzle': (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" '
            'три раза подряд (введите "шаг шаг шаг")',
            'шаг шаг шаг'
        )
    },
    'library': {
        'description': (
            'Пыльная библиотека. На полках старые свитки. '
            'Где-то здесь может быть ключ от сокровищницы.'
        ),
        'exits': {'east': 'hall', 'north': 'armory'},
        'items': ['ancient_book'],
        'puzzle': (
            'В одном свитке загадка: "Что растет, когда его съедают?" '
            '(ответ одно слово)',
            'резонанс'
        )
    },
    'armory': {
        'description': (
            'Старая оружейная комната. На стене висит меч, '
            'рядом — небольшая бронзовая шкатулка.'
        ),
        'exits': {'south': 'library', 'down': 'cellar'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None
    },
    'treasure_room': {
        'description': (
            'Комната, на столе большой сундук. '
            'Дверь заперта — нужен особый ключ.'
        ),
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': (
            'Дверь защищена кодом. Введите код '
            '(подсказка: это число пятикратного шага, 2*5= ? )',
            '10'
        )
    },
    'secret_passage': {
        'description': (
            'Узкий тайный проход. Пахнет сыростью. '
            'На полу валяется старый ключ от сокровищницы.'
        ),
        'exits': {'north': 'trap_room'},
        'items': ['treasure_key'],
        'puzzle': None
    },
    'cellar': {
        'description': (
            'Темный подвал. В углу стоят пустые бочки. '
            'На стене нацарапана странная надпись.'
        ),
        'exits': {'up': 'armory'},
        'items': ['rope'],
        'puzzle': (
            'Надпись гласит: "Сколько букв в слове ответ?"',
            '5'
        )
    }
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "north/south/...": "быстрое перемещение без go",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение",
}

EVENT_PROBABILITY = 10
EVENT_TYPES_COUNT = 3
DAMAGE_RANGE = 10
DEATH_THRESHOLD = 3  # если damage меньше этого - Loss
