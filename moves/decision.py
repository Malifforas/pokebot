from typing import List
import numpy as np
from .util import get_screen_dimensions, crop_screen, check_for_shiny, get_text, get_npc_text, get_move_description
from .emulator import Emulator, EmulatorConnectionError, EmulatorInputError, EmulatorStartupError
from .nuzlocke import Nuzlocke

# The global Nuzlocke object that will be used throughout the game
NUZLOCKE = Nuzlocke()


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
    state = crop_screen(state, get_screen_dimensions())
    state = np.array(state)
    state = np.transpose(state, (1, 0, 2))
    state = state / 255.0
    return state


def get_action_space() -> List[str]:
    return ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "START", "SELECT"]


def get_reward(action: str, prev_state: np.ndarray, curr_state: np.ndarray) -> float:
    """
    Calculates the reward for taking a particular action.

    Args:
        action (str): The action taken by the agent.
        prev_state (np.ndarray): The game state before the action was taken.
        curr_state (np.ndarray): The game state after the action was taken.

    Returns:
        float: The reward for taking the action.
    """
    reward = 0.0

    # If the game over screen is displayed, return a negative reward
    game_over_screen = crop_screen(curr_state, (160, 128, 3), (160, 32))
    if np.mean(game_over_screen) < 0.1:
        reward = -1.0
        return reward

    # If a shiny Pokemon is encountered, return a high positive reward
    if check_for_shiny(curr_state):
        reward = 100.0
        return reward

    # If an NPC is talking, return a negative reward to encourage the agent to move on
    if get_npc_text(curr_state) != "":
        reward = -0.1
        return reward

    # If the action taken was to move to a new location, check if a new encounter has been made
    if action in ["UP", "DOWN", "LEFT", "RIGHT"]:
        new_state_text = get_text(curr_state)
        if new_state_text != "" and new_state_text != get_text(prev_state):
            if NUZLOCKE.is_new_encounter():
                reward = 10.0
                return reward
            else:
                reward = -10.0
                return reward

    # If no other reward condition is met, return a small negative reward to encourage the agent to move
    reward = -0.01
    return reward
def perform_action(emulator: Emulator, action: str) -> None:
    try:
        emulator.press_button(action)
    except EmulatorButtonError:
        pass
    except EmulatorConnectionError:
        raise
