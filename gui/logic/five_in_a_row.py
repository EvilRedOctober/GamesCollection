# -*- coding: utf-8 -*-


from gui.logic.abstracts import *
from games.five_in_a_row import *


class FiveCell(AbstractCell):
    """Abstract class for game form with basic logic."""

    # Paths to the icons
    ICONS = (None, ":/Icons/cross.png", ":/Icons/Naught.png")
    INNER_COLOR1 = QtGui.QColor(255, 225, 175)
    INNER_COLOR2 = INNER_COLOR1
    OUTER_COLOR = QtGui.QColor(150, 150, 150)
    HELP_COLOR = QtGui.QColor(100, 60, 10)

    def __init__(self, *args, **kwargs):
        super(FiveCell, self).__init__(*args, **kwargs)
        # To draw win line
        self.type_of_win_line = 0

    def paintEvent(self, *args, **kwargs):
        super(FiveCell, self).paintEvent(*args, **kwargs)
        if self.status == 2:
            p = QtGui.QPainter(self)
            p.setRenderHint(p.Antialiasing)
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
            pen.setWidth(4)
            p.setPen(pen)
            coords = [(0, 0, self.SIZE, self.SIZE),
                      (self.SIZE//2, 0, self.SIZE//2, self.SIZE),
                      (0, self.SIZE//2, self.SIZE, self.SIZE//2),
                      (0, self.SIZE, self.SIZE, 0)][self.type_of_win_line]
            p.drawLines(QtCore.QLine(*coords))


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
            "Цель игры — первым построить фигурами своей формы непрерывный ряд из пяти фигур в горизонтальном, " \
            "вертикальном или диагональном направлении.\nЕсли доска заполнена и ни один из игроков не построил " \
            "ряд из пяти фигур, может быть объявлена ничья."
    Board_Class = Five_in_a_row
    Cell_Class = FiveCell

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(FiveForm, self).__init__(parent)
        self.setup_form()

    def apply_move(self, x, y):
        super(FiveForm, self).apply_move(x, y)
        # Needs to mark cells to draw win line
        if self.party.board.is_win:
            # Special attribute
            poses = self.party.board.win_pos
            # To get the line direction (diagonal, vertical, horizontal, reverse diagonal)
            direction = (poses[1][0] - poses[0][0], poses[1][1] - poses[0][1])
            type_of_win_line = [(1, 1), (1, 0), (0, 1), (1, -1)].index(direction)
            for x, y in poses:
                self.boardField.itemAtPosition(x, y).widget().status = 2
                self.boardField.itemAtPosition(x, y).widget().type_of_win_line = type_of_win_line
