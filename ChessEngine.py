class GameState():

    # ! Bishops move wrong sometimes but are on correct squares.
    # ! When in check pieces move wrong or cant take at all.

    # TODO: Pieces when in check will jump and not move correctly sometimes not allowing the game to flow properly. The lack of a logical intregrity in the piece move function may be leaking into
    # TODO: the inCheck() and getValidMoves() functions.

    def __init__(self):
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
        self.whiteToMove = True
        self.moveLog = []
        
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        
        self.inCheck = False
        self.checkMate = False
        self.stalemate = False

        self.pins = []
        self.checks = []

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endColumn)
        self.promotePawn(move.endRow, move.endColumn)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceMovedTo
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startColumn)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startColumn)

    def getValidMoves(self): 
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKnightMoves(kingRow, kingCol, moves)
        else: #not in check so all moves are okay
            moves = self.getAllPossibleMoves()

        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColour = "b"
            allyColour = "w"
            startRow = self.whiteKingLocation[0]
            startCol  = self.whiteKingLocation[1]
        else:
            enemyColour = "w"
            allyColour = "b"
            startRow = self.blackKingLocation[0]
            startCol  = self.blackKingLocation[1]

            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
            for j in range(len(directions)):
                d = directions[j]
                possiblePin = ()
                for i in range(1, 8):
                    endRow = startRow + d[0] * i
                    endCol = startCol + d[1] * i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == allyColour:
                            if possiblePin == ():
                                possiblePin = (endRow, endCol, d[0], d[1])
                            else:
                                break
                        elif endPiece[0] == enemyColour:
                            type = endPiece[1]
                            if (0 <= j <= 3 and type == 'R') or \
                                    (4 <= j <= 7 and type == 'B') or \
                                    (i == 1 and type == 'p' and ((enemyColour == 'w' and 6 <= j <= 7) or (enemyColour == 'b' and 4 <= j <= 5))) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                                if possiblePin == (): #no piece blocking, so check
                                    inCheck = True
                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                                else: #piece blocking so pin
                                    pins.append(possiblePin)
                            else: #enemy piece not applying check
                                break
                else:
                    break
        
        knightMoves = ((-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColour and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endColumn == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    
    def checkmate(self):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1)]

        if self.whiteToMove:
            r, c = self.blackKingLocation
            turnTake  = "w"
        else:
            r, c = self.whiteKingLocation
            turnTake = "b"

        for dr, dc in directions:
            row, column = r + dr, c + dc

            if 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--" or self.board[row][column][0] == turnTake: 
                    if self.squareUnderAttack(row, column) != True:
                        return False
            
        return True

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
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= len(self.board) - 1:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def promotePawn(self, r, c):
        colour = self.board[r][c][0]
        piece = self.board[r][c][1]

        if colour == "w" and r == 0:
            if piece == "P":
                self.board[r][c] = "wQ"

        if colour == "b" and r == 7:
            if piece == "P":
                self.board[r][c] = "bQ"

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
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
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
        """directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
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
                column += dc"""

        self.getRookMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
        turnTake = "b" if self.whiteToMove else "w"

        for dr, dc in directions:
            row, column = r + dr, c + dc
            if 0 <= row < len(self.board) and 0 <= column < len(self.board):
                if self.board[row][column] == "--" or self.board[row][column][0] == turnTake:
                    moves.append(Move((r, c), (row, column), self.board))
                    print(str(row) + " " + str(column))

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