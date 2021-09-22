# -*- coding: utf-8 -*-
"""Contains abstract classes for PyQt forms"""

from PyQt5 import QtWidgets, QtCore, QtGui

from basic.party import Party
from games.abstracts import Board, Move
from gui.forms.game_form import Ui_GameForm


class AbstractCell(QtWidgets.QWidget):
    """Abstract class for game form with basic logic."""
    ICONS = (None, ":/Icons/cross.png", ":/Icons/naught.png")
    OUTER_COLOR = QtCore.Qt.lightGray
    INNER_COLOR1 = QtGui.QColor(50, 50, 50)
    INNER_COLOR2 = QtGui.QColor(200, 225, 200)

    clicked = QtCore.pyqtSignal(int, int)

    def __init__(self, x: int, y: int, value: int, *args, **kwargs):
        super(AbstractCell, self).__init__(*args, **kwargs)
        self.setFixedSize(QtCore.QSize(40, 40))

        self.x = x
        self.y = y
        self.value = value
        self.isAvailable = True

    def paintEvent(self, event: QtGui.QPaintEvent):
        # Painting rectangle
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)

        r = event.rect()
        if (self.x + self.y) % 2:
            brush = QtGui.QBrush(self.INNER_COLOR1)
        else:
            brush = QtGui.QBrush(self.INNER_COLOR2)
        p.fillRect(r, brush)
        pen = QtGui.QPen(self.OUTER_COLOR)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)
        image = self.ICONS[self.value]
        if image:
            p.drawPixmap(r, QtGui.QPixmap(image))

    def mouseReleaseEvent(self, event):
        if self.isAvailable:
            self.clicked.emit(self.x, self.y)


class AbstractGameForm(QtWidgets.QWidget, Ui_GameForm):
    """Basic class for game form with basic logic."""
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0}, 'Среднее': {'max_depth': 1}, 'Сложно': {'max_depth': 3}}
    BOARD_SIZES = ('8',)
    PLAYERS = ('Белые', 'Чёрные')
    RULES = "Здесь могла быть выша игра."
    Board_Class = Board
    Cell_Class = AbstractCell

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(AbstractGameForm, self).__init__(parent)
        self.setupUi(self)
        self.party = None

    def setup_form(self):
        self.difficultyLevelsCombo.addItems(self.DIFFICULTY_LEVELS.keys())
        self.sizesCombo.addItems(self.BOARD_SIZES)
        self.computerPlayerCombo.addItems(self.PLAYERS)
        self.rulesText.setText(self.RULES)
        self.startButton.clicked.connect(self.game_start)

    def game_start(self):
        # Game settings
        is_AI = self.isComputer.isChecked()
        print(is_AI)
        difficulty_settings = self.DIFFICULTY_LEVELS[self.difficultyLevelsCombo.currentText()]
        size = int(self.sizesCombo.currentText())
        AI_player = self.computerPlayerCombo.currentIndex() + 1
        board = self.Board_Class(turn=1, size=size)
        self.party = Party(self, board, is_AI, AI_player, difficulty_settings)

        # Field setup
        for i in reversed(range(self.boardField.count())):
            self.boardField.itemAt(i).widget().setParent(None)
        for i in range(size):
            for j in range(size):
                w = self.Cell_Class(i, j, board.get_value(i, j))
                w.clicked.connect(self.apply_move)
                self.boardField.addWidget(w, i, j)
        self.party.run()
        self.update_values()

    def update_values(self):
        for i in reversed(range(self.boardField.count())):
            w = self.boardField.itemAt(i).widget()
            value = self.party.board.get_value(w.x, w.y)
            w.value = value
            if value:
                w.isAvailable = False
                w.update()

    def apply_move(self, x, y):
        if self.party.do_move((x, y)):
            for i in reversed(range(self.boardField.count())):
                w = self.boardField.itemAt(i).widget()
                w.isAvailable = False
        self.update_values()
