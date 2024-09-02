from classes.piece import *
from classes.square import Square


# check if the clicked position is a valid move for selected piece
def is_valid_move(selected_piece_cord, clicked_pos, moves):
    for move in moves:
        if move.initial == selected_piece_cord and move.final == clicked_pos:
            return True
    return False


# return the move that starts at the initial position from the list of moves
def find_move(initial, moves, final=None):
    matching_moves = [move for move in moves if move.initial == initial]

    # if final is provided, return the move that ends at the final position
    if final is not None:
        matching_move = [move for move in matching_moves if move.final == final]
        return matching_move[0]

    # otherwise return all moves that start at the initial position
    return matching_moves


class Board:

    def __init__(self):
        self.squares = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('red')

    # create the board
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    self.squares[row][col] = Square(row, col)

    # add pieces to the board
    def _add_pieces(self, color):
        init_rows = [5, 6, 7] if color == 'white' else [0, 1, 2]

        for row in init_rows:
            for col in range(COLS):
                if self.squares[row][col] != 0:
                    self.squares[row][col] = Square(row, col, Pawn(color))

    # move the piece, remove the attacked piece and promote the pawn to queen
    def move_piece(self, move):
        initial = move.initial
        final = move.final
        self.squares[final[0]][final[1]].piece = self.squares[initial[0]][initial[1]].piece
        self.squares[initial[0]][initial[1]].piece = None

        if move.attacked_piece:
            attacked_row, attacked_col = move.attacked_piece
            self.squares[attacked_row][attacked_col].piece = None

        if (final[0] == 0 or final[0] == 7) and self.squares[final[0]][final[1]].piece.name != 'queen':
            self.squares[final[0]][final[1]].piece = Queen(self.squares[final[0]][final[1]].piece.color)

    def all_available_moves(self, color):

        moves = []

        # for each piece of the given color, get all possible moves
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col] != 0 and self.squares[row][col].has_piece() and self.squares[row][col].piece.color == color:
                    piece = self.squares[row][col].piece
                    possible_moves = piece.possible_moves(self)
                    moves.extend(possible_moves)

        # if there are any moves that attack an opponent piece, return only those moves
        if any(move.attacked_piece is not None for move in moves):
            moves = list(filter(lambda x: x.attacked_piece is not None, moves))

        return moves

    # check if there is a winner or a tie
    def check_winners(self, turn):
        white = 0
        red = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col] != 0 and self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color == 'white':
                        white += 1
                    else:
                        red += 1
        if white == 0:
            print('Red wins')
            pygame.quit()
            quit()
        elif red == 0:
            print('White wins')
            pygame.quit()
            quit()
        elif not self.all_available_moves(turn):
            print("tie")
            pygame.quit()
            quit()
