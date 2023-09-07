import pygame

class GameState():

    def __init__(self):
        self.whiteToMove = True
        self.moveLog = []
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        print("done")
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        print("done")
        self.moveLog.append(move)
        print("done")
        self.whiteToMove = not self.whiteToMove

class Move():

    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    filesToColumns = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, 
                      "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    columnsToFiles = {v : k for k, v in filesToColumns.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = int(startSquare[0])
        self.startColumn = int(startSquare[1])
        self.endRow = int(endSquare[0])
        self.endColumn = int(endSquare[1])
        self.pieceMoved = board[self.startRow][self.startColumn] 
        self.pieceMovedTo = board[self.endRow][self.endColumn]
        print("done")

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, r, c):
        return self.columnsToFiles[c] + self.rowsToRanks[r]
    