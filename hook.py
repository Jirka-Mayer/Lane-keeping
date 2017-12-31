"""
    Fixing a bug on windows with key character

    + allowing multiple listeners
"""

from pykeyboard import PyKeyboardEvent
from pymouse import PyMouseEvent
import platform

SYSTEM = platform.system()

CHARACTER_MAP = {
    27: "escape",

    65: "a",
    68: "d",
    69: "e",
    81: "q",
    83: "s",
    87: "w",
    88: "x",

    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
}

# there should only be one instance
class KeyboardHook(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)

        # list of listener functions
        self.tapListeners = []

    # overwrite default _tap method on windows
    def _tap(self, event):
        if SYSTEM == "Windows":
            keycode = event.KeyID
            press_bool = (event.Message in [self.hc.WM_KEYDOWN, self.hc.WM_SYSKEYDOWN])
        
            if keycode in CHARACTER_MAP:
                character = CHARACTER_MAP[keycode]
            else:
                character = "Unknown character, keycode: " + str(keycode)

            self.tap(keycode, character, press_bool)
        else:
            PyKeyboardEvent._tap(self, event)

    def tap(self, keycode, character, press):
        for listener in self.tapListeners:
            listener(keycode, character, press)

    # bonus - disable default escape action
    def escape(self, event):
        pass

    def addTapListener(self, listener):
        self.tapListeners.append(listener)


# there should only be one instance
class MouseHook(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

        # list of listener functions
        self.moveListeners = []

    def move(self, x, y):
        for listener in self.moveListeners:
            listener(x, y)

    def addMoveListener(self, listener):
        self.moveListeners.append(listener)
