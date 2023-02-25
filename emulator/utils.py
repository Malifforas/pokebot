import numpy as np
from .emulator import Emulator
from PIL import Image

class Util:
    @staticmethod
    def get_screen_dimensions(screen):
        return screen.shape[0], screen.shape[1]

    @staticmethod
    def crop_screen(screen, top, bottom, left, right):
        return screen[top:bottom, left:right]

    @staticmethod
    def resize_screen(screen, width, height):
        return np.array(Image.fromarray(screen).resize((width, height), resample=Image.BOX))

def image(im):
    """
    Create an image from a numpy array.

    Args:
        im (np.ndarray): The numpy array to convert to an image.

    Returns:
        Image: The PIL Image object.
    """
    im = im.copy()
    if len(im.shape) == 2:
        im = np.stack([im] * 3, axis=-1)
    im = (im * 255.0).astype(np.uint8)
    return Image.fromarray(im)
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

    def crop_screen(screen, crop_size):
        height, width, _ = screen.shape
        crop_height, crop_width = crop_size
        start_x = (width - crop_width) // 2
        start_y = (height - crop_height) // 2
        end_x = start_x + crop_width
        end_y = start_y + crop_height
        return screen[start_y:end_y, start_x:end_x, :]

