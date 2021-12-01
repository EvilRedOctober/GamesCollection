# -*- coding: utf-8 -*-

from copy import deepcopy

import numpy as np

from games.abstracts import Piece, Board, Move


class Tile(Piece):
    NUM2STR = ['_', 'W', 'G']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Talpa(Board):
    MAX_SCORES = 100

    def __init__(self, size: int = 8, turn: int = 1, field: np.ndarray = None,  paths: list[set[Move]] = None,
                 last_move: Move = None):
        """

        A game board for talpa game.

        :param size: 6, 8 or 10 for board size. If new board is empty
        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param paths: Paths of empty tiles in field in a form of a list of sets of paths' coordinates.
        :param last_move: Position of last move.
        """
        if field is None:
            field = np.array([[Tile(1) if (i+j) % 2 else Tile(2) for j in range(size)] for i in range(size)],
                             dtype=object)
        self._field = field
        self._size = size
        self._turn = turn
        self.paths = paths if paths else []
        self.last_move = last_move
        # Determine the legal moves
        attack_moves = []
        remove_moves = []
        for i in range(self._size):
            for j in range(self._size):
                if self._field[i][j] == self._turn:
                    # Remove own tile
                    remove_moves.append(((i, j), (i, j)))
                    for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= x < self._size and 0 <= y < self._size and self._field[x][y] == self.last_turn:
                            # Can attack enemy near
                            attack_moves.append(((i, j), (x, y)))
        # First phase of game - attack enemy, second - remove own tiles
        self._legal_moves = attack_moves if len(attack_moves) > 0 else remove_moves
        # Count lens of paths for game evaluating
        self.paths_lens = []
        self.count_paths_lengths()

    def count_paths_lengths(self):
        for path in self.paths:
            min_hor = min(map(lambda x: x[0], path))
            min_ver = min(map(lambda x: x[1], path))
            max_hor = max(map(lambda x: x[0], path))
            max_ver = max(map(lambda x: x[1], path))
            self.paths_lens.append(((max_hor - min_hor + 1), (max_ver - min_ver + 1)))

    def move(self, locations: tuple[Move, Move]) -> Board:
        """
        Returns board with next state after move.

        :param locations: tuple pf location of piece and its destination location
        :return: copy of board with new state
        """
        if locations not in self._legal_moves:
            raise IndexError('Bad move %s!' % str(locations))
        tile_pos, destination = locations
        new_field = self._field.copy()
        new_paths = deepcopy(self.paths)
        new_turn = self.last_turn
        # Change tiles positions
        new_field[destination] = new_field[tile_pos]
        new_field[tile_pos] = Tile(0)

        # There is three possible situation with paths (empty tiles) around removed tile:
        i, j = tile_pos
        first_path_index = -1
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < self._size and 0 <= y < self._size and self._field[x][y] == 0:
                if first_path_index == -1:
                    # 1) One path - add current empty tile to this path
                    for k in range(len(new_paths)):
                        if (x, y) in new_paths[k]:
                            new_paths[k].add((i, j))
                            first_path_index = k
                            break
                else:
                    # 2) More than one path - add current empty tile to first path, connect every other path with first
                    # and remove other paths from new_paths
                    for k in range(len(new_paths)):
                        if (x, y) in new_paths[k] and k != first_path_index:
                            new_paths[first_path_index] |= new_paths[k]
                            new_paths.pop(k)
                            first_path_index = first_path_index if first_path_index < k else first_path_index - 1
                            break
        # 3) No other paths - create new path for new_paths and add current empty tile to it
        if first_path_index == -1:
            new_paths.append({(i, j), })

        return Talpa(self._size, new_turn, new_field, new_paths, destination)

    @property
    def is_win(self) -> bool:
        # Player best path
        player_len = max(map(lambda x: x[self.last_turn - 1], self.paths_lens)) if self.paths_lens else 0
        # Opponent best path
        opponent_len = max(map(lambda x: x[self.turn - 1], self.paths_lens)) if self.paths_lens else 0
        if opponent_len == self._size:
            # Opponent's victory in priority (even if the player should win)
            self._turn = self.last_turn
            return True
        if player_len == self._size:
            return True
        return False

    @property
    def is_draw(self) -> bool:
        # There is no draw
        return False

    def evaluate(self, player: int) -> float:
        """Summing the square of lens"""
        player_scores = 0
        enemy_scores = 0
        for lengths in self.paths_lens:
            player_scores += lengths[player - 1] ** 2
            enemy_scores += lengths[Tile.opposite(player) - 1] ** 2
        if enemy_scores == self._size ** 2:
            return -enemy_scores
        return player_scores - enemy_scores * 1.1
