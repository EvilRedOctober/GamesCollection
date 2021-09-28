# -*- coding: utf-8 -*-


from gui.logic.abstracts import *
from games.reversi import *


class ReversiCell(AbstractCell):
    """Abstract class for game form with basic logic."""

    # Paths to the icons
    ICONS = (None, ":/Icons/yellowStone.png", ":/Icons/blueStone.png")
    INNER_COLOR1 = QtGui.QColor(200, 200, 200)
    INNER_COLOR2 = QtGui.QColor(250, 250, 250)
    OUTER_COLOR = QtGui.QColor(50, 50, 50)
    LAST_TURN_COLOR = QtGui.QColor(250, 0, 0)

    def paintEvent(self, *args, **kwargs):
        super(ReversiCell, self).paintEvent(*args, **kwargs)
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)
        if self.status == 2:
            pen = QtGui.QPen(self.LAST_TURN_COLOR)
            pen.setWidth(2)
            p.setPen(pen)
            p.drawRect(2, 2, self.SIZE - 4, self.SIZE - 4)


class ReversiForm(AbstractGameForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0}, 'Среднее': {'max_depth': 2}, 'Сложно': {'max_depth': 3}}
    BOARD_SIZES = ('8', '10', '12')
    PLAYERS = ('Жёлтые', 'Фиолетовые')
    RULES = "Реверси (0телло).\n\n" \
            "В игре используется квадратная доска и специальные фишки, окрашенные с разных сторон в " \
            "контрастные цвета. Один из игроков играет жёлтыми, другой — фиолетовыми. Делая ход, игрок ставит " \
            "фишку на клетку доски «своим» цветом вверх. \nВ начале игры в центр доски выставляются 4 фишки в центр." \
            "\nПервый ход делают жёлтые. Далее игроки ходят по очереди.\nДелая ход, игрок должен поставить свою фишку" \
            " на одну из клеток доски таким образом, чтобы между этой поставленной фишкой и одной из имеющихся уже на" \
            " доске фишек его цвета находился непрерывный ряд фишек соперника, горизонтальный, вертикальный или " \
            "диагональный (другими словами, чтобы непрерывный ряд фишек соперника оказался «закрыт» фишками игрока " \
            "с двух сторон). Все фишки соперника, входящие в «закрытый» на этом ходу ряд, переворачиваются на другую " \
            "сторону (меняют цвет) и переходят к ходившему игроку.\nЕсли в результате одного хода «закрывается» " \
            "одновременно более одного ряда фишек противника, то переворачиваются все фишки, оказавшиеся на " \
            "всех «закрытых» рядах.\nИгрок вправе выбирать любой из возможных для него ходов. Если игрок имеет " \
            "возможные ходы, он не может отказаться от хода. Если игрок не имеет допустимых ходов, " \
            "то ход передаётся сопернику.\nИгра прекращается, когда на доску выставлены все фишки или когда " \
            "ни один из игроков не может сделать хода. По окончании игры проводится подсчёт фишек каждого цвета, " \
            "и игрок, чьих фишек на доске выставлено больше, объявляется победителем. В случае равенства количества " \
            "фишек засчитывается ничья."
    Board_Class = Reversi
    Cell_Class = ReversiCell

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(ReversiForm, self).__init__(parent)
        self.setup_form()

    def update_values(self):
        available_moves = set(self.party.board.legal_moves)
        for i in reversed(range(self.boardField.count())):
            w = self.boardField.itemAt(i).widget()
            value = self.party.board.get_value(w.x, w.y)
            w.value = value
            if value:
                w.isAvailable = False
            if (w.x, w.y) in available_moves:
                w.status = 1
                w.isAvailable = True
            else:
                w.isAvailable = False
                w.status = 0
            w.update()
        if self.party.board.last_move:
            x, y = self.party.board.last_move
            self.boardField.itemAtPosition(x, y).widget().status = 2
            self.boardField.itemAtPosition(x, y).widget().update()
