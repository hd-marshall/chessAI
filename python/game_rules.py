from typing import Callable, Dict, Tuple, List, Union

class Game_Rules:

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
        self.player_colour : str = "w"

        # self.white_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = self.get_valid_moves("w", )
        # self.black_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = self.get_valid_moves("b", )

        self.pinned_pieces = [] #Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.in_check = False        
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.directions: Dict[str, Tuple[int, int]] = {
            "N": (-1, 0),
            "NE": (-1, 1),
            "E": (0, 1),
            "SE": (1, 1),
            "S": (1, 0),
            "SW": (1, -1),
            "W": (0, -1),
            "NW": (-1, -1),
        }
        self.reverse_directions = {v: k for k, v in self.directions.items()}
        self.piece_directions: Dict[str, List[Union[str, Tuple[int, int]]]] = {
            "R": ["N", "E", "S", "W"],
            "B": ["NE", "SE", "SW", "NW"],
            "Q": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
            "K": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        }

    
    def get_valid_moves(self, player_colour: str, board: List[List[str]]) ->  Dict[Tuple[int, int], List[Tuple[int, int]]]:

        move_list = {}
        opponent_colour = "b" if player_colour == "w" else "b"
        n = len(self.board)

        for i in range(n):
            for j in range(n):

                if self.board[i][j] != "--" and self.board[i][j][0] == player_colour:

                    piece_type = self.board[i][j][1]
                    position = (i, j)
                    
                    move_list[position] = []
                    move_list[position].extend(self.rules.get_piece_move(piece_type, position, opponent_colour, board))

        return move_list

    def update_valid_moves(self, player_colour: str) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        pass
    

    def get_piece_move(self, piece: str, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> List[Tuple[int, int]]:

        valid_piece_moves = []

        if piece == "K":
            valid_piece_moves = self.get_king_moves(start_sqr, opponent_colour, board)

        elif piece == "N":
            valid_piece_moves = self.get_knight_moves(start_sqr, opponent_colour, board)
        
        elif piece == "P":
            valid_piece_moves = self.get_pawn_moves(start_sqr, opponent_colour, board)
        
        else:
            for dir in self.piece_directions[piece]:
                valid_piece_moves.extend(self.get_direction_moves(dir, start_sqr, opponent_colour, board))

        return valid_piece_moves

    def get_direction_moves(self, dir: str, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> List[Tuple[int, int]]:

        valid_direction_moves = []

        r, c = start_sqr[0], start_sqr[1]
        dr, dc = self.directions[dir]

        row, column = r + dr, c + dc

        while 0 <= row < len(board) and 0 <= column < len(board):
            if board[row][column] == "--":
                end_sqr = (row, column)
                valid_direction_moves.append(end_sqr)

            elif board[row][column][0] == opponent_colour:
                end_sqr = (row, column)
                valid_direction_moves.append(end_sqr)
                self.pins(dir, end_sqr, opponent_colour, board)
                break
            else:
                break

            row += dr
            column += dc
        
        return valid_direction_moves

    def get_king_moves(self, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> List[Tuple[int, int]]:
        
        if opponent_colour == "w":
            self.white_king_location = start_sqr
        else:
            self.black_king_location = start_sqr

        directions = self.piece_directions["K"]
        r, c = start_sqr[0], start_sqr[1]
        
        valid_king_moves = []

        for dir in directions:
            dr, dc = self.directions[dir]
            row, column = r + dr, c + dc

            if 0 <= row < len(board) and 0 <= column < len(board):
                if board[row][column] == "--" or board[row][column][0] == opponent_colour:
                    
                    end_sqr = (row, column)
                    valid_king_moves.append(end_sqr)
        
        return valid_king_moves

    def get_knight_moves(self, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> List[Tuple[int, int]]:
        
        directions = [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        r, c = start_sqr[0], start_sqr[1]

        valid_knight_moves = []

        for dr, dc in directions:
            row, column = r + dr, c + dc

            if 0 <= row < len(board) and 0 <= column < len(board):
                if board[row][column] == "--" or board[row][column][0] == opponent_colour:
                    end_sqr = (row, column)
                    valid_knight_moves.append(end_sqr)

        return valid_knight_moves

    def get_pawn_moves(self, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> List[Tuple[int, int]]:
        
        r, c = start_sqr[0], start_sqr[1]
        curr_turn = "b" if opponent_colour == "w" else "w"

        valid_pawn_moves = []

        self.promote_pawn(start_sqr, opponent_colour, board)

        if curr_turn == "w":
            if board[r - 1][c] == "--":
                valid_pawn_moves.append((r - 1, c))

                if r == 6 and board[r - 2][c] == "--":
                    valid_pawn_moves.append((r - 2, c))

            if c - 1 >= 0:
                if board[r - 1][c - 1][0] == opponent_colour:
                    valid_pawn_moves.append((r - 1, c - 1))

            if c + 1 <= len(board) - 1:
                if board[r - 1][c + 1][0] == opponent_colour:
                    valid_pawn_moves.append((r - 1, c + 1))

        elif r + 1 < 8:
            if board[r + 1][c] == "--":
                valid_pawn_moves.append((r + 1, c))

                if r == 1 and board[r + 2][c] == "--":
                    valid_pawn_moves.append((r + 2, c))

            if c - 1 >= 0:
                if board[r + 1][c - 1][0] == opponent_colour:
                    valid_pawn_moves.append((r + 1, c - 1))

            if c + 1 <= len(board) - 1:
                if board[r + 1][c + 1][0] == opponent_colour:
                    valid_pawn_moves.append((r + 1, c + 1))

        return valid_pawn_moves

    def promote_pawn(self, promote_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> Tuple[Tuple[int, int]]:

        curr_turn = "b" if opponent_colour == "w" else "w"
        r, c = promote_sqr[0], promote_sqr[1]

        if curr_turn == "w" and r == 0:
            board[r][c] = "wQ"

        elif curr_turn == "b" and r == 7:
            board[r][c] = "bQ"

    def square_under_attack_direction(self, sqr, attacking_pieces, board):
            
        attacked_row, attacked_col = sqr
        attack_row, attack_col = attacking_pieces[0]
        attack_piece = board[attack_row][attack_col][1]

        # Calculate the direction vector from the attacking piece to the king
        dir_row = attacked_row - attack_row
        dir_col = attacked_col - attack_col

        # Handle knight separately
        if attack_piece == 'N':
            if (abs(dir_row), abs(dir_col)) in [(1,2), (2,1)]:
                return (dir_row, dir_col)  # Return the non-normalized direction for knights
        else:
            # Normalize the direction vector for other pieces
            length = max(abs(dir_row), abs(dir_col))
            if length != 0:
                dir_row = dir_row // length
                dir_col = dir_col // length

            direction_tuple = (dir_row, dir_col)

            if direction_tuple in self.reverse_directions:
                direction_str = self.reverse_directions[direction_tuple]

                return direction_str

        return None  # If no valid attack direction is found
    
    def square_under_attack(self, sqr: Tuple[int, int], opponent_moves: Dict[Tuple[int, int], List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
        
        attacking_pieces = []

        for piece, moves in opponent_moves.items():
            if sqr in moves:
                
                attacking_pieces.append(piece)
        
        return attacking_pieces

    def checks(self, turn_take: str, player_moves: Dict[Tuple[int, int], List[Tuple[int, int]]], opponent_moves: Dict[Tuple[int, int], List[Tuple[int, int]]], board) -> None:

        king_location = self.white_king_location if turn_take == "b" else self.black_king_location

        attacking_pieces = self.square_under_attack(king_location, opponent_moves)

        # If 1 Piece is attacking the King.
        if len(attacking_pieces) == 1:
            
            attack_piece = attacking_pieces[0]
            attacked_dir = self.square_under_attack_direction(king_location, attacking_pieces, board)
            attacked_sqrs = self.get_direction_moves(attacked_dir, attacking_pieces[0], turn_take, board)

            for piece, moves in player_moves.items():
                
                new_valid_moves = []    

                for move in moves:
                    if piece == king_location:
                        if move not in attacked_sqrs or attack_piece == move:
                            new_valid_moves.append(move)

                    else:
                        if move in attacked_sqrs or attack_piece == move:
                            new_valid_moves.append(move)

                player_moves[piece] = new_valid_moves

        # If more then 1 Piece is attacking the King.
        if len(attacking_pieces) > 1:

            player_moves.clear()

            for moves in player_moves[king_location]:
                if move not in attacked_sqrs:
                    player_moves[king_location].extend(move)

    def checkmate(self) -> None:
        pass

    def pins(self, dir: str, start_sqr: Tuple[int, int], opponent_colour: str, board: List[List[str]]) -> None:
        
        opponent_king = self.white_king_location if opponent_colour == "b" else self.black_king_location

        r, c = start_sqr[0], start_sqr[1]
        dr, dc = self.directions[dir]

        row, column = r + dr, c + dc

        while 0 <= row < len(board) and 0 <= column < len(board):

            if board[row][column] == "--":

                row += dr
                column += dc

            elif (row, column) != opponent_king:

                break
        
            elif (row, column) == opponent_king:

                self.pinned_pieces.append(start_sqr)
                break