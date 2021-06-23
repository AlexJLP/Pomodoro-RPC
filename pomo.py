import time
from datetime import datetime
from typing import Callable

import art
import blessed
from blessed.formatters import FormattingString
from pypresence import Presence

term = blessed.Terminal()

client_id = ""  # Enter Application ID here. Create at https://discord.com/developers/applications
RPC = Presence(client_id=client_id)
RPC.connect()

# Globals
c = term.white
large_i = "pfp_study"  # Image (large) shown in profile
st = "Focusing"  # Text when hovering image


def discord_status(text):
    """Sets the discord status on established  RPC connection.

    Args:
        text: Text to set as status.
    """
    RPC.update(state=text, large_image=large_i, large_text=st,
               start=int(datetime.timestamp(datetime.now().replace())))


def write_time(t):
    """Write time on terminal as ascii art, overwriting previous text.

    Args:
        t: Time string.
    """
    t_art = art.text2art(t, font="starwars")
    print(term.home + term.move_down(1) + c + term.clear_eos + t_art + term.white)


def timer(minutes):
    """Countdown timer for minutes minutes

    Args:
        minutes: minutes to time.
    """
    countdown = minutes * 60
    while countdown >= 0:
        mins, secs = divmod(countdown, 60)
        time_f = '{:02d}:{:02d}'.format(mins, secs)
        write_time(time_f)
        time.sleep(1)
        countdown -= 1


def pomo_timer(minutes: int, title: str, colour: FormattingString) -> Callable[[], None]:
    """Create a tier function for the given args.

    Args:
        minutes: Minutes for the timer
        title: Title (displayed in both terminal and Discord Rich Presence)
        colour: Colour string https://blessed.readthedocs.io/en/latest/colors.html

    Returns:
        A function that will run a countdown timer with the set parameters.
    """
    def parameterised_timer():
        discord_status(f"{title}, {minutes}minutes...")
        print(term.home + term.clear + f"Currently in a {title} ({minutes}m)")
        global c
        c = colour
        timer(minutes)

    return parameterised_timer


# - Main Menu -
def quit_fn():
    RPC.close()
    raise SystemExit


menu = {
    "1": ("Pomodoro", pomo_timer(25, "Pomodoro", term.tomato)),
    "2": ("Short Break", pomo_timer(5, "Short Break", term.green3)),
    "3": ("Long Break", pomo_timer(15, "Long Break", term.green3)),
    "4": ("Quit", quit_fn)
}


def main_menu():
    for key in sorted(menu.keys()):
        print(key + ":" + menu[key][0])
    ans = input("Select Option: ")
    menu.get(ans, [None, lambda: print("INVALID CHOICE!")])[1]()


while True:
    main_menu()
