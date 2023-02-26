import numpy as np
from PIL import Image
from .emulator import Emulator


class Util:
    @staticmethod
    def get_screen_dimensions(screen):
        return screen.shape[0], screen.shape[1]

    @staticmethod
    def resize_screen(screen, width, height):
        return np.array(Image.fromarray(screen).resize((width, height), resample=Image.BOX))


def load_rom(emulator: Emulator, rom_path: str) -> None:
    with open(rom_path, "rb") as f:
        rom = f.read()
    emulator.load_rom(rom)


def reset_emulator(emulator: Emulator) -> None:
    buttons_to_press = ["POWER", "A", "START", "A", "A", "A", "A", "A", "A"]
    for button in buttons_to_press:
        emulator.press_button(button)


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
        action (str): The action taken by the agent.
        prev_state (np.ndarray): The game state before the action was taken.
        curr_state (np.ndarray): The game state after the action was taken.

    Returns:
        float: The reward for taking the action.
    """
    # Implementation details omitted for brevity


def perform_action(emulator: Emulator, action: str) -> None:
    emulator.press_button(action)


def crop_screen(screen):
    # Get the dimensions of the screen
    screen_width, screen_height = Util.get_screen_dimensions(screen)

    # Crop the center 256x256 portion of the screen
    crop_left = (screen_width - 256) // 2
    crop_right = crop_left + 256
    crop_top = (screen_height - 256) // 2
    crop_bottom = crop_top + 256
    cropped_screen = screen[crop_top:crop_bottom, crop_left:crop_right, :]

    return cropped_screen