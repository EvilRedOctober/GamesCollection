# -*- coding: utf-8 -*-
"""Contains abstract classes for PyQt forms"""

from PyQt5 import QtWidgets, QtCore, QtGui

from basic.party import Party
from games.abstracts import Board
from gui.forms.game_form import Ui_GameForm


class AbstractCell(QtWidgets.QWidget):
    """Abstract class for game form with basic logic."""
    SIZE = 40
    ICONS = (None, ":/Icons/cross.png", ":/Icons/naught.png")
    OUTER_COLOR = QtGui.QColor(200, 200, 200)
    HELP_COLOR = QtGui.QColor(225, 200, 0)
    INNER_COLOR1 = QtGui.QColor(50, 50, 50)
    INNER_COLOR2 = QtGui.QColor(200, 225, 200)

    clicked = QtCore.pyqtSignal(int, int)

    def __init__(self, x: int, y: int, value: int, *args, **kwargs):
        super(AbstractCell, self).__init__(*args, **kwargs)
        self.setFixedSize(QtCore.QSize(self.SIZE, self.SIZE))

        self.x = x
        self.y = y
        self.value = value
        self.isAvailable = True
        self.status = 0

    def paintEvent(self, event: QtGui.QPaintEvent):
        # Painting rectangle
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)

        r = event.rect()
        if (self.x + self.y) % 2:
            inner_color = self.INNER_COLOR1
        else:
            inner_color = self.INNER_COLOR2
        brush = QtGui.QBrush(inner_color)
        p.fillRect(r, brush)
        pen = QtGui.QPen(inner_color)
        if self.status == 1:
            pen = QtGui.QPen(self.HELP_COLOR)
        pen.setWidth(2)
        p.setPen(pen)
        p.drawRect(2, 2, self.SIZE - 4, self.SIZE - 4)
        pen = QtGui.QPen(self.OUTER_COLOR)
        pen.setWidth(2)
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

    resizeSignal = QtCore.pyqtSignal(int, int)

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
        difficulty_settings = self.DIFFICULTY_LEVELS[self.difficultyLevelsCombo.currentText()]
        N = int(self.sizesCombo.currentText())
        AI_player = self.computerPlayerCombo.currentIndex() + 1
        board = self.Board_Class(turn=1, size=N)
        self.party = Party(self, board, is_AI, AI_player, difficulty_settings)

        # Field setup
        self.boardField.setSpacing(0)
        # Clear old grid
        for i in reversed(range(self.boardField.count())):
            self.boardField.itemAt(i).widget().setParent(None)
        # Create new grid
        for i in range(N):
            for j in range(N):
                w = self.Cell_Class(i, j, board.get_value(i, j))
                w.clicked.connect(self.apply_move)
                self.boardField.addWidget(w, i, j)
        # Do computer move or wait for player
        self.party.run()
        # Repaint and resize
        self.update_values()
        size = self.boardField.itemAtPosition(0, 0).widget().SIZE
        width = N * size + 50 + self.settingsFrame.width()
        height = N * size + 140
        self.resizeSignal.emit(width, height)

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
            else:
                w.status = 0
            w.update()

    def apply_move(self, x, y):
        res = self.party.do_move((x, y))
        self.update_values()
        if res:
            for i in reversed(range(self.boardField.count())):
                w = self.boardField.itemAt(i).widget()
                w.isAvailable = False
                w.status = 0
            if res == 3:
                QtWidgets.QMessageBox.information(self,
                                                  "Ничья!",
                                                  "Никто не победил!",
                                                  buttons=QtWidgets.QMessageBox.Ok)
            else:
                if self.party.isAI and res == self.party.AI_player:
                    text = "Победил компьютер!"
                else:
                    text = "Победили %s!" % self.computerPlayerCombo.itemText(res - 1).lower()
                QtWidgets.QMessageBox.information(self,
                                                  "Победа!",
                                                  text,
                                                  buttons=QtWidgets.QMessageBox.Ok)
