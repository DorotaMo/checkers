class Move:
    def __init__(self, initial, final, attacked_pieces=None):
        self.initial = initial
        self.final = final
        self.attacked_pieces = attacked_pieces
