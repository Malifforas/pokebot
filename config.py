import os

class Config:
    ROM_PATH = os.path.join(os.path.dirname(__file__), '..', 'roms', 'Pokemon - HeartGold Version (USA).nds')
    EMULATOR_PATH = os.path.join(os.path.dirname(__file__), '..', 'DeSmuME_0.9.13_x64.exe')

    # Key bindings
    A_BUTTON = 'z'
    B_BUTTON = 'x'
    UP_BUTTON = 'up'
    DOWN_BUTTON = 'down'
    LEFT_BUTTON = 'left'
    RIGHT_BUTTON = 'right'
    START_BUTTON = 'a'
    SELECT_BUTTON = 's'