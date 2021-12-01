# -*- coding: utf-8 -*-

import numpy as np

from games.abstracts import Piece, Board, Move


class Gem(Piece):
    NUM2STR = ['_', 'G', 'B', 'K']


class Flume(Board):
    MAX_SCORES = 5

    def __init__(self, size: int = 13, turn: int = 1, field: np.ndarray = None, legal_moves: set = None,
                 last_move: Move = (0, 0)):
        """
        A game board for flume game.

        :param size: 11, 13 or 15 for board size. If new board is empty
        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param legal_moves: Set of positions for moves along the border of placed pieces.
        :param last_move: Last player's move.
        """
        if field is None:
            # If creating new empty field
            field = np.array([[Gem(0) for _ in range(size)] for _ in range(size)], dtype=object)
            # Put neutral gems
            for k in range(size):
                field[0][k] = Gem(3)
                field[size - 1][k] = Gem(3)
                field[k][0] = Gem(3)
                field[k][size - 1] = Gem(3)
            legal_moves = {(i, j) for i in range(1, size - 1)
                           for j in range(1, size - 1)}
        self._field = field
        self._size = size
        self._turn = turn
        self._legal_moves = legal_moves
        self._gem_counters = [0, 0, 0]
        self.last_move = last_move
        # Recount gems
        for i in range(3):
            self._gem_counters[i] = (self._field == i).sum()

    @property
    def get_gem_count(self):
        return self._gem_counters[1], self._gem_counters[2]

    def move(self, location: Move):
        if location not in self._legal_moves:
            raise (IndexError('Current location (%d, %d) is already occupied' % location))
        x, y = location
        new_legal_moves = set(self.legal_moves.copy())
        new_legal_moves.remove((x, y))
        new_field = self._field.copy()
        new_field[x][y] = Gem(self.turn)
        # If new gem has at least 3 horizontally or vertically neighbours gems (any color) then make additional move
        if len([True for i, j in self.get_neighbours(location) if (i == x or j == y) and self._field[i][j] != 0]) > 2:
            new_turn = self.turn
        else:
            new_turn = self.last_turn
        return Flume(self._size, new_turn, new_field, new_legal_moves, location)

    @property
    def is_win(self) -> bool:
        if self._gem_counters[0] == 0:
            if self._gem_counters[1] > self._gem_counters[2]:
                self._turn = 2
                return True
            if self._gem_counters[2] > self._gem_counters[1]:
                self._turn = 1
                return True
        return False

    @property
    def is_draw(self) -> bool:
        # There is no draw
        return False

    def evaluate(self, player: int) -> float:
        scores = 0
        if self._field[self.last_move] == self.turn and self.turn == player:
            # If player gets additional move - add scores
            scores += 1
        elif self._field[self.last_move] == self.turn and self.turn != player:
            # But if opponent gets additional move - remove scores
            scores -= 1
        # Counting scores for new additional moves
        additional_scores = 0
        # Searching positions around last move
        for move in self.get_neighbours(self.last_move):
            x, y = move
            # If there is no gem
            if self._field[move] == 0:
                # If new gem has at least 3 horizontally or vertically neighbours gems (any color)
                if len([True for i, j in self.get_neighbours(move) if
                        (i == x or j == y) and self._field[i][j] != 0]) > 2:
                    # Increase bonus
                    additional_scores += 1
        if self.turn == player:
            # If player can do additional moves then add scores
            scores += additional_scores
        else:
            # If opponent can do additional moves then decrease scores
            scores -= additional_scores
        return scores
