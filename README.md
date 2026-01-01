# Лабиринт сокровищ

Текстовая adventure игра на Python. Исследуйте древний лабиринт, собирайте предметы, решайте загадки и найдите сокровище!

## Установка

```bash
make install
# или
poetry install
```

## Запуск

```bash
make project
# или
poetry run project
```

## Команды игры

| Команда | Описание |
|---------|----------|
| `go <direction>` | Перейти в направлении (north/south/east/west) |
| `north/south/...` | Быстрое перемещение без go |
| `look` | Осмотреть текущую комнату |
| `take <item>` | Поднять предмет |
| `use <item>` | Использовать предмет из инвентаря |
| `inventory` | Показать инвентарь |
| `solve` | Решить загадку в комнате |
| `help` | Показать список команд |
| `quit` | Выйти из игры |

## Демонстрация

<!-- Вставьте ссылку на asciinema здесь -->
<!-- [![asciicast](https://asciinema.org/a/YOUR_ID.svg)](https://asciinema.org/a/YOUR_ID) -->

## Проверка кода

```bash
make lint
```
