import pygame
from pieces import *

class ChessBoard():

    def __init__(self):
        self.blackPieces = []
        self.whitePieces = []
        self.createBoard()

    def fillBoard(self, screen, squareSize):
        for row in range(8):
            for col in range(8):
                piece = None
                if row == 0:
                    if col == 0 or col == 7:
                        piece = Rook("black")
                        self.blackPieces.append(piece)
                    elif col == 1 or col == 6:
                        piece = Knight("black")
                        self.blackPieces.append(piece)
                    elif col == 2 or col == 5:
                        piece = Bishop("black")
                        self.blackPieces.append(piece)
                    elif col == 3:
                        piece = Queen("black")
                        self.blackPieces.append(piece)
                    elif col == 4:
                        piece = King("black")
                        self.blackPieces.append(piece)
                elif row == 7:
                    if col == 0 or col == 7:
                        piece = Rook("white")
                        self.whitePieces.append(piece)
                    elif col == 1 or col == 6:
                        piece = Knight("white")
                        self.whitePieces.append(piece)
                    elif col == 2 or col == 5:
                        piece = Bishop("white")
                        self.whitePieces.append(piece)
                    elif col == 3:
                        piece = Queen("white")
                        self.whitePieces.append(piece)
                    elif col == 4:
                        piece = King("white")
                        self.whitePieces.append(piece)
                elif row == 1:
                    piece = Pawn("black")
                    self.blackPieces.append(piece)
                elif row == 6:
                    piece = Pawn("white")
                    self.whitePieces.append(piece)

                if piece:
                    piece_rect = piece.image.get_rect()
                    piece_rect.topleft = (col * squareSize, row * squareSize)
                    screen.blit(piece.image, piece_rect.topleft)

    def createBoard(self):
        pygame.init()

        fill = False
        width, height = 500, 500
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Drag and Drop Chess")

        self.white = (255, 222, 173)
        self.black = (160, 82, 45)

        self.rows, self.cols = 8, 8
        self.square_size = width // self.cols

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for row in range(self.rows):
                for col in range(self.cols):
                    color = self.white if (row + col) % 2 == 0 else self.black
                    pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

            if fill == False:
                self.fillBoard(self.screen, self.square_size)
            pygame.display.flip()

        pygame.quit()