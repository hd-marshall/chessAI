class GameState():
    #

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

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= len(self.board) - 1:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= len(self.board) - 1:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            while 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--":
                    moves.append(Move((r, c), (row, column), self.board))
                elif self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))
                    break
                else:
                    break
                row += dr
                column += dc

    def getKnightMoves(self, r, c, moves):
        directions = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            if 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--" or self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            while 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--":
                    moves.append(Move((r, c), (row, column), self.board))
                elif self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))
                    break
                else:
                    break
                row += dr
                column += dc

    def getQueenMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            while 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--":
                    moves.append(Move((r, c), (row, column), self.board))
                elif self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))
                    break
                else:
                    break
                row += dr
                column += dc

    def getKingMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            if 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--" or self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))

class Move():

    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rsToRanks = {v : k for k, v in ranksToRows.items()}
    filesToColumns = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, 
                      "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    csToFiles = {v : k for k, v in filesToColumns.items()}

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
        return self.csToFiles[c] + self.rsToRanks[r]