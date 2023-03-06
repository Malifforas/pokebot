import cv2
import keyboard
import numpy as np
from PIL import ImageGrab
import requests
import json
import time
from config import Config

# Duration of button presses
BUTTON_PRESS_DURATION = 0.2

# Mapping of button names to emulator key codes
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

def press(button):
    """
    Press a button on the emulator.

    :param button: The button to press.
    """
    keyboard.press(BUTTON_MAPPING[button])
    time.sleep(BUTTON_PRESS_DURATION)
    keyboard.release(BUTTON_MAPPING[button])
    time.sleep(BUTTON_PRESS_DURATION)

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2"

    @staticmethod
    def get_pokemon(pokemon_name):
        url = f"{PokeAPI.BASE_URL}/pokemon/{pokemon_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        return None

    @staticmethod
    def get_move(move_name):
        url = f"{PokeAPI.BASE_URL}/move/{move_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        return None

class Screen:
    @staticmethod
    def grab(region):
        return cv2.cvtColor(np.array(ImageGrab.grab(region)), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def load(file_path):
        return cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)


class Button:
    A = 0
    B = 1
    X = 2
    Y = 3
    L = 4
    R = 5
    UP = 6
    DOWN = 7
    LEFT = 8
    RIGHT = 9
    START = 10
    SELECT = 11

    @staticmethod
    def press(button):
        Config.emulator.press_button(button)

    @staticmethod
    def hold(button, hold_time):
        Config.emulator.press_button(button)
        time.sleep(hold_time)
        Config.emulator.release_button(button)

    @staticmethod
    def release(button):
        Config.emulator.release_button(button)


class Target:
    NOSE_LOCK_CENTER = (110, 72)


class State:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h


class PlayerRole:
    OPPONENT = "opponent"
    PLAYER = "player"
