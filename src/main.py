from app import app
from getkey import getkey
from state import State
import os

clear = "cls" if os.name == "nt" else "clear"
state = State()
app.set_key("state", state)


def any_alerts():
    return app.get_key("alerts") is not None and len(app.get_key("alerts")) > 0


def update_screen():
    os.system(clear)
    alerts = app.get_key("alerts")
    if any_alerts():
        print("\n".join(alerts))
        alerts.clear()
    app.call()


update_screen()
while True:
    key = getkey()
    if key.isdigit():
        app.set_key("num", key)
        key = "num"
    if app.transition(key) or any_alerts():
        winner = state.check_win()
        if winner is not None:
            os.system(clear)
            print(f"{winner.name} has won!")
            state.board.print()
            if input("Would you like to play again? (Y/n) ").upper() == "Y":
                state = State()
                app.reset()
                app.set_key("state", state)
            else:
                break

        update_screen()
