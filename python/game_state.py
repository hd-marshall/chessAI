from python.game_rules import Game_Rules

from typing import Dict, Tuple, List

class Game_State:

    def __init__(self) -> None:
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.rules = Game_Rules()
        self.clicked_squares : List[Tuple[int, int], Tuple[int, int]] = []
        self.player_colour : str = "w"
        self.move_number : int = 0

        self.valid_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        self.valid_opponent_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

    def scan_board(self, player_colour: str, opponent_colour: str, moves_dict: Dict[Tuple[int, int], List[Tuple[int, int]]]) -> None:
        
        n = len(self.board)

        for i in range(n):
            for j in range(n):

                if self.board[i][j] != "--" and self.board[i][j][0] == player_colour:

                    piece_type = self.board[i][j][1]
                    position = (i, j)
                    
                    moves_dict[position] = []
                    moves_dict[position].extend(self.rules.get_piece_move(piece_type, position, opponent_colour, self.board))

    def create_move_list(self) -> None:

        opponent = "w" if self.player_colour == "b" else "b"

        self.scan_board(self.player_colour, opponent, self.valid_moves)
        self.scan_board(opponent, self.player_colour, self.valid_opponent_moves)

        self.rules.checks(self.player_colour, self.valid_moves, self.valid_opponent_moves, self.board)

        """
        print(self.rules.pinned_pieces)
        if len(self.rules.pinned_pieces) > 0:

            for pinned_piece in self.rules.pinned_pieces:

                self.valid_moves[pinned_piece] = []
        """

    def update_move_list(self) -> None:
        pass

    def move(self) -> None:
        
        start_row = self.clicked_squares[0][0]
        start_col = self.clicked_squares[0][1]
        end_row = self.clicked_squares[1][0]
        end_col = self.clicked_squares[1][1]

        piece_value = self.board[start_row][start_col]

        self.board[end_row][end_col] = piece_value
        self.board[start_row][start_col] = "--"

        self.player_colour = "w" if self.player_colour == "b" else "b" 
        self.move_number += 1

        self.valid_moves.clear()
        self.valid_opponent_moves.clear()

    def get_legal_move(self, end_sqr) -> bool:
        
        start_sqr = self.clicked_squares[0]

        if start_sqr in self.valid_moves:
            if end_sqr in self.valid_moves[start_sqr]:

                return True
            
        return False

    def validate_clicked_sqrs(self, location: Tuple[int, int]) -> bool:
        
        row, col = location

        if not self.clicked_squares and self.board[row][col] == "--":
            return False
        
        self.clicked_squares.append(location)

        if self.get_legal_move(location):

            self.clicked_squares.append(location)
            self.move()
            self.clicked_squares.clear()
            return True
        
        else:
            self.clicked_squares.clear()
            self.clicked_squares.append(location)
        
    def create_guidelines(self) -> List[Tuple[int, int]]:

        guidelines_squares = []
        
        if len(self.clicked_squares) != 1:
            return guidelines_squares
        
        row, col = self.clicked_squares[0][0], self.clicked_squares[0][1]

        return self.valid_moves.get((row, col), [])