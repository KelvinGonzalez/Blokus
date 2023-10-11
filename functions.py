from player_piece import PlayerPiece
from enums import Color
from board import Board
import math

character_limit = 48


def character_limiter(x, limit, append=""):
  count = 0
  i = 0
  while i < len(x):
    count += 1
    if count > limit:
      if x[i] == " ":
        x = x[:i] + "\n" + append + x[i + 1:]
        count = len(append)
        i += count
    if x[i] == "\n":
      count = 0
    i += 1
  return x


def get_printable_piece(piece: PlayerPiece, color: Color, valid: bool):
  result = []
  for i in range(len(piece.shape)):
    result.append(" ".join([
      " " if y == 0 else color.value if valid else "X" for y in piece.shape[i]
    ]))
  return result


def raise_alert(alert, data):
  if data.get("alerts") is None:
    data["alerts"] = [alert]
    return
  data["alerts"].append(alert)


def start(data):
  print(
    character_limiter(
      "Welcome to Blokus!\n\nPlace your tetrominoes on the board, corner-to-corner, blocking your opponents. Maximize territory to win!\n\nPress enter to start the game.",
      character_limit))


def board(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  print(f"Turn #{state.turn+1}: {player.name}'s Turn")
  state.board.print()


def pieces(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  print(f"Turn #{state.turn+1}: {player.name}'s Turn")
  printable_pieces = []
  for i in range(len(player.pieces)):
    piece_num_string = f"Piece #{i+1}"
    printable_piece = get_printable_piece(player.pieces[i], player.color,
                                          data["valid_moves"][i])
    piece_num_string += " " * (len(printable_piece[0]) - len(piece_num_string))
    printable_pieces.append([piece_num_string] + printable_piece)
  width = math.ceil(math.sqrt(len(player.pieces)))
  s = ""
  for i in range(0, len(printable_pieces), width):
    for n in range(width):
      s += (("+" + "-" * len(printable_pieces[0][0]) +
             "+") if i + n == data['index'] or i + n == data['index'] + width
            else " " * (len(printable_pieces[0][0]) + 2))
    s += "\n"
    for j in range(len(printable_pieces[0])):
      for n in range(width):
        if i + n < len(printable_pieces):
          separator = ("|" if i + n == data['index'] else " ")
          s += separator + printable_pieces[i + n][j] + separator
      s += "\n"
    if i < len(printable_pieces) <= i + width:
      for n in range(width):
        s += (("+" + "-" * len(printable_pieces[0][0]) + "+") if i +
              n == data['index'] else " " * (len(printable_pieces[0][0]) + 2))
      s += "\n"
  print(s)
  if data["num_buffer"] != "":
    print(f"Selecting... {data['num_buffer']}")


def piece(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  print(f"Turn #{state.turn+1}: {player.name}'s Turn")
  state.board.print_mock(piece.split(data["position"]), player.color)


def start_enter(data):
  data["index"] = 0
  data["num_buffer"] = ""
  data["valid_moves"] = [True] * 13 + [False] + [True] * 7


def pieces_up(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  width = math.ceil(math.sqrt(len(player.pieces)))
  if data.get("index") > width:
    data["index"] -= width
  else:
    data["index"] = 0


def pieces_down(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  width = math.ceil(math.sqrt(len(player.pieces)))
  if data.get("index") < len(player.pieces) - width:
    data["index"] += width
  else:
    data["index"] = len(player.pieces) - 1
  data["num_buffer"] = ""


def pieces_left(data):
  if data.get("index") > 0:
    data["index"] -= 1
  else:
    data["index"] = 0
  data["num_buffer"] = ""


def pieces_right(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  if data.get("index") < len(player.pieces) - 1:
    data["index"] += 1
  else:
    data["index"] = len(player.pieces) - 1
  data["num_buffer"] = ""


def pieces_num(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  buffer = int(data["num_buffer"] + data["num"])
  if 0 < buffer <= len(player.pieces):
    data["num_buffer"] += data["num"]
    data["index"] = buffer - 1


def pieces_back(data):
  if data["num_buffer"] != "":
    data["num_buffer"] = data["num_buffer"][:-1]
    if data["num_buffer"] != "":
      data["index"] = int(data["num_buffer"]) - 1


def pieces_enter_condition(data):
  condition = data["valid_moves"][data["index"]]
  if not condition:
    raise_alert("No valid moves for this piece", data)
  return condition


def pieces_enter(data):
  data["position"] = (Board.grid_size // 2, Board.grid_size // 2)


def pieces_board(data):
  pass


def board_pieces(data):
  pass


def piece_up(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  i, j = data["position"]
  if not state.board.out_of_bounds(piece.split((i - 1, j))):
    data["position"] = (i - 1, j)


def piece_down(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  i, j = data["position"]
  if not state.board.out_of_bounds(piece.split((i + 1, j))):
    data["position"] = (i + 1, j)


def piece_left(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  i, j = data["position"]
  if not state.board.out_of_bounds(piece.split((i, j - 1))):
    data["position"] = (i, j - 1)


def piece_right(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  i, j = data["position"]
  if not state.board.out_of_bounds(piece.split((i, j + 1))):
    data["position"] = (i, j + 1)


def piece_num(data):
  if data["num"] == "0":
    piece_center(data)
  elif data["num"] in ["1", "2", "3", "4"]:
    positions = [(Board.grid_size // 4, Board.grid_size // 4),
                 (Board.grid_size // 4, Board.grid_size * 3 // 4),
                 (Board.grid_size * 3 // 4, Board.grid_size // 4),
                 (Board.grid_size * 3 // 4, Board.grid_size * 3 // 4)]
    data["position"] = positions[int(data["num"]) - 1]


def piece_center(data):
  data["position"] = (Board.grid_size // 2, Board.grid_size // 2)


def piece_rotate(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  piece.rotate_90()
  offset = state.board.out_of_bounds_offset(piece.split(data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_neg_rotate(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  piece.rotate_neg_90()
  offset = state.board.out_of_bounds_offset(piece.split(data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_horizontal_flip(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  piece.flip_horizontal()
  offset = state.board.out_of_bounds_offset(piece.split(data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_vertical_flip(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  piece.flip_vertical()
  offset = state.board.out_of_bounds_offset(piece.split(data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_left_swap(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  while True:
    if data["index"] > 0:
      data["index"] -= 1
    else:
      data["index"] = len(player.pieces) - 1
    if data["valid_moves"][data["index"]]:
      break
  offset = state.board.out_of_bounds_offset(player.pieces[data["index"]].split(
    data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_right_swap(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  while True:
    if data["index"] < len(player.pieces) - 1:
      data["index"] += 1
    else:
      data["index"] = 0
    if data["valid_moves"][data["index"]]:
      break
  offset = state.board.out_of_bounds_offset(player.pieces[data["index"]].split(
    data["position"]))
  data["position"] = (data["position"][0] - offset[0],
                      data["position"][1] - offset[1])


def piece_enter_condition(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  condition = state.board.validate(piece.split(data["position"]), player.color)
  if not condition:
    raise_alert("Piece is in an invalid position", data)
  return condition


def piece_enter(data):
  state = data["state"]
  player = state.players[state.turn % len(state.players)]
  piece = player.pieces[data["index"]]
  state.place_piece(player, piece, data["position"])
  data["index"] = 0
  data["num_buffer"] = ""
  for x in range(len(state.players)):
    player = state.players[state.turn % len(state.players)]
    data["valid_moves"] = state.board.any_valid_move(player)
    if any(data["valid_moves"]):
      break
    state.pass_turn()
    raise_alert(f"{player.name} has no valid moves", data)


def piece_pieces(data):
  data["num_buffer"] = ""
