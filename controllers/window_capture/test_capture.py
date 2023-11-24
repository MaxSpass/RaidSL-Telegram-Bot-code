import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import time
import ctypes
import cv2
import numpy as np


hwnd_target = win32gui.FindWindow(None, 'Raid: Shadow Legends')
# hwnd_target = win32gui.FindWindow(None, 'Slack | proj-goml | Arcware')
# hwnd_target = win32gui.FindWindow(None, 'bot – controllers\…\main.py')

left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
w = right - left
h = bot - top

win32gui.SetForegroundWindow(hwnd_target)
time.sleep(1.0)

hdesktop = win32gui.GetDesktopWindow()
hwndDC = win32gui.GetWindowDC(hdesktop)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hdesktop, hwndDC)

if result == None:
    #PrintWindow Succeeded
    im.save("images/test.png")

# nimg = np.array(im)
# ocvim = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR).copy()
# fnam = "opencv test-cv2.png"
# cv2.imwrite(fnam, ocvim)


# key = cv2.waitKey(1)
# if key == ord('q'):
#     cv2.destroyAllWindows()
#     break
#
# print('Done.')