from .emulator import Emulator
from .utils import (
    load_rom,
    reset_emulator,
    get_game_state,
    get_action_space,
    get_reward,
    perform_action,
)


class PokemonAI:
    def __init__(self, rom_path, emulator_path):
        self.rom_path = rom_path
        self.emulator_path = emulator_path
        self.emulator = None

    def start(self):
        # Load ROM and start emulator
        self.emulator = Emulator(self.emulator_path, self.rom_path)
        load_rom(self.emulator, self.rom_path)
        self.emulator.start()

    def reset(self):
        # Reset emulator to starting state
        reset_emulator(self.emulator)

    def get_state(self):
        # Get game state from emulator
        return get_game_state(self.emulator)

    def get_action_space(self):
        # Get list of possible actions for the AI to take
        return get_action_space()

    def get_reward(self, prev_state, curr_state, action):
        # Get reward for the AI's action
        return get_reward(prev_state, curr_state, action)

    def perform_action(self, action):
        # Perform action in emulator
        perform_action(self.emulator, action)

    def stop(self):
        # Stop emulator
        self.emulator.stop()