# GamesCollection

Коллекция настольных игр для двух игроков.
Имеется возможность выбора из 5 игр и настройки размера игрового поля для некоторых из них.
Поддерживается игра с компьютером на разных уровнях сложнсти.
Для работы логики компьютерного соперника реализованы эвристики вместе с методами минимакса и альфа-бета отсечения.


## Список игр
* Пять в ряд (гомоку)
* Заяц и волки             
* Реверси (отелло)
* Шашки
* Мельница

## Запуск приложения
Программы были написаны при использовании Python 3.9
1. Установить требования

`pip install -r requirements.txt`

2. Запустить главный скрипт

`python main.pyw`


## Краткое описание структуры проекта
```
basic/                   # Базовая логика основных функций приложения
games/                   # Классы игровых досок (с правилами, эвристикой и т.д.) и фигур
games/ai/                # Функции с реализацией логики компьютера (минимакс и альфа-бета отсечение)
gui/                     # Модули графического пользовательского интерфейса
gui/forms/               # Содержит скомпилированные ui файлы (классы форм с графическим интерфейсом)
gui/logic/               # Классы форм со встроенной логикой
resources/               # Файлы используемых ресурсов
resources/forms_ui/      # ui файлы с формами Qt
resources/icons/         # Иконки и картинки

forms_resources_rc.py    # Скомпилированный файл ресурсов
main.pyw              # Основной файл
```