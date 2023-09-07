import pygame as p
from chessBoard import ChessBoard

gameBoard = ChessBoard()

WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SCREEN_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages(piece):
    pieces = ["wp", ]
    IMAGES[piece] = p.image.load("python/chessAI/images" + piece + ".png")

p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Drag and Drop Chess")