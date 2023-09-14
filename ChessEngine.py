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
        self.moveFunctions = {"P" : self.getPawnMoves, "R" : self.getRookMoves, "N" : self.getKnightMoves, 
                              "B" : self.getBishopMoves, "Q" : self.getQueenMoves, "K" : self.getKingMoves}

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceMovedTo
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves)
        return moves

    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove:
            if self.board[row - 1][column] == "--":
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "--":
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))

        else:
            if self.board[row + 1][column] == "--":
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "--":
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def getRookMoves(self, row, column, moves):
        pass

    def getKnightMoves(self, row, column, moves):
        pass

    def getBishopMoves(self, row, column, moves):
        pass

    def getQueenMoves(self, row, column, moves):
        pass

    def getKingMoves(self, row, column, moves):
        pass


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
        self.pieceName = board[self.startRow][self.startColumn][1]
        self.moveID = self.startRow * 1000 + self.endColumn * 100 + self.endRow * 10 + self.endColumn

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, r, c):
        return self.columnsToFiles[c] + self.rowsToRanks[r]