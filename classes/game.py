import time

from classes.AI import AI
from classes.board import Board
from classes.board import is_valid_move, find_move
from classes.button import Button
from classes.const import *

dict_of_images = {'white_pawn': '', 'white_queen': '', 'red_pawn': '', 'red_queen': ''}
for key in dict_of_images:
    dict_of_images[key] = pygame.image.load('images/' + key + '.png')

big_custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 50)
custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
small_custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)


class Game:
    def __init__(self, screen, font, game_mode="player", depth=3):
        self.screen = screen
        self.font = font
        self.game_mode = game_mode
        self.depth = depth

        # Calculate offset to center the board on screen
        screen_w, screen_h = screen.get_size()
        self.offset_x = (screen_w - WIDTH) // 2
        self.offset_y = (screen_h - HEIGHT) // 2

        # Initialize game elements
        self.board = Board()
        self.selected_piece = None
        self.selected_piece_cord = None
        self.turn = 'white'

        self.return_button = Button((self.offset_x + 605, self.offset_y + 50), 137, 43, 'Menu', font)

        if self.game_mode == "ai":
            if depth == 0:
                self.AI = AI("red", mode='random')
            else:
                self.AI = AI("red", mode='recursive_minimax', depth=self.depth)

        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound('sounds/piece_move.mp3')
        self.end_sound = pygame.mixer.Sound('sounds/game_end.wav')

    def end_screen(self, winner):
        # Play sound
        self.end_sound.play()

        message1 = winner
        message2 = "Wanna"
        message3 = "play again?"

        # Messages
        text1 = big_custom_font.render(message1, True, (255, 255, 255))
        text2 = custom_font.render(message2, True, (255, 255, 255))
        text3 = custom_font.render(message3, True, (255, 255, 255))
        cx = self.offset_x + WIDTH // 2
        text_rect1 = text1.get_rect(center=(cx, self.offset_y + 120))
        text_rect2 = text2.get_rect(center=(cx, self.offset_y + 230))
        text_rect3 = text3.get_rect(center=(cx, self.offset_y + 290))

        buttons = [
            Button((self.offset_x + 180, self.offset_y + 350), 170, 80, 'YES', big_custom_font, hover_color=(0, 255, 0)),
            Button((self.offset_x + 420, self.offset_y + 350), 170, 80, 'NO', big_custom_font, hover_color=(255, 0, 0)),
        ]

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.screen.blit(text3, text_rect3)

            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.draw(self.screen, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_clicked(mouse_pos):
                        return
                    elif buttons[1].is_clicked(mouse_pos):
                        if self.are_you_sure():
                            pygame.quit()
                            quit()

            pygame.display.flip()

    def show_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col] != 0 and self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img = dict_of_images[piece.color + '_' + piece.name]
                    img = pygame.transform.scale(img, (SQSIZE, SQSIZE))
                    img_center = self.offset_x + col * SQSIZE + SQSIZE // 2, self.offset_y + row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    self.screen.blit(img, piece.texture_rect)

    def draw_outline(self, row, col):
        piece = self.board.squares[row][col].piece
        if piece:
            img = dict_of_images[piece.color + '_' + piece.name]
            img = pygame.transform.scale(img, (SQSIZE, SQSIZE))
            mask = pygame.mask.from_surface(img)
            outline = mask.outline()
            outline = [(self.offset_x + col * SQSIZE + x, self.offset_y + row * SQSIZE + y) for x, y in outline]

            offset = 3
            offset_outline = []
            for x, y in outline:
                if x > self.offset_x + col * SQSIZE + SQSIZE // 2:
                    x += offset
                else:
                    x -= offset
                if y > self.offset_y + row * SQSIZE + SQSIZE // 2:
                    y += offset
                else:
                    y -= offset
                offset_outline.append((x, y))

            pygame.draw.lines(self.screen, (200, 200, 0), True, offset_outline, 3)

    def show_possible_moves(self, moves):
        for move in moves:
            row, col = move.final
            outline_rect = (self.offset_x + col * SQSIZE + 1, self.offset_y + row * SQSIZE + 1, SQSIZE - 3, SQSIZE - 3)
            pygame.draw.rect(self.screen, (34, 139, 34), outline_rect, 4)

    def show_bg(self):
        self.screen.fill((0, 0, 0))
        for row in range(ROWS):
            for col in range(COLS):
                color = (201, 156, 119) if (row + col) % 2 == 0 else (91, 60, 17)
                pygame.draw.rect(self.screen, color, (self.offset_x + col * SQSIZE, self.offset_y + row * SQSIZE, SQSIZE, SQSIZE))

        self.return_button.draw(self.screen, pygame.mouse.get_pos())

    def are_you_sure(self):
        message1 = "Are you sure"
        message2 = "you want to exit?"

        text1 = big_custom_font.render(message1, True, (255, 255, 255))
        text2 = custom_font.render(message2, True, (255, 255, 255))
        cx = self.offset_x + WIDTH // 2
        text_rect1 = text1.get_rect(center=(cx, self.offset_y + 140))
        text_rect2 = text2.get_rect(center=(cx, self.offset_y + 200))

        buttons = [
            Button((self.offset_x + 180, self.offset_y + 350), 170, 80, 'YES', big_custom_font, hover_color=(0, 255, 0)),
            Button((self.offset_x + 420, self.offset_y + 350), 170, 80, 'NO', big_custom_font, hover_color=(255, 0, 0)),
        ]

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)

            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.draw(self.screen, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_clicked(mouse_pos):
                        return True
                    elif buttons[1].is_clicked(mouse_pos):
                        return False

            pygame.display.flip()

    def draw_game(self):
        self.show_bg()
        self.show_pieces()
        if self.selected_piece:
            self.draw_outline(self.selected_piece_cord[0], self.selected_piece_cord[1])
            moves = find_move(self.selected_piece_cord, self.board.all_available_moves(self.turn))
            self.show_possible_moves(moves)

    def ai_action(self):
        if self.game_mode == "ai" and self.turn == 'red':  # AI's turn
            move = self.AI.return_move(self.board)
            time.sleep(1.0)
            self.board.move_piece(move)
            self.move_sound.play()
            self.turn = 'white'

    def player_action(self, pos):
        m_x, m_y = pos
        clicked_row = (m_y - self.offset_y) // SQSIZE
        clicked_col = (m_x - self.offset_x) // SQSIZE

        if clicked_col < 8:
            square = self.board.squares[clicked_row][clicked_col]
            all_valid_moves = self.board.all_available_moves(self.turn)

            if self.selected_piece and is_valid_move(self.selected_piece_cord, (clicked_row, clicked_col),
                                                     all_valid_moves):
                self.move_sound.play()
                move = find_move(self.selected_piece_cord, all_valid_moves, (clicked_row, clicked_col))
                self.board.move_piece(move)

                # Switch turns
                self.turn = 'red' if self.turn == 'white' else 'white'
                self.selected_piece = None

            elif square != 0 and square.has_piece() and square.piece.color == self.turn:
                self.selected_piece_cord = (clicked_row, clicked_col)
                self.selected_piece = square.piece

            else:
                self.selected_piece = None

    def game_loop(self):
        while True:
            if self.board.check_winners(self.turn):
                result = self.board.check_winners(self.turn)
                if result == 'tie':
                    self.end_screen("It's a tie!")
                else:
                    self.end_screen(result + " wins!")
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the return button is clicked
                    if self.return_button.is_clicked(mouse_pos):
                        if self.are_you_sure():
                            return

                    self.player_action(pygame.mouse.get_pos())
                    self.draw_game()
                    pygame.display.update()

            if self.board.check_winners(self.turn):
                result = self.board.check_winners(self.turn)
                if result == 'tie':
                    self.end_screen("It's a tie!")
                else:
                    self.end_screen(result + " wins!")
                return

            self.ai_action()
            self.draw_game()
            pygame.display.update()
