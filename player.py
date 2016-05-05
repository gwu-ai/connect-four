from minimax import Minimax
from connect4 import COLUMN


class Player(object):

    type = None  # possible types are "Human" and "AI"
    name = None
    color = None
    is_max_player = None

    def __init__(self, name, color, is_max_player):
        self.type = "Human"
        self.name = name
        self.color = color
        self.is_max_player = is_max_player

    def move(self, state):
        print("{0}'s turn. ".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= COLUMN - 1:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):

    difficulty = None

    def __init__(self, name, color, is_max_player, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.is_max_player = is_max_player

    def move(self, state):
        print("{0}'s turn. ".format(self.name))

        m = Minimax(state)
        best_move, value = m.alphaBetaBestMove(self.difficulty, state, self.color)

        return best_move
