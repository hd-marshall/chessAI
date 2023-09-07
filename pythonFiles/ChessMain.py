import pygame as p
import ChessEngine

WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in pieces:
        image_path = "python/chessAI/images/" + piece + ".png"
        image = p.image.load(image_path)
        image = p.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[piece] = image

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    #print(gameState.board)
    loadImages()

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()