# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from numpy import ndarray

from games.abstracts import *
from games.ai.decision_rule import find_best_move


GAME_CONTINUE, PLAYER_1_WIN, PLAYER_2_WIN, DRAW, BAD_MOVE = 0, 1, 2, 3, -1


class Party(QtCore.QThread):
    sendGameField = QtCore.pyqtSignal(ndarray, list)
    sendGameState = QtCore.pyqtSignal(int)
    unblockGameForm = QtCore.pyqtSignal()
    waitSignal = QtCore.pyqtSignal(bool)

    def __init__(self, board: Board, is_AI: bool, AI_player: int = None,
                 difficulty_settings: dict = None):
        """
        A class for storing the state of the board, controlling the order of players
        and calling AI functions (in the case of playing with a computer).

        :param board: Initialized game board.
        :param is_AI: True if play with computer.
        :param AI_player: Number of AI player.
        :param difficulty_settings: dictionary with difficulty settings.
        """
        QtCore.QThread.__init__(self)
        self.isAI = is_AI
        self.board = board
        self.difficulty_settings = difficulty_settings
        self.AI_player = AI_player
        self.move = None

    def start(self, move=None):
        super().start()
        self.move = move

    def run(self):
        # CHeck that move is possible
        self.waitSignal.emit(True)
        if self.move:
            try:
                board = self.board.move(self.move)
                self.board = board
            except IndexError:
                self.sendGameState.emit(BAD_MOVE)
                self.unblockGameForm.emit()
                return

        # Check game state after move
        self.check_state()
        self.sendGameField.emit(self.board.field, self.board.legal_moves)
        self.waitSignal.emit(False)

    def check_state(self):
        """Check that game continue, there is winner or draw."""
        if self.board.is_draw:
            self.sendGameState.emit(DRAW)
        elif self.board.is_win:
            self.sendGameState.emit(self.board.last_turn)
        else:
            self.sendGameState.emit(GAME_CONTINUE)
            self.sendGameField.emit(self.board.field, self.board.legal_moves)
            if self.isAI and self.board.turn == self.AI_player:
                self.do_ai_move()
            else:
                self.unblockGameForm.emit()

    def do_ai_move(self):
        """Find AI's best move and apply it or wait for player move."""
        self.msleep(1000)
        best_move = find_best_move(self.board, **self.difficulty_settings)
        self.board = self.board.move(best_move)
        self.check_state()
