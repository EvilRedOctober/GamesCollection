# -*- coding: utf-8 -*-


from games.flume import *
from gui.logic.reversi import *


class FlumeCell(ReversiCell):
    # Paths to the icons
    ICONS = (None, ":/Icons/greenGem.png", ":/Icons/blueGem.png", ":/Icons/blackGem.png")
    INNER_COLOR1 = QtGui.QColor(255, 200, 100)
    INNER_COLOR2 = QtGui.QColor(255, 200, 100)
    OUTER_COLOR = QtGui.QColor(200, 100, 0)
    LAST_TURN_COLOR = QtGui.QColor(250, 0, 0)


class FlumeForm(ReversiForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0, 'randomizing': 20}, 'Среднее': {'max_depth': 1, 'randomizing': 5},
                         'Сложно': {'max_depth': 1}}
    BOARD_SIZES = ('11', '13', '15')
    PLAYERS = ('Зелёные', 'Синие')
    RULES = "Флюм.\n\n" \
            "Это настольная логическая игра для двух игроков, в которой используется квадратная доска. Эта игра " \
            "была придумана Марком Стиром (Mark Steere) в 2009 г.\nВ игре Флюм используются квадратные доски с " \
            "нечетным количеством пересечений. В начале игры край доски заполняется камнями чёрного цвета.\n" \
            "В игре Флюм побеждает игрок, выставивший на доску к концу партии наибольшее количество камней своего " \
            "цвета.\nВ игре Флюм не бывает ничейных ситуаций.\nИгра начинается с пустой доски. Один из игроков " \
            "играет зелёными камнями, другой - синими. Начинает игрок, играющий зелёными камнями.\nВ свой ход каждый " \
            "игрок кладёт камень своего цвета на одно из свободных полей на доске.\nЕсли камень кладётся " \
            "на поле, по соседству с которым (по горизонтали или вертикали) находятся три или четыре камня " \
            "любого из цветов (чёрного, синего или зеленого), то игрок получает дополнительный ход. В этом случае " \
            "игрок обязан выставить еще один камень на доску. Пропуск хода запрещен."
    Board_Class = Flume
    Cell_Class = FlumeCell

    WIN_MESSAGE = ("Победили зелёные!", "Победили синие!")
