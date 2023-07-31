from user import Color, PieceShard

class GridItem:
    def __init__(self, piece_id: int, owner_color: Color):
        self.piece_id = piece_id
        self.owner_color = owner_color

class Board:
    def __init__(self, grid_items: list[list[GridItem]]=None):
        if grid_items is None:
            n = 20
            grid_items = [[None for j in range(n)] for i in range(n)]
        self.grid_items = grid_items

    def print(self):
        result = ""
        for i in range(len(self.grid_items)):
            result += chr(ord("A") + i) + " | " + " ".join(["." if y is None else y.owner_color.value for y in self.grid_items[i]]) + "\n"
        result += "--+" + "--" * len(self.grid_items[0]) + "\n"
        result += "  | " + " ".join([chr(ord("A") + i) for i in range(len(self.grid_items[0]))])
        print(result)

    def print_mock(self, piece_shards: list[PieceShard], color: Color):
        mock = [[None if y is None else GridItem(y.piece_id, y.owner_color) for y in x] for x in self.grid_items]
        for shard in piece_shards:
            i, j = shard.position[0], shard.position[1]
            mock[i][j] = GridItem(shard.piece_id, color)
        
        result = ""
        for i in range(len(mock)):
            result += chr(ord("A") + i) + " | " + " ".join(["." if y is None else y.owner_color.value for y in mock[i]]) + "\n"
        result += "--+" + "--" * len(mock[0]) + "\n"
        result += "  | " + " ".join([chr(ord("A") + i) for i in range(len(mock[0]))])
        print(result)

    def validate(self, piece_shards: list[PieceShard], color: Color) -> bool:
        def position_out_of_bounds(i: int, j: int) -> bool:
            return i < 0 or j < 0 or i >= len(self.grid_items) or j >= len(self.grid_items[0])
        def first_move(color: Color) -> bool:
            for row in self.grid_items:
                for grid_item in row:
                    if grid_item is not None and grid_item.owner_color == color:
                        return False
            return True
        
        is_first_move = first_move(color)
        touches_corner = False
        is_corner = False
        touches_side = False
        out_of_bounds = False
        intersects = False

        for shard in piece_shards:
            i, j = shard.position[0], shard.position[1]
            if position_out_of_bounds(i, j):
                out_of_bounds = True
                break
            if self.grid_items[i][j] is not None:
                intersects = True
                break
            if is_first_move and (i == 0 and j == 0 or i == 0 and j == len(self.grid_items[0])-1 or i == len(self.grid_items)-1 and j == 0 or i == len(self.grid_items)-1 and j == len(self.grid_items[0])-1):
                is_corner = True
            if not is_first_move and (not position_out_of_bounds(i+1, j) and self.grid_items[i+1][j] is not None and self.grid_items[i+1][j].owner_color == color or not position_out_of_bounds(i-1, j) and self.grid_items[i-1][j] is not None and self.grid_items[i-1][j].owner_color == color or not position_out_of_bounds(i, j+1) and self.grid_items[i][j+1] is not None and self.grid_items[i][j+1].owner_color == color or not position_out_of_bounds(i, j-1) and self.grid_items[i][j-1] is not None and self.grid_items[i][j-1].owner_color == color):
                touches_side = True
                break
            if not is_first_move and (not position_out_of_bounds(i+1, j+1) and self.grid_items[i+1][j+1] is not None and self.grid_items[i+1][j+1].owner_color == color or not position_out_of_bounds(i+1, j-1) and self.grid_items[i+1][j-1] is not None and self.grid_items[i+1][j-1].owner_color == color or not position_out_of_bounds(i-1, j+1) and self.grid_items[i-1][j+1] is not None and self.grid_items[i-1][j+1].owner_color == color or not position_out_of_bounds(i-1, j-1) and self.grid_items[i-1][j-1] is not None and self.grid_items[i-1][j-1].owner_color == color):
                touches_corner = True

        return (is_first_move and is_corner or not is_first_move and touches_corner and not touches_side) and not out_of_bounds and not intersects