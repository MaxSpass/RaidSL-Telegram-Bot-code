import pyautogui
import time

def report_mouse_position(seconds=10):
    for i in range(0, seconds):
        print(pyautogui.position())
        time.sleep(1)