from board import *
from user import *
from piece import *
from state import *
import os

state = State()
page = "board"
page_data = {}
alerts = []

def get_printable_piece(piece: PlayerPiece, color: Color):
    result = []
    for i in range(len(piece.shape)):
        result.append(" ".join([" " if y == 0 else color.value for y in piece.shape[i]]))
    return result

def print_target_piece(piece: PlayerPiece, color: Color):
    result = "      |    \n"
    for i in range(len(piece.shape)):
        result += ("--" if i == 2 else "  ") + " ".join([" " if y == 0 else color.value for y in piece.shape[i]]) + ("--" if i == 2 else "") + "\n"
    result += "      |    "
    print(result)

def parse_position(position_code):
    if len(position_code) != 2:
        return (-1, -1)
    return (ord(position_code[0])-ord("A"), ord(position_code[1])-ord("A"))

def goto(x: int, data: dict=None):
    global page, page_data
    if data is None:
        data = {}
    page = x
    page_data = data

def display_page():
    player = state.players[state.turn % len(state.players)]
    print(f"Turn #{state.turn+1}: {player.name}'s Turn")
    if page == "board":
        state.board.print()
    elif page == "pieces":
        printable_pieces = []
        for i in range(len(player.pieces)):
            piece_num_string = f"Piece #{i}"
            printable_piece = get_printable_piece(player.pieces[i], player.color)
            printable_pieces.append([piece_num_string + " "*(len(printable_piece[0])-len(piece_num_string))] + printable_piece)
        width = 5
        s = ""
        for i in range(0, len(printable_pieces), width):
            for j in range(len(printable_pieces[0])):
                for n in range(width):
                    if i+n < len(printable_pieces):
                        s += printable_pieces[i+n][j] + "  "
                s += "\n"
        print(s)
    elif page == "piece":
        state.board.print()
        print("Piece:")
        print_target_piece(player.pieces[page_data["index"]], player.color)
    elif page == "place_piece":
        state.board.print_mock(player.pieces[page_data["index"]].split(page_data["position"]), player.color)
        print("Confirm piece position? (Y/n) ")

def raise_alert(text: str):
    alerts.append("Alert: " + text)

while True:
    try:
        player = state.players[state.turn % len(state.players)]
        display_page()
        command = input("Enter command: ")

        if command == "board":
            goto("board")
        elif command == "pieces":
            goto("pieces")
        elif command.startswith("piece "):
            index = int(command[len("piece "):])
            if index >= 0 and int(command[len("piece "):]) < len(player.pieces):
                goto("piece", {"index": index})
            else:
                raise_alert("Invalid piece index")
        elif page == "piece" and command.startswith("rotate "):
            for c in command[len("rotate "):]:
                if c == "+":
                    player.pieces[page_data["index"]].rotate_90()
                elif c == "-":
                    player.pieces[page_data["index"]].rotate_neg_90()
        elif page == "piece" and command.startswith("place "):
            if state.board.validate(player.pieces[page_data["index"]].split(parse_position(command[len("piece "):])), player.color):
                goto("place_piece", {"position": parse_position(command[len("piece "):]), "index": page_data["index"]})
            else:
                raise_alert("Piece cannot be placed in that location")
        elif page == "piece" and command.startswith("flip "):
            dir = command[len("flip "):]
            if dir == "horizontal" or dir == "h":
                player.pieces[page_data["index"]].flip_horizontal()
            elif dir == "vertical" or dir == "v":
                player.pieces[page_data["index"]].flip_vertical()
            else:
                raise_alert("Piece cannot be flipped in that direction")
        elif page == "place_piece" and command.upper() == "Y":
            if state.place_piece(player, player.pieces[page_data["index"]], page_data["position"]):
                raise_alert("Piece was placed")
                goto("board")
            else:
                raise_alert("Piece was not placed")
        elif page == "place_piece" and command.lower() == "n":
            goto("piece", {"index": page_data["index"]})
        elif command == "pass":
            state.pass_turn()
            raise_alert("Player has passed")
            goto("board")
        elif command == "exit":
            break
        else:
            raise_alert("Invalid command")

        winner = state.check_win()
        if winner is not None:
            os.system('cls')
            print(f"{winner.name} has won!")
            state.board.print()
            if input("Would you like to play again? (Y/n) ").upper() == "Y":
                state = State()
                page = "board"
                page_data = {}
                alerts = []
            else:
                break
    except:
        raise_alert("Error has occurred")
    os.system('cls')
    if len(alerts) > 0:
        print("\n".join(alerts))
        alerts.clear()
