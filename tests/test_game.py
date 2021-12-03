from random import choice

import pytest


from games.checkers import Checkers
from games.five_in_a_row import Five_in_a_row
from games.flume import Flume
from games.hare_and_wolves import Hare_and_wolves
from games.reversi import Reversi
from games.talpa import Talpa
from games.virus_war import Virus_war
from games.ai.decision_rule import find_best_move


@pytest.fixture(params=[Checkers, Five_in_a_row, Flume, Hare_and_wolves,
                        Reversi, Talpa, Virus_war],
                ids=lambda x: f"Game {x.__name__}")
def Board(request: pytest.FixtureRequest) -> type:
    """Game board class"""
    return request.param


class TestGame:

    def test_random_moves_game_with_statistics(self, Board):
        """Play 100 games with random moves"""
        moves_counters = []
        win_draw_counters = [0, 0, 0]
        for _ in range(100):
            i = 0
            board = Board()
            while True:
                move = choice(board.legal_moves)
                board = board.move(move)
                if board.is_win:
                    win_draw_counters[board.last_turn - 1] += 1
                    break
                elif board.is_draw:
                    win_draw_counters[-1] += 1
                    break
                assert i < 1000, "Too long game!"
                i += 1
            moves_counters.append(i)
        print(f'\n{Board.__name__}')
        print()
        print(f"Avg moves: {round(sum(moves_counters) / len(moves_counters))}")
        print(f"Max moves: {max(moves_counters)}")
        print(f"Min moves: {min(moves_counters)}")
        print()
        print(f"Player 1 win: {win_draw_counters[0]}")
        print(f"Player 2 win: {win_draw_counters[1]}")
        print(f"Draws: {win_draw_counters[2]}")
        print("_"*32)

    @pytest.mark.parametrize("player_1", [{'max_depth': 0, 'randomizing': 20},
                                          {'max_depth': 1, 'randomizing': 0}],
                             ids=lambda x: f"Player 1 {x}")
    @pytest.mark.parametrize("player_2", [{'max_depth': 0, 'randomizing': 20},
                                          {'max_depth': 1, 'randomizing': 0}],
                             ids=lambda x: f"Player 2 {x}")
    def test_ai_game(self, Board, player_1, player_2):
        """Test easy and smart AI combinations"""
        board = Board()
        print(f'\n{Board.__name__}')
        difficulty_params = [player_1, player_2]
        while True:
            move = find_best_move(board, **difficulty_params[board.turn - 1])
            board = board.move(move)
            if board.is_win:
                print(f"Player {board.last_turn} is winner!")
                break
            elif board.is_draw:
                print(f"Game drawn!")
                break

    def test_wrong_moves(self, Board):
        """Try to make illegal move"""
        board = Board()
        print(f'\n{Board.__name__}')
        bad_moves = []
        with pytest.raises(IndexError):
            for i in range(10):
                move = choice(board.legal_moves)
                board = board.move(move)
                bad_moves.append(move)
            print(board)
            for move in bad_moves:
                board.move(move)
