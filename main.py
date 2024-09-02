import pygame
import time

from classes.AI import AI
from classes.board import is_valid_move, find_move
from classes.const import *
from classes.game import Game


class Main:

    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.game = Game()
        self.AI = AI("red")

    def mainloop(self):

        board = self.game.board
        selected_piece_cord = None
        selected_piece = None
        turn = 'white'

        while True:
            self.game.show_bg(self.main_screen)
            self.game.show_pieces(self.main_screen)

            board.check_winners(turn)

            # if the piece is selected, draw the outline and show possible moves
            if selected_piece:
                self.game.draw_outline(self.main_screen, selected_piece_cord[0], selected_piece_cord[1])
                piece_moves = find_move(selected_piece_cord, board.all_available_moves(turn))
                self.game.show_possible_moves(self.main_screen, piece_moves)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN and turn == 'white':
                    m_x, m_y = pygame.mouse.get_pos()
                    clicked_row = m_y // SQSIZE
                    clicked_col = m_x // SQSIZE
                    if clicked_col < 8:
                        square = board.squares[clicked_row][clicked_col]
                        all_valid_moves = board.all_available_moves(turn)

                        # if the piece is selected and clicked on a valid move destination, move the piece
                        if selected_piece and is_valid_move(selected_piece_cord, (clicked_row, clicked_col),
                                                            all_valid_moves):

                            move = find_move(selected_piece_cord, all_valid_moves, (clicked_row, clicked_col))
                            board.move_piece(move)
                            turn = 'white' if turn == 'red' else 'red'
                            selected_piece = None

                        # if clicked on piece of the same color, select the piece
                        elif square != 0 and square.has_piece() and square.piece.color == turn:
                            selected_piece_cord = (clicked_row, clicked_col)
                            selected_piece = square.piece

                        # deselect the piece
                        else:
                            selected_piece = None

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # AI move
                elif turn == 'red':
                    random_move = self.AI.return_move(board)
                    board.move_piece(random_move)
                    turn = 'white' if turn == 'red' else 'red'
                    time.sleep(0.4)

            pygame.display.update()


main = Main()
main.mainloop()
