import pyautogui, sys
import time
import os
from helpers.screen import *
from constants.index import *

DEBUG = True

def debug_position():
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


# debug_position()
# exit()

# pyautogui.getWindow(GAME_WINDOW)

needles_folder_path = os.path.join('images', 'needles')
needles_avatars_folder_path = os.path.join('images', 'avatars')


prepare_window()
time.sleep(1)
# quests_coordinates = [256, 494]
# pyautogui.moveTo(quests_coordinates)


exit()

# needle = os.path.join(needles_folder_path, 'shop.jpg')
# needle = os.path.join(needles_folder_path, 'quests.jpg')
needle = os.path.join(needles_avatars_folder_path, 'Lydia_the_Deathsiren.png')
target = pyautogui.locateOnScreen(needle, grayscale=True, confidence=0.25)
print(target)

if target:
    pyautogui.click(target)


# im1 = pyautogui.screenshot()
# im1.save('test.jpg')

# pyautogui.click(x=quests_coordinates[0], y=quests_coordinates[1])

