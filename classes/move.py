class Move:
    def __init__(self, initial, final, attacked_piece=None):
        self.initial = initial
        self.final = final
        self.attacked_piece = attacked_piece
