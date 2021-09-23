# -*- coding: utf-8 -*-

from collections import deque

import numpy as np

from games.abstracts import Piece, Board, Move


class Hare(Piece):
    def __init__(self):
        super().__init__(1)

    def __repr__(self):
        return 'R'


class Wolf(Piece):
    def __init__(self):
        super().__init__(2)

    def __repr__(self):
        return 'W'


class Hare_and_wolves(Board):
    _size = 8

    def __init__(self, turn: int = 1, field: np.ndarray = None, hare_pos: Move = None, wolves_poses: list[Move] = None,
                 *args, **kwargs):
        """

        A game board for hare and wolves. First player plays with one hare, second - with four wolves.
        Every animal can do one move in nearest diagonals cells, but wolf can move only to lower positions.
        Only one wolf can move per turn. Players cannot skip turn. Hare must reach top position of field to win.
        Wolves must get hare and make so that the hare has no possible moves.

        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param hare_pos: Location of Hare.
        :param wolves_poses: List of locations of wolves.
        """
        if field is None:
            field = np.array([[Piece(0) for _ in range(8)] for _ in range(8)], dtype=object)
            # Lists of animals
            hare_pos = (7, 3)
            field[hare_pos] = Hare()
            wolves_poses = [(0, 0), (0, 2), (0, 4), (0, 6)]
            for wolf_pos in wolves_poses:
                field[wolf_pos] = Wolf()
        self._hare_pos = hare_pos
        self._wolves_poses = wolves_poses
        self._field = field
        self._turn = turn

    def move(self, locations: tuple[Move, Move]) -> Board:
        """
        Returns board with next state after move.

        :param locations: tuple pf location of piece and its destination location
        :return: copy of board with new state
        """
        animal_pos, destination = locations
        new_field = self._field.copy()
        if max(abs(destination[0] - animal_pos[0]), abs(destination[1] - animal_pos[1])) != 1:
            raise IndexError('Bad move %s! Too long move.' % str(locations))
        if self.turn == 1 and self._field[destination] != 0:
            raise IndexError('Bad move %s! Hare can move only to empty cell.' % str(locations))
        if self.turn == 2 and (self._field[animal_pos] != 2 or
                               (self._field[destination] != 0 or destination[0] < animal_pos[0])):
            raise IndexError('Bad move %s! Wolves can move only to lower empty cells.' % str(locations))
        if sum(destination) != sum(animal_pos) and destination[0] - destination[1] != animal_pos[0] - animal_pos[1]:
            raise IndexError('Bad move %s! Can move only to adjacent diagonal cell.' % str(locations))
        new_field[animal_pos], new_field[destination] = new_field[destination], new_field[animal_pos]
        new_turn = self.last_turn
        if self.turn == 1:
            new_hare_pos = destination
            new_wolves_pos = self._wolves_poses.copy()
        else:
            new_hare_pos = self._hare_pos
            i = self._wolves_poses.index(animal_pos)
            new_wolves_pos = self._wolves_poses.copy()
            new_wolves_pos[i] = destination
        return Hare_and_wolves(new_turn, new_field, new_hare_pos, new_wolves_pos)

    @property
    def is_win(self) -> bool:
        if self.last_turn == 1 and (self._hare_pos[0] == 0 or self.legal_moves == []):
            return True
        if self.last_turn == 2 and self.legal_moves == []:
            return True
        return False

    @property
    def is_draw(self) -> bool:
        return False

    @property
    def legal_moves(self) -> list[tuple[Move, Move]]:
        # Returns empty adjacent diagonal cells.
        if self.turn == 1:
            x, y = self._hare_pos
            return [(self._hare_pos, (x+i, y+j)) for i, j in ((1, 1), (1, -1), (-1, 1), (-1, -1)) if 8 > x+i >= 0 and
                    8 > y+j >= 0 and self._field[x+i][y+j] == 0]
        legal_moves = []
        for wolf_pos in self._wolves_poses:
            x, y = wolf_pos
            moves = [(wolf_pos, (x+i, y+j)) for i, j in ((1, 1), (1, -1)) if 8 > x+i >= 0 and
                    8 > y+j >= 0 and self._field[x+i][y+j] == 0]
            legal_moves += moves
        return legal_moves

    def evaluate(self, player: int) -> float:
        """Using BFS to estimate distance of hare to top position.
        If there is no way to top, then uses height of hare in field.
        Evaluates board scores for hare (by reversing scores) and wolves (returns clear scores)."""
        to_check = deque()
        path_length = 0
        to_check.append((self._hare_pos, path_length))
        checked = set()
        can_get_top = False
        while to_check:
            pos, path_length = to_check.popleft()
            # If BFS gets top then stop
            if pos[0] == 0:
                can_get_top = True
                break
            checked.add(pos)
            for x, y in self.get_neighbours(pos):
                # Only empty not checked diagonals
                if self._field[x][y] == 0 and x != pos[0] and y != pos[1] and (x, y) not in checked:
                    to_check.append(((x, y), path_length + 1))
        if can_get_top:
            # How long is the hare's path to the top
            scores = path_length
        else:
            if path_length == 0:
                # If hare is caught there is max scores
                scores = 100
            else:
                # Height have more weight because hare cannot reach the top and it's profitable for wolves
                scores = self._hare_pos[0] * 10
        if player == 1:
            # Reversing scores for hare because closest path is better
            scores = 100 - scores
        return scores


if __name__ == '__main__':
    from games.ai.decision_rule import find_best_move

    def test():
        wins = [0, 0]
        for k in range(1, 26):
            board = Hare_and_wolves()
            while not board.is_win:
                if board.turn == 2:
                    move = find_best_move(board, 4)
                else:
                    move = find_best_move(board, 0)
                board = board.move(move)
            wins[board.last_turn - 1] += 1
            print('Party %i. Win player %d!' % (k, board.last_turn))
            print(board)
        print(wins)

    test()
