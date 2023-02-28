from config import Config
from pokebot.emulator import Emulator
from game_state import GameState
from button import Button
from target import Target
from typing import List, Callable
import time

# Global Variables
SCREEN_REGION = (0, 0, 256, 192)
RUN_BUTTON_REGION = (178, 168, 32, 24)
BUTTON_THRESHOLD = 0.8


def wait_for(func: Callable[[], bool], timeout: int = 5000, interval: int = 100) -> bool:
    """
    Wait for function to return True for up to `timeout` milliseconds.

    :param func: A function that returns a boolean value.
    :param timeout: Maximum time to wait in milliseconds.
    :param interval: Polling interval in milliseconds.
    :return: True if function returns True before timeout, False otherwise.
    """
    elapsed_time = 0
    while elapsed_time < timeout:
        if func():
            return True
        time.sleep(interval / 1000)
        elapsed_time += interval
    return False


__all__ = [
    'Config',
    'Emulator',
    'GameState',
    'Button',
    'Target',
    'List',
    'Callable',
    'wait_for',
    'SCREEN_REGION',
    'RUN_BUTTON_REGION',
    'BUTTON_THRESHOLD'
]