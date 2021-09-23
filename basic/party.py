# -*- coding: utf-8 -*-

from typing import Optional

from PyQt5 import QtWidgets

from games.abstracts import *
from games.ai.decision_rule import find_best_move


class Party:

    def __init__(self, form: Optional[QtWidgets.QWidget], board: Board,
                 is_AI: bool, AI_player: int = None, difficulty_settings: dict = None):
        """
        A class for storing the state of the board, controlling the order of players
        and calling AI functions (in the case of playing with a computer).

        :param form: Main form to return messages.
        :param board: Initialized game board.
        :param is_AI: True if play with computer.
        :param AI_player: Number of AI player.
        :param difficulty_settings: dictionary with difficulty settings.
        """
        self.form = form
        self.board = board
        self.isAI = is_AI
        self.AI_player = AI_player
        self.difficulty_settings = difficulty_settings

    def run(self) -> int:
        """Find AI's best move and apply it or wait for player move."""
        if self.board.is_draw:
            return 3
        elif self.board.is_win:
            return self.board.last_turn
        if self.isAI and self.board.turn == self.AI_player:
            best_move = find_best_move(self.board, **self.difficulty_settings)
            self.board = self.board.move(best_move)
            return self.run()
        else:
            return 0

    def do_move(self, move: Union[Move, tuple[Move, Move]]) -> int:
        """Apply player's move."""
        try:
            self.board = self.board.move(move)
            return self.run()
        except IndexError:
            QtWidgets.QMessageBox.information(self.form,
                                              "Невозможный ход!",
                                              "Данный ход %s нельзя совершить! Выберите другой ход!" % str(move),
                                              buttons=QtWidgets.QMessageBox.Ok)
            return 0
