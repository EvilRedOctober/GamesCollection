# -*- coding: utf-8 -*-


from gui.logic.hare_and_wolves import *
from games.talpa import *


class TalpaCell(HareCell):
    """Abstract class for game form with basic logic."""
    INNER_COLOR1 = QtGui.QColor(75, 50, 150)
    INNER_COLOR2 = QtGui.QColor(75, 50, 150)
    OUTER_COLOR = QtGui.QColor(125, 150, 200)

    # Paths to the icons
    ICONS = (None, ":/Icons/whiteTitle.png", ":/Icons/goldTitle.png")


class TalpaForm(HareForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0, 'randomizing': 20}, 'Среднее': {'max_depth': 1, 'randomizing': 5},
                         'Сложно': {'max_depth': 1}}
    BOARD_SIZES = ('6', '8', '10')
    PLAYERS = ('Белые', 'Жёлтые')
    RULES = "Тальпа.\n\n" \
            "Настольная логическая игра для двух игроков, придуманная Арти Сэндлером в 2010. В игре Тальпа " \
            "используется квадратная доска.\nЛевая и правая границы доски окрашены в жёлтый цвет, а верхняя и нижняя " \
            "границы доски - в белый.\nВ начале партии доска в шахматном порядке заполнена белыми и жёлтыми фишками." \
            "\nЦелью игры Тальпа является открытие 'туннеля' в виде цепочки соседних по горизонтали или вертикали " \
            "(но не по диагонали) пустых клеток между сторонами своего цвета без открытия такого же 'туннеля' между " \
            "сторонами противника.\nИгрок проигрывает партию, если он делает ход, открывающий 'туннель' между " \
            "сторонами противника, даже, если этим же ходом он создает свой собственный 'туннель'.\n " \
            "Угловые клетки относятся к обеим прилегающим краям доски.\nВ игре Тальпа не бывает ничейных ситуаций.\n" \
            "Игроки ходят по очереди. Начинает игрок, играющий белыми фишками. В свой ход игрок выбирает одну из своих" \
            " фишек и сбивает фишку противника, находящуюся на соседней по горизонтали или вертикали (но не по " \
            "диагонали) клетке. Сбитая фишка убирается с доски, а на ее место перемещается выбранная фишка игрока, " \
            "оставляя за собой пустую клетку. Игрок обязан сделать сбивающий ход, если существует такая возможность. " \
            "В противном случае игрок в свой ход снимает с доски одну из своих фишек."
    Board_Class = Talpa
    Cell_Class = TalpaCell

    COMPUTER_WIN_TEXT = 'Победил компьютер!'

    WIN_MESSAGE = ("Победили белые!", "Победили жёлтые!")

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(TalpaForm, self).__init__(parent)
        self.boardFrame.layout().setSpacing(0)
        # Add board edges (so the player knows how to build a path in the game)
        self.boardFrame.layout().setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.upper_edge = QtWidgets.QWidget()
        self.upper_edge.setFixedSize(0, 20)
        self.lower_edge = QtWidgets.QWidget()
        self.lower_edge.setFixedSize(0, 20)
        self.left_edge = QtWidgets.QWidget()
        self.left_edge.setFixedSize(20, 0)
        self.right_edge = QtWidgets.QWidget()
        self.right_edge.setFixedSize(20, 0)

        # Change default position of game board (from (0, 1) to (1, 1))
        self.boardField.setParent(None)
        self.boardFrame.layout().addLayout(self.boardField, 1, 1)
        self.boardFrame.layout().addWidget(self.lower_edge, 0, 1)
        self.boardFrame.layout().addWidget(self.upper_edge, 2, 1)
        self.boardFrame.layout().addWidget(self.left_edge, 1, 0)
        self.boardFrame.layout().addWidget(self.right_edge, 1, 2)

    def game_start(self):
        super(TalpaForm, self).game_start()
        # Length of board to draw edges
        length = self.size * self.boardField.itemAt(1).widget().width()

        # Set sizes and colors of edges
        self.upper_edge.setFixedWidth(length)
        self.lower_edge.setFixedWidth(length)
        style_css = 'border: 2px outset rgb(125, 150, 200);'\
                    'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, '\
                    'stop: 0 rgb(255, 255, 255), stop: 1 rgb(150, 150, 150));'
        self.upper_edge.setStyleSheet(style_css)
        self.lower_edge.setStyleSheet(style_css)

        self.left_edge.setFixedHeight(length)
        self.right_edge.setFixedHeight(length)
        style_css = 'border: 2px outset rgb(125, 150, 200);'\
                    'background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, '\
                    'stop: 0 rgb(255, 255, 0), stop: 1 rgb(200, 150, 0));'
        self.left_edge.setStyleSheet(style_css)
        self.right_edge.setStyleSheet(style_css)
