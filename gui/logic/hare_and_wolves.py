# -*- coding: utf-8 -*-


from gui.logic.abstracts import *
from games.hare_and_wolves import *


class HareCell(AbstractCell):
    """Abstract class for game form with basic logic."""
    INNER_COLOR1 = QtGui.QColor(240, 240, 255)
    INNER_COLOR2 = QtGui.QColor(50, 50, 50)
    OUTER_COLOR = QtGui.QColor(0, 0, 0)

    figure_leave = QtCore.pyqtSignal()

    # Paths to the icons
    ICONS = (None, ":/Icons/hare.png", ":/Icons/wolf.png")

    def mouseReleaseEvent(self, event):
        if self.isAvailable:
            self.clicked.emit(self.x, self.y)
        else:
            self.figure_leave.emit()


class HareForm(AbstractGameForm):
    DIFFICULTY_LEVELS = {'Легко': {'max_depth': 0}, 'Среднее': {'max_depth': 1}, 'Сложно': {'max_depth': 3}}
    BOARD_SIZES = ('8',)
    PLAYERS = ('Заяц', 'Волки')
    RULES = "Заяц и волки.\n\n" \
            "На шахматной доске есть 4 волка сверху (на черных клеточках), и 1 заяц снизу (на одной из черных). " \
            "Заяц ходит первым. Ходить можно только на одну клеточку по диагонали, притом волки могут ходить только " \
            "вниз, а заяц в любую сторону. Заяц побеждает, когда достиг одной из верхних клеточек, а волки, когда " \
            "они окружили или прижали зайца (когда зайцу некуда ходить)."
    Board_Class = Hare_and_wolves
    Cell_Class = HareCell
    WIN_MESSAGE = ("Победил заяц!", "Победили волки!")

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(HareForm, self).__init__(parent)
        self.figure_selected = None

    def game_start(self):
        super(HareForm, self).game_start()
        for i in reversed(range(self.boardField.count())):
            self.boardField.itemAt(i).widget().figure_leave.connect(self.undo_selection)
        self.figure_selected = None

    def undo_selection(self):
        self.figure_selected = None
        self.party.start(None)

    def is_available_move(self, move, legal_moves):
        # If no figure selected then mark available figures
        # Else mark available moves for selected figure
        if self.blocked:
            return False
        available_moves = [moves[1] for moves in legal_moves if self.figure_selected == moves[0]] if \
            self.figure_selected else [moves[0] for moves in legal_moves]
        return move in available_moves

    def update_values(self, field, legal_moves):
        super(HareForm, self).update_values(field, legal_moves)

    def apply_move(self, x, y):
        if not self.blocked:
            if self.figure_selected is None:
                self.figure_selected = (x, y)
                self.party.start(None)
                return
            self.waitSignal.emit(True, None)
            self.party.start((self.figure_selected, (x, y)))
            self.blocked = True
            self.figure_selected = None
