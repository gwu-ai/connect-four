import random

from connect4 import COLUMN
from connect4 import ROW


class Minimax(object):
    board = None
    colors = ["x", "o"]

    def __init__(self, board):
        self.board = [x[:] for x in board]

    def alphaBetaBestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for col in range(COLUMN):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.alphaBetaSearch(temp, depth - 1, -float("inf"), float("inf"), opp_player, True)

        best_alpha = -float("inf")
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def alphaBetaSearch(self, state, depth, alpha, beta, curr_player, is_max_player):
        legal_states = []
        for i in range(COLUMN):
            if self.isLegalMove(i, state):
                temp = self.makeMove(state, i, curr_player)
                legal_states.append(temp)

        if depth == 0 or len(legal_states) == 0 or self.gameIsOver(state):
            return self.value(state, curr_player)

        if is_max_player:
            max_val = alpha
            for legal_state in legal_states:
                oppo_player = self.getOppPlayer(curr_player)
                child_val = self.alphaBetaSearch(legal_state, depth - 1, max_val, beta, oppo_player, False)

                if child_val >= max_val:
                    max_val = child_val

                if beta <= max_val:
                    break
            return max_val
        elif not is_max_player:
            min_val = beta
            for legal_state in legal_states:
                oppo_player = self.getOppPlayer(curr_player)
                child_val = self.alphaBetaSearch(legal_state, depth - 1, alpha, min_val, oppo_player, True)

                if child_val <= min_val:
                    min_val = child_val

                if alpha >= min_val:
                    break
            return min_val


    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for col in range(COLUMN):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth - 1, temp, opp_player)

        best_alpha = -float("inf")
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(COLUMN):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)


        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -float("inf")
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))
        return alpha

    def getOppPlayer(self, curr_player):
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]
        return opp_player

    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """

        for i in range(ROW):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False

    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        for i in range(ROW):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """
        Heuristic evaluation function:
        player(10000 * 4-in-a-row + 100 * 3-in-a-row + 1 * 2-in-a-row)
        """

        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_fours = self.checkForStreak(state, o_color, 4)
        #opp_threes = self.checkForStreak(state, o_color, 3)
        #opp_twos = self.checkForStreak(state, o_color, 2)

        if opp_fours:
            return -10000
        else:
            return my_fours * 10000 + my_threes * 100 + my_twos# - opp_fours * 10000 - opp_threes * 100 - opp_twos

    def checkForStreak(self, state, color, streak):
        count = 0
        for i in range(ROW):
            for j in range(COLUMN):
                if state[i][j].lower() == color.lower():
                    count += self.verticalStreak(i, j, state, streak)
                    count += self.horizontalStreak(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, ROW):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, COLUMN):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, ROW):
            if j > ROW:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > ROW:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total
