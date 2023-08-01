from enums import *
from board import *
from player import *
from player_piece import *
from piece import *
from state import *
import os
import math

state = State()
page = "start"
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
    if page == "start":
        print("Welcome to Blokus!\n\nPlace your tetrominoes on the board, corner-to-corner, blocking \nyour opponents. Maximize territory to win!\n\nPress enter to start the game.\nType \"help\" after starting to view all commands.\n")
    elif page == "board":
        print(f"Turn #{state.turn+1}: {player.name}'s Turn")
        state.board.print()
    elif page == "pieces":
        print(f"Turn #{state.turn+1}: {player.name}'s Turn")
        printable_pieces = []
        for i in range(len(player.pieces)):
            piece_num_string = f"Piece #{i+1}"
            printable_piece = get_printable_piece(player.pieces[i], player.color)
            printable_pieces.append([piece_num_string + " "*(len(printable_piece[0])-len(piece_num_string))] + printable_piece)
        width = math.ceil(math.sqrt(len(player.pieces)))
        s = ""
        for i in range(0, len(printable_pieces), width):
            for j in range(len(printable_pieces[0])):
                for n in range(width):
                    if i+n < len(printable_pieces):
                        s += printable_pieces[i+n][j] + "  "
                s += "\n"
        print(s)
    elif page == "piece":
        print(f"Turn #{state.turn+1}: {player.name}'s Turn")
        state.board.print()
        print("Piece:")
        print_target_piece(page_data["piece"], player.color)
    elif page == "place_piece":
        print(f"Turn #{state.turn+1}: {player.name}'s Turn")
        state.board.print_mock(page_data["piece"].split(page_data["position"]), player.color)
        print("Confirm piece position? (Y/n) ")
    elif page == "help":
        print("Help:\n"
              " -instructions: Show the game's instructions\n"
              " -board: Show the game board\n"
              " -pieces: Show your current pieces\n"
              " -piece [x]: Focus on a specific piece\n"
              " -rotate [+/-]+: Rotate the focused piece\n"
              " -flip [h/v]: Flip the focused piece\n"
              " -place [RowCol]: Place the focused piece\n"
              " -exit: Exit the game\n")
    elif page == "instructions":
        print("Instructions:\n"
              " 1. Players: Blokus is designed for 2 to 4 players.\n"
              " 2. Board: The game is played on a square grid board with 20x20 cells.\n"
              " 3. Pieces: Each player has a set of differently shaped and colored pieces\n    called \"tetrominoes\" (Tetris-like shapes).\n"
              " 4. Objective: The goal is to strategically place your pieces on the board\n    while blocking your opponents, maximizing your territory.\n"
              " 5. Placing Pieces: Players take turns placing one of their pieces on\n    the board. Pieces must touch their own at a corner but not along edges.\n"
              " 6. Blocking: Pieces cannot touch other players' pieces, except at corners.\n"
              " 7. Passing: If a player cannot legally place a piece, they must pass\n    their turn.\n"
              " 8. End of Game: The game ends when no player can make a legal move.\n"
              " 9. Scoring: Players count occupied cells; the one with the fewest\n    remaining wins.\n")

def raise_alert(text: str):
    alerts.append("Alert: " + text)

while True:
    try:
        player = state.players[state.turn % len(state.players)]
        display_page()
        command = input("Enter command: ")

        if page == "start":
            goto("board")  
        elif command == "board":
            goto("board")
        elif command == "pieces":
            goto("pieces")
        elif command.startswith("piece "):
            index = int(command[len("piece "):]) - 1
            if index >= 0 and index < len(player.pieces):
                goto("piece", {"piece": player.pieces[index]})
            else:
                raise_alert("Invalid piece index")
        elif page == "piece" and command.startswith("rotate "):
            for c in command[len("rotate "):]:
                if c == "+":
                    page_data["piece"].rotate_90()
                elif c == "-":
                    page_data["piece"].rotate_neg_90()
        elif page == "piece" and command.startswith("place "):
            if state.board.validate(page_data["piece"].split(parse_position(command[len("piece "):])), player.color):
                goto("place_piece", {"position": parse_position(command[len("piece "):]), "piece": page_data["piece"]})
            else:
                raise_alert("Piece cannot be placed in that location")
        elif page == "piece" and command.startswith("flip "):
            dir = command[len("flip "):]
            if dir == "horizontal" or dir == "h":
                page_data["piece"].flip_horizontal()
            elif dir == "vertical" or dir == "v":
                page_data["piece"].flip_vertical()
            else:
                raise_alert("Piece cannot be flipped in that direction")
        elif page == "place_piece" and command.upper() == "Y":
            if state.place_piece(player, page_data["piece"], page_data["position"]):
                raise_alert("Piece was placed")
                goto("board")
            else:
                raise_alert("Piece was not placed")
        elif page == "place_piece" and command.lower() == "n":
            goto("piece", {"piece": page_data["piece"]})
        elif command == "pass":
            state.pass_turn()
            raise_alert("Player has passed")
            goto("board")
        elif command == "help":
            goto("help")
        elif command == "instructions":
            goto("instructions")
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
