import pygame
from pieces import *

class ChessBoard():

    def __init__(self):
        self.createBoard()

    def fillBoard(self, screen, squareSize):
        r1 = Rook("black")
        r1_rect = r1.image.get_rect()
        r1_rect.topleft = (7 * squareSize, 0 * squareSize)

        screen.blit(r1.image, r1_rect.topleft)

    def createBoard(self):
        pygame.init()

        width, height = 400, 400
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chessboard")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

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

            self.fillBoard(self.screen, self.square_size)
            pygame.display.flip()

        pygame.quit()