import time
import pyautogui
from classes.window_mgr import *
from debug.functions import *
from recorder.playback import play

GAME_WINDOW = 'Raid: Shadow Legends'


def prepare_window():
    w = WindowMgr()
    w.find_window_wildcard(".*%s*" % GAME_WINDOW)
    w.adjust_window()
    w.set_foreground()

def main():
    pyautogui.FAILSAFE = True

    prepare_window()

    # report_mouse_position()

    # time.sleep(1)
    # play('actions_test_01.json')

if __name__ == "__main__":
    main()