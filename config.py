import os

class Config:
    ROM_PATH = "C:/Users/Blizzard/Desktop/Pokemon AI/roms/Pokemon - HeartGold Version (USA).nds"
    EMULATOR_PATH = "C:/Users/Blizzard/Desktop/Pokemon AI/DeSmuME_0.9.13_x64.exe"

    # Key bindings
    A_BUTTON = 'z'
    B_BUTTON = 'x'
    UP_BUTTON = 'up'
    DOWN_BUTTON = 'down'
    LEFT_BUTTON = 'left'
    RIGHT_BUTTON = 'right'
    START_BUTTON = 'a'
    SELECT_BUTTON = 's'

def config():
    path = "C:/Users/Blizzard/Desktop/Pokemon AI/"
    emulator_path = path + "DeSmuME_0.9.13_x64.exe"
    rom_path = path + "Pokemon - HeartGold Version (USA).nds"
    return emulator_path, rom_path