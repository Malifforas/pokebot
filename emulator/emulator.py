import keyboard
import time

# Key codes for the emulator's default keybinds
BUTTON_MAPPING = {
    "up": "up_arrow",
    "down": "down_arrow",
    "left": "left_arrow",
    "right": "right_arrow",
    "a": "z",
    "b": "x",
    "x": "a",
    "y": "s",
    "l": "q",
    "r": "w",
    "start": "return",
    "select": "backspace",
}

# Duration of button presses
BUTTON_PRESS_DURATION = 0.2


def press(button):
    """
    Press a button on the emulator.

    :param button: The button to press.
    """
    keyboard.press(BUTTON_MAPPING[button])
    time.sleep(BUTTON_PRESS_DURATION)
    keyboard.release(BUTTON_MAPPING[button])
    time.sleep(BUTTON_PRESS_DURATION)