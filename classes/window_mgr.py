import win32gui
import re


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        # win32gui.EnumWindows(self._window_enum_callback, 'Raid: Shadow Legends')
        # win32gui.EnumWindows(self._window_enum_callback, 'Plarium Play')
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def adjust_window(self, x=0, y=0):
        """Windows 10 has an invisible border of 7 pixels"""
        win32gui.MoveWindow(self._handle, x - 7, y, 920, 540, True)

    def get_rect(self):
        return win32gui.GetWindowRect(self._handle)