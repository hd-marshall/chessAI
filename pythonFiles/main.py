import pygame as p
from chessBoard import ChessBoard

gameBoard = ChessBoard()
print(gameBoard.board)

WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SCREEN_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages(piece):
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in range(len(pieces)):
        IMAGES[piece] = p.image.load("python/chessAI/images" + piece + ".png")

p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Drag and Drop Chess")