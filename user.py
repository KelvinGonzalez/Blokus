from enum import Enum
from piece import valid_unit, pieces

class Color(Enum):
    RED = "r"
    GREEN = "g"
    BLUE = "b"
    YELLOW = "y"

class PieceShard:
    def __init__(self, piece_id: int, position: tuple[int]):
        self.piece_id = piece_id
        self.position = position

class PlayerPiece:
    def __init__(self, piece_id: int, shape: list[list[int]]=None):
        if shape is None:
            shape = [list(x) for x in pieces[piece_id].shape]
        self.piece_id = piece_id
        self.shape = shape

    def rotate_90(self):
        self.shape = [[self.shape[len(self.shape) - 1 - j][i] for j in range(len(self.shape))] for i in range(len(self.shape[0]))]
    
    def rotate_neg_90(self):
        self.shape = [[self.shape[j][len(self.shape[0]) - 1 - i] for j in range(len(self.shape))] for i in range(len(self.shape[0]))]

    def flip_horizontal(self):
        self.shape = [row[::-1] for row in self.shape]

    def flip_vertical(self):
        self.shape = self.shape[::-1]

    def split(self, position: tuple[int]) -> list[PieceShard]:
        piece = pieces[self.piece_id]
        shards = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == valid_unit:
                    row = position[0] + i - len(self.shape)//2
                    col = position[1] + j - len(self.shape[0])//2
                    shards.append(PieceShard(self.piece_id, (row, col)))
        return shards

class Player:
    def __init__(self, name: str, color: Color, player_pieces: list[PlayerPiece]=None):
        if player_pieces is None:
            player_pieces = [PlayerPiece(i) for i in range(len(pieces))]
        self.name = name
        self.color = color
        self.pieces = player_pieces
