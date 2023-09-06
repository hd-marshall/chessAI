import pygame
from chessBoard import ChessBoard
from pieces import *

gameBoard = ChessBoard()

for i in range(len(gameBoard.blackPieces)):
    if isinstance(gameBoard.blackPieces[i], Rook):
        print("Rook " + str(i))