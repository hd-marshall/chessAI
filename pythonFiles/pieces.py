import pygame

class Piece:

    def __init__(self, colour):
        self.colour = colour
        self.image = None

    def load_image(self, image_path):
        self.image = pygame.image.load(image_path)
    
class Pawn(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "Pawn.png"
        super().__init__(colour)
        self.load_image(imagePath)

    def move(self):
        pass

class Knight(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "Knight.png"
        super().__init__(colour)
        self.load_image(imagePath)

    def move(self):
        pass

class Bishop(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "Bishop.png"
        super().__init__(colour)
        self.load_image(imagePath)

    def move(self):
        pass

class Rook(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "Rook.png"
        super().__init__(colour)
        self.load_image(imagePath)
    
    def move(self):
        pass

class Queen(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "Queen.png"
        super().__init__(colour)
        self.load_image(imagePath)

    def move(self):
        pass

class King(Piece):

    def __init__(self, colour):
        imagePath = "/Users/harrymarshall/Developer/python/chessAI/images/" + colour + "King.png"
        super().__init__(colour)
        self.load_image(imagePath)
    
    def move(self):
        pass
