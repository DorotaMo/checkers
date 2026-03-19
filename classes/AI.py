import copy
import random


class AI:
    def __init__(self, color, mode='random', depth=1):
        self.color = color
        self.mode = mode
        self.depth = depth

    # random move for now
    def return_move(self, board):

        if self.mode == 'random':
            moves = board.all_available_moves(self.color)
            if moves:
                random_move = random.choice(moves)
                return random_move

        elif self.mode == 'recursive_minimax':
            return self.recursive_minimax(board, self.depth, self.color, True)[0]

    # evaluate the board
    def evaluate(self, board):
        score = 0

        winner = board.check_winners(self.color)
        if winner:
            if winner == self.color:
                return float('inf')
            elif winner == 'tie':
                return -100
            else:
                return float('-inf')
        else:
            for row in range(8):
                for col in range(8):
                    square = board.squares[row][col]
                    if square != 0 and square.has_piece():
                        piece = square.piece
                        if piece.name == 'queen':
                            value = 1.5
                        else:
                            value = 1
                        if piece.color == self.color:
                            score += value
                        else:
                            score -= value
            return score

    def recursive_minimax(self, board, depth, color, maximizing, alpha=float('-inf'), beta=float('inf')):
        opposite_color = 'white' if color == 'red' else 'red'

        if depth == 0 or board.check_winners(color):
            score = self.evaluate(board)
            return None, score

        moves = board.all_available_moves(color)

        if maximizing:
            best_score = float('-inf')
            best_moves = []

            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.move_piece(move)

                _, score = self.recursive_minimax(board_copy, depth - 1, opposite_color, False, alpha, beta)

                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

                # Aktualizacja alpha
                alpha = max(alpha, best_score)

                # Przycinanie beta
                if beta <= alpha:
                    break

            best_move = random.choice(best_moves)
            return best_move, best_score

        # Jeśli gracz minimalizujący
        else:
            best_score = float('inf')
            best_moves = []

            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.move_piece(move)

                _, score = self.recursive_minimax(board_copy, depth - 1, opposite_color, True, alpha, beta)

                if score < best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

                # Aktualizacja beta
                beta = min(beta, best_score)

                # Przycinanie alpha
                if beta <= alpha:
                    break

            best_move = random.choice(best_moves)
            return best_move, best_score
