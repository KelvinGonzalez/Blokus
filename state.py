from board import Board, GridItem
from enums import Color
from player import Player
from player_piece import PlayerPiece, PieceShard
from piece import pieces, valid_unit

class Move:
    def __init__(self, owner_color: Color, piece_shards: list[PieceShard]):
        self.owner_color = owner_color
        self.piece_shards = piece_shards

class State:
    def __init__(self, board: Board=None, players: list[Player]=None, moves: list[Move]=None, turn: int=0, pass_counter: int=0):
        if board is None:
            board = Board()
        if players is None:
            colors = [c for c in Color]
            players = [Player(f"Player {i+1}", colors[i]) for i in range(len(colors))]
        if moves is None:
            moves = []
        self.board = board
        self.players = players
        self.moves = moves
        self.turn = turn
        self.pass_counter = pass_counter

    def place_piece(self, player: Player, player_piece: PlayerPiece, position: tuple[int]) -> bool:
        if player != self.players[self.turn % len(self.players)]:
            return False
        if player_piece not in player.pieces:
            return False
        shards = player_piece.split(position)
        if not self.board.validate(shards, player.color):
            return False
        
        for shard in shards:
            i, j = shard.position[0], shard.position[1]
            self.board.grid_items[i][j] = GridItem(shard.piece_id, player.color)
        self.moves.append(Move(player.color, shards))
        player.pieces.remove(player_piece)
        self.turn += 1
        self.pass_counter = 0
        return True
    
    def pass_turn(self):
        self.turn += 1
        self.pass_counter += 1

    def check_win(self) -> Player:
        unit_count = [0 for x in self.players]
        for i in range(len(self.players)):
            player = self.players[i]
            if len(player.pieces) == 0:
                return player
            for piece in player.pieces:
                for row in pieces[piece.piece_id].shape:
                    for unit in row:
                        if unit == valid_unit:
                            unit_count[i] += 1
        if self.pass_counter < len(self.players):
            return None
        return self.players[min(range(len(unit_count)), key=unit_count.__getitem__)]
