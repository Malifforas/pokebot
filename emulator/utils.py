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

def get_reward(action, prev_state, curr_state):
    """
    Calculates the reward for taking a particular action.

    Args:
        action (int): The action taken by the agent.
        prev_state (GameState): The game state before the action was taken.
        curr_state (GameState): The game state after the action was taken.

    Returns:
        float: The reward for taking the action.
    """
    # Implementation details omitted for brevity

def perform_action(emulator: Emulator, action: str) -> None:
    emulator.press_button(action)