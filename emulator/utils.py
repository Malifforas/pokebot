import numpy as np
from .emulator import Emulator

def load_rom(emulator: Emulator, rom_path: str) -> None:
    with open(rom_path, "rb") as f:
        rom = f.read()
    emulator.load_rom(rom)

def reset_emulator(emulator: Emulator) -> None:
    emulator.press_button("POWER")
    emulator.press_button("A")
    emulator.press_button("START")
    emulator.press_button("A")
    emulator.press_button("A")
    emulator.press_button("A")
    emulator.press_button("A")
    emulator.press_button("A")
    emulator.press_button("A")

def get_game_state(emulator: Emulator) -> np.ndarray:
    state = emulator.get_screen()
    state = np.array(state)
    state = np.transpose(state, (1, 0, 2))
    state = state / 255.0
    return state

def get_action_space() -> list:
    return ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "START", "SELECT"]

def get_reward(prev_state: np.ndarray, curr_state: np.ndarray, action: str) -> float:
    prev_score = np.mean(prev_state)
    curr_score = np.mean(curr_state)
    if action in ["UP", "DOWN", "LEFT", "RIGHT"]:
        reward = -0.01
    elif action == "A":
        reward = 1.0
    else:
        reward = 0.0
    reward += curr_score - prev_score
    return reward

def perform_action(emulator: Emulator, action: str) -> None:
    emulator.press_button(action)