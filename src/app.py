from state_manager import App, State, Transition
from functions import *
from getkey import keys

app = App()

start = app.add_state(State(start))
pieces = app.add_state(State(pieces))
board = app.add_state(State(board))
piece = app.add_state(State(piece))

app.add_transition(start, Transition(keys.ENTER, pieces, start_enter))

app.add_transition(pieces, Transition("w", pieces, pieces_up))
app.add_transition(pieces, Transition("s", pieces, pieces_down))
app.add_transition(pieces, Transition("a", pieces, pieces_left))
app.add_transition(pieces, Transition("d", pieces, pieces_right))
app.add_transition(pieces, Transition("num", pieces, pieces_num))
app.add_transition(
    pieces,
    Transition(keys.ENTER, piece, pieces_enter, condition=pieces_enter_condition),
)
app.add_transition(pieces, Transition(keys.BACKSPACE, pieces, pieces_back))
app.add_transition(pieces, Transition("b", board, pieces_board))

app.add_transition(board, Transition("b", pieces, board_pieces))

app.add_transition(piece, Transition("w", piece, piece_up))
app.add_transition(piece, Transition("s", piece, piece_down))
app.add_transition(piece, Transition("a", piece, piece_left))
app.add_transition(piece, Transition("d", piece, piece_right))
app.add_transition(piece, Transition("num", piece, piece_num))
app.add_transition(piece, Transition("e", piece, piece_rotate))
app.add_transition(piece, Transition("q", piece, piece_neg_rotate))
app.add_transition(piece, Transition("x", piece, piece_horizontal_flip))
app.add_transition(piece, Transition("z", piece, piece_vertical_flip))
app.add_transition(piece, Transition(keys.LEFT, piece, piece_left_swap))
app.add_transition(piece, Transition(keys.RIGHT, piece, piece_right_swap))
app.add_transition(
    piece, Transition(keys.ENTER, pieces, piece_enter, condition=piece_enter_condition)
)
app.add_transition(piece, Transition("p", pieces, piece_pieces))
