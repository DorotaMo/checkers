import pygame
from classes.const import *
from classes.move import Move


# check if the position is in the board
def is_in_board(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


class Piece:
    def __init__(self, name, color, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    # set the texture of the piece
    def set_texture(self):
        self.texture = pygame.image.load('images/' + self.color + '_' + self.name + '.png')
        pass

    # return the move if it is valid
    def move(self, board, coord, vertical, horizontal):
        next_position = (coord[0] + vertical, coord[1] + horizontal)
        if is_in_board(next_position[0], next_position[1]):
            # if square is empty
            if not board.squares[next_position[0]][next_position[1]].has_piece():
                return Move(coord, next_position)
            # if square has a piece of the opposite color
            elif board.squares[next_position[0]][next_position[1]].piece.color != self.color:
                attacked_coords = next_position
                next_position = next_position[0] + vertical, next_position[1] + horizontal
                # if square after opposite color is empty
                if is_in_board(next_position[0], next_position[1]) and not board.squares[next_position[0]][next_position[1]].has_piece():
                    return Move(coord, next_position, attacked_coords)

    # return a list of possible moves for the piece
    def possible_moves(self, board):
        list_of_moves = []
        row = self.texture_rect.top // SQSIZE
        col = self.texture_rect.left // SQSIZE
        coords = (row, col)

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if not self.dir else [(self.dir, 1), (self.dir, -1)]
        for direction in directions:
            move = self.move(board, coords, direction[0], direction[1])
            if move:
                list_of_moves.append(move)
        return list_of_moves


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color)


class Queen(Piece):

    def __init__(self, color):
        self.dir = 0
        super().__init__('queen', color, )
