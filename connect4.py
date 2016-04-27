
COLUMN = 7
ROW = 6
BOARD_SIZE = COLUMN * ROW
STREAK = 4

import random
import os
import time

from player import Player, AIPlayer

class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """

    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = u"Connect Four"
    names = ["x", "o"]
    colors = ["x", "o"]

    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

        # do cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"Welcome to {0}!".format(self.game_name))
        print("The first player is x, and the second player is o.")
        print("Should Player 1 be a Human or a Computer?")

        while self.players[0] == None:
            choice = str(input("Type 'H' or 'C': "))
            if choice.lower() == "human" or choice.lower() == "h":
                self.players[0] = Player(self.names[0], self.colors[0], True)
            elif choice.lower() == "computer" or choice.lower() == "c":
                diff = int(input("Enter difficulty for this AI (1 - 5) "))
                self.players[0] = AIPlayer(self.names[0], self.colors[0], True, diff + 1)
            else:
                print("Invalid choice, please try again")

        print("Should Player 2 be a Human or a Computer?")
        while self.players[1] == None:
            choice = str(input("Type 'H' or 'C': "))
            if choice.lower() == "human" or choice.lower() == "h":
                self.players[1] = Player(self.names[1], self.colors[1], False)
            elif choice.lower() == "computer" or choice.lower() == "c":
                diff = int(input("Enter difficulty for this AI (1 - 5) "))
                self.players[1] = AIPlayer(self.names[1], self.colors[1], False, diff + 1)
            else:
                print("Invalid choice, please try again")

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(ROW):
            self.board.append([])
            for j in range(COLUMN):
                self.board[i].append(' ')

    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(ROW):
            self.board.append([])
            for j in range(COLUMN):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only BOARD_SIZE legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > BOARD_SIZE:
            self.finished = True
            # this would be a stalemate :(
            return

        # move is the column that player want's to play
        move = player.move(self.board)

        for i in range(ROW):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return

    def checkForFours(self):
        # for each piece in the board...
        for i in range(ROW):
            for j in range(COLUMN):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return

    def verticalCheck(self, row, col):
        # print("checking vert")
        fourInARow = False
        consecutiveCount = 0

        for i in range(row, ROW):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for j in range(col, COLUMN):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, ROW):
            if j > ROW:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > ROW:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope

    def findFours(self):
        """ Finds start i,j of four-in-a-row
            Calls highlightFours
        """

        for i in range(ROW):
            for j in range(COLUMN):
                if self.board[i][j] != ' ':
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')

                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')

                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)

    def highlightFour(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """

        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def printState(self):
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(COLUMN):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")
