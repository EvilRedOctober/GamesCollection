# -*- coding: utf-8 -*-

import numpy as np

from games.abstracts import Piece, Board, Move


class Figure(Piece):
    NUM2STR = ['0', '+', '-']


class Reversi(Board):

    def __init__(self, size: int = 15, turn: int = 1, field: np.ndarray = None, boundary_moves: set = None,
                 last_move: Move = None):
        """
        A game board for reversi (otello).

        :param size: 8 or 10 for board size. If new board is empty
        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param boundary_moves: Set of positions for moves along the border of placed pieces.
        :param last_move: Position of last move.
        """
        if field is None:
            # If creating new empty field
            field = np.array([[Figure(0) for _ in range(size)] for _ in range(size)], dtype=object)
            field[size // 2 - 1][size // 2 - 1] = Figure(1)
            field[size // 2][size // 2] = Figure(1)
            field[size // 2 - 1][size // 2] = Figure(2)
            field[size // 2][size // 2 - 1] = Figure(2)
            boundary_moves = {(size // 2 - 2, size // 2 - 1), (size // 2 - 2, size // 2),
                              (size // 2 + 1, size // 2 - 1), (size // 2 + 1, size // 2),
                              (size // 2 - 1, size // 2 - 2), (size // 2, size // 2 - 2),
                              (size // 2 - 1, size // 2 + 1), (size // 2, size // 2 + 1)}
        self._field = field
        self._size = size
        self._turn = turn
        self._boundary_moves = boundary_moves
        self._legal_moves = []
        self._gem_counters = [0, 0, 0]
        self.last_move = last_move
        # Recount gems
        for i in range(3):
            self._gem_counters[i] = (self._field == i).sum()
        self.check_legal_moves()
        # When player can't do any move return turn
        if len(self._legal_moves) == 0:
            self._turn = self.last_turn
            self.check_legal_moves()
        # When even opponent can't do any move set clear positions to zero to end game
        if len(self._legal_moves) == 0:
            self._gem_counters[0] = 0

    def check_legal_moves(self):
        self._legal_moves = []
        for x, y in self._boundary_moves:
            # Flag that move is added to stop checking
            move_added = False
            # Check all directions
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                k = 1
                next_x, next_y = x + k * dx, y + k * dy
                # Flag to know when we reached reverse color
                got_reverse_color = False
                while 0 <= next_x < self._size and 0 <= next_y < self._size and self._field[next_x][next_y] != 0:
                    if self._field[next_x][next_y] == self.last_turn:
                        got_reverse_color = True
                    else:
                        if self._field[next_x][next_y] == self.turn and got_reverse_color:
                            # We can change color of at least one piece
                            self._legal_moves.append((x, y))
                            move_added = True
                        break
                    k += 1
                    next_x, next_y = x + k * dx, y + k * dy
                if move_added:
                    break

    def move(self, location: Move):
        if location not in self._legal_moves:
            raise (IndexError('Current location (%d, %d) is already occupied' % location))
        x, y = location
        new_boundary_moves = self._boundary_moves.copy()
        new_boundary_moves.remove((x, y))
        for i, j in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
            if 0 <= i < self._size and 0 <= j < self._size and self._field[i][j] == 0:
                new_boundary_moves.add((i, j))
        new_field = self._field.copy()
        new_field[x][y] = Figure(self.turn)
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            k = 1
            next_x, next_y = x + k * dx, y + k * dy
            # Flag to know when we reached reverse color
            got_reverse_color = False
            while 0 <= next_x < self._size and 0 <= next_y < self._size and self._field[next_x][next_y] != 0:
                if self._field[next_x][next_y] == self.last_turn:
                    got_reverse_color = True
                else:
                    if self._field[next_x][next_y] == self.turn and got_reverse_color:
                        next_x -= dx
                        next_y -= dy
                        while next_x != x or next_y != y:
                            new_field[next_x][next_y] = Figure(self.turn)
                            next_x -= dx
                            next_y -= dy
                    break
                k += 1
                next_x, next_y = x + k * dx, y + k * dy
        new_turn = self.last_turn
        return Reversi(self._size, new_turn, new_field, new_boundary_moves, location)

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
        if self._gem_counters[0] == 0:
            return self._gem_counters[1] == self._gem_counters[2]
        return False

    def evaluate(self, player: int) -> float:
        return self._gem_counters[player] - self._gem_counters[Piece.opposite(player)]


if __name__ == '__main__':

    def test():
        from games.ai.decision_rule import find_best_move
        win = [0, 0]

        for i in range(1):
            board = Reversi(8)
            print(board)
            while not board.is_win and not board.is_draw:
                if board.turn == 1:
                    x, y = find_best_move(board, 1)
                else:
                    x, y = find_best_move(board, 0)
                board = board.move((x, y))
                print(board)
            if board.is_draw:
                print('round drawn!')
            else:
                win[board.turn - 1] += 1
                print('Player %i won!' % board.last_turn)
        print(win)


    test()
