# -*- coding: utf-8 -*-

from copy import deepcopy
from random import randint

import numpy as np

from games.abstracts import Piece, Board, Move


class Five_in_a_row(Board):
    WIN_TEMPLATES = np.array([[[i == j for j in range(5)] for i in range(5)],
                              [[i == 2 for _ in range(5)] for i in range(5)],
                              [[j == 2 for j in range(5)] for _ in range(5)],
                              [[i + j == 4 for j in range(5)] for i in range(5)]])
    SCORE_TEMPLATES = np.array([[[i == j for j in range(9)] for i in range(9)],
                               [[i == 4 for _ in range(9)] for i in range(9)],
                               [[j == 4 for j in range(9)] for _ in range(9)],
                               [[i + j == 8 for j in range(9)] for i in range(9)]])
    SCORES_THRESHOLD = 7000

    def __init__(self, size: int = 15, turn: int = 1, field: np.ndarray = None, moves: list[list[Move]] = None,
                 legal_moves: set = None):
        """
        A game board for five-in-a-row game (Gomoku).

        :param size: 15 or 19 for board size. If new board is empty
        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param moves: List of lists for every players' moves
        """
        if field is None:
            # If creating new empty field
            field = np.array([[Piece(0) for _ in range(size)] for _ in range(size)], dtype=object)
            legal_moves = {(size // 2, size // 2)}
            moves = [[], []]
        self._field = field
        self._size = size
        self._turn = turn
        self._legal_moves = legal_moves
        self._moves = moves

    def move(self, location: Move):
        x, y = location
        if self._field[x][y] != 0:
            raise(IndexError('Current location (%d, %d) is already occupied' % location))
        new_field = self._field.copy()
        new_field[x][y] = Piece(self.turn)
        new_turn = self.last_turn
        new_moves = deepcopy(self._moves)
        new_moves[self.turn - 1].append(location)
        legal_moves = self._legal_moves.copy()
        if location in legal_moves:
            # For the AI, it is only necessary to control key positions in the center and adjacent to the moves.
            legal_moves.remove(location)
        # Update moves with nearest empty positions
        legal_moves.update([(x, y) for x, y in self.get_neighbours(location) if new_field[x][y] == 0])
        return Five_in_a_row(self._size, new_turn, new_field, new_moves, legal_moves)

    @property
    def is_win(self) -> bool:
        # Checking the area near every non-border move of the current player with every winning pattern.
        last_player = self.last_turn
        last_player_moves = self._moves[last_player - 1]
        if len(last_player_moves) == 0:
            return False
        last_move = last_player_moves[-1]
        moves_2_check = [(x, y) for x, y in self.get_neighbours(last_move, 2) if self._field[x][y] == last_player]
        for x, y in moves_2_check:
            for template in self.WIN_TEMPLATES:
                # Non-border moves
                if 1 < x < self._size - 2 and 1 < y < self._size - 2:
                    # Area near move
                    w = self._field[x - 2:x + 3, y - 2:y + 3]
                    # Count identical moves in the places of the template
                    if (w[template] == w[2][2]).sum() == 5:
                        # If five in a row - win
                        return True

    @property
    def is_draw(self) -> bool:
        return len(self.legal_moves) == 0

    def count_scores(self, player: int) -> float:
        # Checking the area near every non-border move of the current player with every winning pattern.
        x, y = self._moves[self.last_turn - 1][-1]
        opponent = Piece.opposite(player)
        total_scores = 0
        # Move from the borders
        lx = max(x - 4, 0)
        rx = min(x + 5, 15)
        ly = max(y - 4, 0)
        ry = min(y + 5, 15)
        window = (self._field[lx:rx, ly:ry]).copy()
        # When scores counting for player this will increase players scores by blocking opponent
        window[x-lx][y-ly] = Piece(player)
        for template in self.SCORE_TEMPLATES:
            # Resize template for borders
            border_template = template[4-x+lx:4+rx-x, 4-y+ly:4+ry-y]
            part = window[border_template]
            # Checking every five cells
            template_scores = 0
            for i in range(part.size - 4):
                five = part[i:i+5]
                # Count identical moves in the places of the template
                own_pieces = (five == player).sum()
                enemy_pieces = (five == opponent).sum()
                if enemy_pieces > 0 or own_pieces == 0:
                    continue
                if own_pieces == 1:
                    template_scores = max(randint(1, 20), template_scores)
                elif own_pieces == 2:
                    template_scores = max(randint(190, 200), template_scores)
                elif own_pieces == 3:
                    template_scores = max(randint(2990, 3000), template_scores)
                elif own_pieces == 4 and (part[0] == 0 or part[-1] == 0):
                    template_scores = max(randint(6990, 7000), template_scores)
                elif own_pieces == 4:
                    template_scores = max(randint(1990, 2000), template_scores)
                elif own_pieces == 5:
                    template_scores = max(99999, template_scores)
            total_scores += template_scores
        return total_scores

    def evaluate(self, player: int) -> float:
        return self.count_scores(player) * 1.1 + self.count_scores(Piece.opposite(player))


if __name__ == '__main__':
    from random import choice

    def test():
        for i in range(1):
            board = Five_in_a_row(15)
            while not board.is_win:
                x, y = choice(list(board.legal_moves))
                board = board.move((x, y))
                print(board)

    test()
