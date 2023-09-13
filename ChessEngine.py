class GameState():

    def __init__(self):
        self.whiteToMove = True
        self.moveLog = []
        """self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]"""
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "--", "wP", "wP", "wP", "--", "wP"],
        ["wR", "--", "--", "wQ", "wK", "--", "--", "wR"]
        ]

    def checkTeammate(self, move):
        if move.pieceMoved[0] == move.pieceMovedTo[0]:
            return False

    def checkColour(self, move):
        if self.checkTeammate(move) == False:
            return False

        if self.whiteToMove == True and move.pieceMoved[0] == "w":
            return self.whatPiece(move)
        elif self.whiteToMove == False and move.pieceMoved[0] == "b":
            return self.whatPiece(move)
        else:
            return False
        
    def whatPiece(self, move):
        if move.pieceMoved[1] == "P":
            return self.pawnMove(move)
        elif move.pieceMoved[1] == "R":
            return self.rookMove(move)
        elif move.pieceMoved[1] == "N":
            pass
        elif move.pieceMoved[1] == "B":
            pass
        elif move.pieceMoved[1] == "Q":
            pass
        elif move.pieceMoved[1] == "K":
            pass

    def pawnMove(self, move):
        validMove = False
        pawnColour = move.pieceMoved[0]

        if pawnColour == "w":
            if move.startRow == 6:
                if move.startRow - 2 == move.endRow and move.startColumn == move.endColumn:
                    validMove = True     
            if move.startRow - 1 == move.endRow and move.startColumn == move.endColumn:
                validMove = True
            if move.startRow - 1 == move.endRow and move.startColumn - 1 == move.endColumn and self.board[move.endRow][move.endColumn][0] == "b":
                validMove = True
            elif move.startRow - 1 == move.endRow and move.startColumn + 1 == move.endColumn and self.board[move.endRow][move.endColumn][0] == "b":
                validMove = True

        if pawnColour == "b":
            if move.startRow == 1:
                if move.startRow + 2 == move.endRow and move.startColumn == move.endColumn:
                    validMove = True     
            if move.startRow + 1 == move.endRow and move.startColumn == move.endColumn:
                validMove = True
            if move.startRow + 1 == move.endRow and move.startColumn - 1 == move.endColumn and self.board[move.endRow][move.endColumn][0] == "w":
                validMove = True
            elif move.startRow + 1 == move.endRow and move.startColumn + 1 == move.endColumn and self.board[move.endRow][move.endColumn][0] == "w":
                validMove = True

        return validMove
    
    def rookMove(self, move):
        validMove = False
        
        if move.startRow == move.endRow:
            print("row")
            for column in range(6):
                if self.board[move.startRow][move.startColumn + column + 1][0] == "w":
                    validMove = False
                    break
                else:
                    validMove = True

        if move.startColumn == move.endColumn:
            print("col")
            for row in range(6):
                if self.board[move.startRow - row - 1][move.startColumn][0] == "w":
                    validMove = False
                    break
                else:
                    validMove = True

        return validMove
            

    def makeMove(self, move):
        if self.checkColour(move) == True:
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

    def validMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
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

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, r, c):
        return self.columnsToFiles[c] + self.rowsToRanks[r]