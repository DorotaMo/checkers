import pygame
from classes.const import *
from classes.board import Board


class Game:

    def __init__(self):
        self.board = Board()

    # drawing the board
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, (201, 156, 119), (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE))
                else:
                    pygame.draw.rect(surface, (91, 60, 17), (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE))

    # displaying the pieces
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col] != 0 and self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    img = piece.texture
                    img = pygame.transform.scale(img, (SQSIZE, SQSIZE))

                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    # drawing the outline of the selected piece
    def draw_outline(self, surface, row, col):
        piece = self.board.squares[row][col].piece
        if piece:
            img = piece.texture
            img = pygame.transform.scale(img, (SQSIZE, SQSIZE))
            mask = pygame.mask.from_surface(img)
            outline = mask.outline()
            outline = [(col * SQSIZE + x, row * SQSIZE + y) for x, y in outline]

            offset = 3
            offset_outline = []
            for x, y in outline:
                if x > col * SQSIZE + SQSIZE // 2:
                    x += offset
                else:
                    x -= offset
                if y > row * SQSIZE + SQSIZE // 2:
                    y += offset
                else:
                    y -= offset
                offset_outline.append((x, y))

            pygame.draw.lines(surface, (200, 200, 0), True, offset_outline, 3)  # Yellow outline with thickness 3

    # displaying possible moves
    def show_possible_moves(self, surface, moves):
        for move in moves:
            row, col = move.final

            outline_rect = (col * SQSIZE + 1, row * SQSIZE + 1, SQSIZE - 3, SQSIZE - 3)
            pygame.draw.rect(surface, (34, 139, 34), outline_rect, 4)
