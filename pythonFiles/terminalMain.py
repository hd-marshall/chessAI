from pieces import *

class GameBoard:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]

    def __str__(self):
        board_str = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                board_str += str(self.board[i][j]) + ' '
            board_str += '\n'
        return board_str 

    def place_piece(self, piece, position):
        x, y = position
        self.board[x][y] = piece

    def begin_game(self):
        self.place_piece(Rook("black"), (0, 0))
        self.place_piece(Rook("black"), (0, 7))
        self.place_piece(Rook("white"), (7, 0))
        self.place_piece(Rook("white"), (7, 7))

        self.place_piece(Knight("black"), (0, 1))
        self.place_piece(Knight("black"), (0, 6))
        self.place_piece(Knight("white"), (7, 1))
        self.place_piece(Knight("white"), (7, 6))

        self.place_piece(Bishop("black"), (0, 2))
        self.place_piece(Bishop("black"), (0, 5))
        self.place_piece(Bishop("white"), (7, 2))
        self.place_piece(Bishop("white"), (7, 5))

        self.place_piece(Queen("black"), (0, 3))
        self.place_piece(Queen("white"), (7, 3))

        self.place_piece(King("black"), (0, 4))
        self.place_piece(King("white"), (7, 4))

        for i in range(8):
            self.place_piece(Pawn("black"), (1, i))
            self.place_piece(Pawn("white"), (6, i))
        
board = GameBoard()
board.begin_game()

while True:
    print(board)
    piece = input("What piece? ")
    move = input("What square? ")