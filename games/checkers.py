# -*- coding: utf-8 -*-

from copy import deepcopy

import numpy as np

from games.abstracts import Piece, Board, Move


class Checkers_piece(Piece):
    def __init__(self, player: int, location: Move = None, is_king: bool = False):
        super().__init__(player)
        self.is_king = is_king
        self.location = location

    @property
    def value(self):
        # To draw image in form
        return self.is_king + self.player if self.player < 2 else self.is_king + self.player + 1

    def __repr__(self):
        return ['▭', '⛀', '⛁', '⛂', '⛃'][self.value]


class Checkers(Board):

    def __init__(self, size: int = 8, turn: int = 1, field: np.ndarray = None,
                 pieces_lists: list[list[Checkers_piece]] = None, last_taker: Checkers_piece = None,
                 turns_without_attack: int = 0):
        """

        A game board for checkers (English draughts).

        :param size: Board size. If new board is empty
        :param turn: 1 or 2 for player number.
        :param field: Old field with new move. If a new board is obtained by making a move on the previous board.
        :param pieces_lists: List of lists of players pieces.
        :param last_taker: The piece that took the opponent's piece on the last move (Or None, if there was no take).
        :param turns_without_attack: Number of moves in a row without taking pieces.
        """
        self._size = size
        if field is None:
            field = np.array([[Checkers_piece(0) for _ in range(self._size)] for _ in range(self._size)], dtype=object)
            # Lists of pieces
            reds, blues = [], []
            for i in range(self._size // 2 - 1):
                for j in range(self._size):
                    if (i + j) % 2:
                        red = Checkers_piece(1, (self._size - 1 - i, self._size - 1 - j))
                        field[self._size - 1 - i][self._size - 1 - j] = red
                        reds.append(red)
                        blue = Checkers_piece(2, (i, j))
                        field[i][j] = blue
                        blues.append(blue)
                        pieces_lists = [reds, blues]
        self._pieces_lists = pieces_lists
        self._field = field
        self._turn = turn
        self.turns_without_attack = turns_without_attack
        # There is possible attack move
        self.can_attack = True
        # If last piece took an opponent piece
        if last_taker:
            # Back to last player
            self._turn = self.last_turn
            moves = self.get_moves([last_taker, ])
            # If can continue taking pieces
            if len(moves) != 0:
                self._legal_moves = moves
                return
            # If no possible moves then other player move
            self._turn = self.last_turn
        # If can't continue attack then other player search for the attack move
        # Taking is mandatory
        moves = self.get_moves(self._pieces_lists[turn - 1])
        # But if there is no attack move then search for the simple move
        if len(moves) == 0:
            moves = self.get_moves(self._pieces_lists[turn - 1], False)
            self.can_attack = False
        self._legal_moves = moves

    def get_moves(self, pieces: list[Checkers_piece], is_attack: bool = True) -> list[tuple[Move, Move]]:
        """Returns a list of possible moves (attack or simple)."""
        moves = []
        for piece in pieces:
            x, y = piece.location
            player = self.turn
            opponent = self.last_turn
            if piece.is_king:
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            else:
                if player == 1:
                    directions = [(-1, -1), (-1, 1)]
                else:
                    directions = [(1, 1), (1, -1)]
            for dx, dy in directions:
                if is_attack:
                    if 0 <= x+dx*2 < self._size and 0 <= y+dy*2 < self._size and \
                            self._field[x+dx][y+dy] == opponent and self._field[x+dx*2][y+dy*2] == 0:
                        moves.append(((x, y), (x+dx*2, y+dy*2)))
                else:
                    if 0 <= x+dx < self._size and 0 <= y+dy < self._size and \
                            self._field[x+dx][y+dy] == 0:
                        moves.append(((x, y), (x+dx, y+dy)))
        return moves

    def move(self, locations: tuple[Move, Move]) -> Board:
        last_pos, new_pos = locations
        new_field = deepcopy(self._field)
        # Turning into a king
        if (self.turn == 1 and new_pos[0] == 0) or (self.turn == 2 and new_pos[0] == self._size - 1):
            new_field[last_pos].is_king = True
            is_king = True
        else:
            is_king = False
        if locations not in self._legal_moves:
            raise IndexError('Bad move %s!' % str(locations))
        new_field[last_pos], new_field[new_pos] = new_field[new_pos], new_field[last_pos]
        new_field[new_pos].location = new_pos
        # Change piece location
        new_pieces_lists = deepcopy(self._pieces_lists)
        for piece in new_pieces_lists[self.turn - 1]:
            if piece.location == last_pos:
                piece.location = new_pos
                # Change simple piece to king in list
                if is_king:
                    piece.is_king = True
                break
        new_turn = self.last_turn
        last_taker = None
        turns_without_attack = self.turns_without_attack + 1
        if self.can_attack:
            turns_without_attack = 0
            # Remove opponent piece
            x, y = last_pos
            new_x, new_y = new_pos
            med_x, med_y = x + (new_x - x) // 2, y + (new_y - y) // 2
            for i in range(len(new_pieces_lists[self.last_turn - 1])):
                if new_pieces_lists[self.last_turn - 1][i].location == (med_x, med_y):
                    new_pieces_lists[self.last_turn - 1].pop(i)
                    new_field[med_x][med_y] = Checkers_piece(0)
                    break
            last_taker = new_field[new_pos]
        return Checkers(self._size, new_turn, new_field, new_pieces_lists, last_taker, turns_without_attack)

    @property
    def is_win(self) -> bool:
        if len(self._legal_moves) == 0 or (len(self._pieces_lists[self.turn - 1]) <= 1):
            return True
        return False

    @property
    def is_draw(self) -> bool:
        lens = (len(self._pieces_lists[0]), len(self._pieces_lists[1]))
        if min(lens) == 1 and max(lens) <= 3 and not self.can_attack:
            return True
        if self.turns_without_attack > 60:
            return True
        if max(lens) <= 5 and self.turns_without_attack > 30:
            return True
        if max(lens) <= 3 and self.turns_without_attack > 5:
            return True
        return False

    @property
    def legal_moves(self) -> list[tuple[Move, Move]]:
        return self._legal_moves

    def evaluate(self, player: int) -> float:
        if self.is_win and player == self.last_turn:
            return 100
        elif self.is_win and player != self.last_turn:
            return -100
        elif self.is_draw:
            return 0
        player_scores = sum((3 if piece.is_king else 1 for piece in self._pieces_lists[player - 1]))
        enemy_scores = sum((3 if piece.is_king else 1 for piece in self._pieces_lists[Piece.opposite(player) - 1]))
        scores = player_scores - enemy_scores
        if self.can_attack and self.turn == player:
            scores *= 1.1
        elif self.can_attack and self.turn != player:
            scores -= 0.1 * scores
        return scores


if __name__ == '__main__':
    from games.ai.decision_rule import find_best_move

    def test():
        wins = [0, 0]
        for k in range(10):
            board = Checkers()
            while not board.is_win:
                if board.turn == 2:
                    move = find_best_move(board, 6)
                else:
                    move = find_best_move(board, 4)
                board = board.move(move)
                print(board)
                print('-'*32)
            wins[board.last_turn - 1] += 1
            print('Win player %d!' % board.last_turn)
        print(wins)

    test()
