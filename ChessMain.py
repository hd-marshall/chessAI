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
    p.display.set_caption("Drag and Drop Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    loadImages()
    squareSelected = ()
    playerClicks = []

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                clickRow = location[1] // SQUARE_SIZE
                clickColumn = location[0] // SQUARE_SIZE
                if squareSelected == (clickRow, clickColumn):
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (clickRow, clickColumn)
                    playerClicks.append(squareSelected)
                
                if len(playerClicks) == 2:
                    

        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    white = (255, 253, 208)
    black = (139, 69, 19)

    boardColours = [p.Color(white), p.Color(black)]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            colour = boardColours[((row + column) % 2)]
            p.draw.rect(screen, colour, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()