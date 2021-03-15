from gtp_connection import GtpConnection
from board import GoBoard
import random
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    is_black_white,
    is_black_white_empty,
    coord_to_point,
    where1d,
    MAXSIZE,
    GO_POINT
)
class RandomPlayer(object):
    def __init__(self):
        pass

    def name(self):
        return "Random Player"

    def genMove(self, state):
        if state.winner() != EMPTY:
            return random.choice(state.legalMoves())
        else:
            return state.winner()

class Gomoku3():
    # def __init__(self):
    #     """
    #     Gomoku player that selects moves randomly from the set of legal moves.
    #     Passes/resigns only at the end of the game.
    #
    #     Parameters
    #     ----------
    #     name : str
    #         name of the player (used by the GTP interface).
    #     version : float
    #         version number (used by the GTP interface).
    #     """
    #     self.name = "GomokuAssignment3"
    #     self.version = 1.0

    def __init__(self, numSimulations):
        self.numSimulations = numSimulations

    def simulate(self, state, point, color):
        stats = [0] * 3
        state.play_move(point, color)
        moveNr = state.moveNumber()
        for _ in range(self.numSimulations):
            winner, temp = state.simulate()
            print(winner, temp)
            stats[winner] += 1
            state.resetToMoveNumber(moveNr)
        assert sum(stats) == self.numSimulations
        assert moveNr == state.moveNumber()
        state.undoMove()
        eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.numSimulations
        if state.current_player == WHITE:
            eval = 1 - eval
        return eval

    def genMove(self, state):
        moves = state.legalMoves()
        color = state.current_player
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            move = moves[i]
            score[i] = self.simulate(state, move, color)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        assert best in state.legalMoves()
        return best


    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move(board, color)

def selectPlayer(numMoves, player1, player2):
    if numMoves % 2 == 0:
        return player1
    else:
        return player2

def playGame(player1, player2):
    t = GoBoard(7)
    numMoves = 0
    while t.winner() == EMPTY and t.moveNumber() < 49:
        player = selectPlayer(numMoves, player1, player2)
        t.play_move(player.genMove(t), t.current_player)
        numMoves += 1
    #print("Game winner:", t.winner(), "Moves:", t.moves)
    return t.winner()

def playMatch(player1, player2, numGames):
    stats = [0] * 3
    for _ in range(numGames):
        winner = playGame(player1, player2)
        stats[winner] += 1
    printstats(stats, player1, player2)
    return stats

def printstats(stats, player1, player2):
    print("{0} wins for {1}, {2} wins for {3}, {4} draws".
          format(stats[BLACK], player1.name(),
                 stats[WHITE], player2.name(),
                 stats[EMPTY]))

def playMatchBothColors(player1, player2, numGames):
    # player1 is X
    stats1 = playMatch(player1, player2, numGames)
    # player1 is O
    stats2 = playMatch(player2, player1, numGames)
    # Compute combined statistics - reversed colors in second match
    stats1[BLACK] += stats2[WHITE]
    stats1[WHITE] += stats2[BLACK]
    stats1[EMPTY] += stats2[EMPTY]
    print("Total:")
    printstats(stats1, player1, player2)
    eval = (stats1[BLACK] + 0.5 * stats1[EMPTY]) / (2 * numGames)
    print("Percentage for {0} = {1:.2f}".format(player1.name(), 100 * eval))

def run():
    """
    start the gtp connection and wait for commands.
    """
    player1 = Gomoku3(1)
    player3 = RandomPlayer()
    playMatchBothColors(player1, player3, 1)


if __name__ == "__main__":
    run()
