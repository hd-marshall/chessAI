import os
import pygame as p
import pygame.mixer as pm
import ChessEngine

WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wP"]
    for piece in pieces:
        image_path = "/Users/harrymarshall/Developer/python/chessAI/images/" + piece + ".png"
        image = p.image.load(image_path)
        image = p.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES[piece] = image

def main():
    p.init()
    pm.init()
    clicks = pm.Sound("/Users/harrymarshall/Developer/python/chessAI/sounds/click1.wav")
    clicksError = pm.Sound("/Users/harrymarshall/Developer/python/chessAI/sounds/click2Error.wav")
    clicks.set_volume(0.5)
    clicksError.set_volume(0.5)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess: The Game")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
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
                clickRow = int(location[1] // SQUARE_SIZE)
                clickColumn = int(location[0] // SQUARE_SIZE)
                if squareSelected == (clickRow, clickColumn):
                    squareSelected = ()
                    playerClicks = []
                    clicksError.play()
                elif len(playerClicks) < 1 and gameState.board[clickRow][clickColumn] == "--":
                    squareSelected = ()
                    clicksError.play()
                else:
                    squareSelected = (clickRow, clickColumn)
                    playerClicks.append(squareSelected)
                    clicks.play()
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                        squareSelected = ()
                        playerClicks = []
                    else: 
                       playerClicks = [squareSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
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