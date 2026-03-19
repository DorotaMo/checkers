import pygame
from classes.const import *
from classes.move import Move


# check if the position is in the board
def is_in_board(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


class Piece:
    def __init__(self, name, color, direction):
        self.direction = direction
        self.name = name
        self.color = color

    # return the move if it is valid
    def move(self, board, coord, vertical, horizontal, attacked_coords=None, list_of_moves=None, current_move=None):
        if attacked_coords is None:
            attacked_coords = []

        if list_of_moves is None:
            list_of_moves = []

        if current_move is None:
            current_move = []

        next_position = (coord[0] + vertical, coord[1] + horizontal)

        if is_in_board(next_position[0], next_position[1]):
            # if square is empty
            if not board.squares[next_position[0]][next_position[1]].has_piece() and attacked_coords == []:
                list_of_moves.append(Move(coord, next_position))
                return list_of_moves
            elif not board.squares[next_position[0]][next_position[1]].has_piece() and attacked_coords != []:
                # no move available since this is not the first move
                return
            # if square has a piece of the opposite color
            elif board.squares[next_position[0]][next_position[1]].piece.color != self.color:
                # Save the current position as the attacked piece's coordinates
                attacked_positions = next_position
                # Calculate the position after jumping over the attacked piece
                next_position = (next_position[0] + vertical, next_position[1] + horizontal)

                # If the square after the attacked piece is empty
                if is_in_board(next_position[0], next_position[1]) and not board.squares[next_position[0]][next_position[1]].has_piece():

                    # Check if the move is not a part of the current move
                    if current_move:
                        if (coord, next_position) in [(move.initial, move.final) for move in current_move]:
                            return
                        elif (coord, next_position) in [(move.final, move.initial) for move in current_move]:
                            return

                    # Append attacked position to the list
                    attacked_coords.append(attacked_positions)
                    current_move.append(Move(coord, next_position, attacked_coords))

                    # Recursively calculate moves from the new position
                    try:
                        self.move(board, next_position, vertical, horizontal, attacked_coords.copy(), list_of_moves, current_move.copy())
                        self.move(board, next_position, vertical, -horizontal, attacked_coords.copy(), list_of_moves, current_move.copy())

                        if self.direction == 0:
                            self.move(board, next_position, -vertical, horizontal, attacked_coords.copy(), list_of_moves, current_move.copy())

                    except RecursionError:
                        print("Błąd rekurencji: Zatrzymano dalszą rekurencję.")
                        input("Czy chcesz kontynuować? (t/n): ")

                    list_of_moves.append(Move(current_move[0].initial, current_move[-1].final, current_move[-1].attacked_pieces))

            else:
                return None

        return list_of_moves

    # return a list of possible moves for the piece
    def possible_moves(self, board, coords2):
        list_of_moves = []
        coords = coords2

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if not self.direction else [(self.direction, 1),
                                                                                      (self.direction, -1)]
        for direction in directions:
            moves = self.move(board, coords, direction[0], direction[1])
            if moves:
                for move in moves:
                    if move.attacked_pieces:
                        if not any(set(move.attacked_pieces).issubset(set(m.attacked_pieces)) and len(move.attacked_pieces) != len(m.attacked_pieces) and move != m for m in moves):
                            list_of_moves.append(move)
                    else:
                        list_of_moves.append(move)

        return list_of_moves


class Pawn(Piece):

    def __init__(self, color):
        pawn_direction = -1 if color == 'white' else 1
        super().__init__('pawn', color, pawn_direction)


class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 0)
