# -*- coding: utf-8 -*-


from gui.logic.abstracts import *
from games.five_in_a_row import *


class FiveCell(AbstractCell):
    """Abstract class for game form with basic logic."""

    # Paths to the icons
    ICONS = (None, ":/Icons/cross.png", ":/Icons/Naught.png")
    OUTER_COLOR = QtCore.Qt.lightGray
    INNER_COLOR1 = QtGui.QColor(225, 200, 175)
    INNER_COLOR2 = INNER_COLOR1


class FiveForm(AbstractGameForm):
    DIFFICULTY_LEVELS = {'Легко': {'randomizing': 20}, 'Среднее': {'randomizing': 5}, 'Сложно': {'randomizing': 0}}
    BOARD_SIZES = ('15', '19')
    PLAYERS = ('Крестики', 'Нолики')
    RULES = "Пять в ряд (Гомоку).\n\n" \
            "Игра ведётся на квадратном поле («доске»), расчерченном вертикальными и горизонтальными линиями." \
            "Пересечения линий называются «пунктами». Наиболее распространённым является поле размером 15×15 " \
            "линий.\nИграют две стороны — «крестики» и «нолики». Каждая сторона использует свои собственные" \
            " фишки.\nКаждым ходом игрок выставляет фишку своей формы в один из свободных пунктов доски. " \
            "Первый ход делают крестикие в центральный пункт доски. Далее ходы делаются по очереди.\n" \
            "Цель игры — первым построить камнями своего цвета непрерывный ряд из пяти камней в горизонтальном, " \
            "вертикальном или диагональном направлении.\nЕсли доска заполнена и ни один из игроков не построил " \
            "ряд из пяти камней, может быть объявлена ничья."
    Board_Class = Five_in_a_row
    Cell_Class = FiveCell

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(FiveForm, self).__init__(parent)
        self.setup_form()
