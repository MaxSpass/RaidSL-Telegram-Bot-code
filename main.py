import pyautogui
from classes.window_mgr import *

GAME_WINDOW = 'Raid: Shadow Legends'


def prepare_window():
    w = WindowMgr()
    w.find_window_wildcard(".*%s*" % GAME_WINDOW)
    w.adjust_window()
    w.set_foreground()

def main():
    pyautogui.FAILSAFE = True

    prepare_window()


if __name__ == "__main__":
    main()