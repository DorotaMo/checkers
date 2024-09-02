import random


class AI:
    def __init__(self, color):
        self.color = color

    # random move for now
    def return_move(self, board):
        moves = board.all_available_moves(self.color)
        if moves:
            random_move = random.choice(moves)

            return random_move
