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
def get_possible_moves(emulator: Emulator) -> List[str]:
    """
    Returns a list of valid moves that the agent can take from its current state.

    Args:
        emulator (Emulator): The Emulator object.

    Returns:
        List[str]: A list of valid moves that the agent can take.
    """
    moves = []
    for move in get_action_space():
        try:
            emulator.press_button(move)
            emulator.release_button(move)
            moves.append(move)
        except EmulatorInputError:
            pass
    return moves
def get_q_value(q_table: dict, state: np.ndarray, action: str) -> float:
    """
    Returns the Q-value for a given state-action pair.

    Args:
        q_table (dict): The Q-table.
        state (np.ndarray): The game state.
        action (str): The action taken by the agent.

    Returns:
        float: The Q-value for the state-action pair.
    """
    state_key = str(state)
    if state_key not in q_table:
        q_table[state_key] = {a: 0.0 for a in get_action_space()}
    return q_table[state_key][action]
def update_q_table(q_table: dict, state: np.ndarray, action: str, reward: float, next_state: np.ndarray, discount_factor: float, learning_rate: float) -> None:
    """
    Updates the Q-value for a given state-action pair based on the observed reward and the expected future reward.

    Args:
        q_table (dict): The Q-table.
        state (np.ndarray): The game state.
        action (str): The action taken by the agent.
        reward (float): The observed reward.
        next_state (np.ndarray): The game state after the action was taken.
        discount_factor (float): The discount factor for future rewards.
        learning_rate (float): The learning rate for updating Q-values.
    """
    state_key = str(state)
    if state_key not in q_table:
        q_table[state_key] = {a: 0.0 for a in get_action_space()}
    next_q = max([get_q_value(q_table, next_state, a) for a in get_possible_moves(NUZLOCKE.emulator)])
    q_table[state_key][action] += learning_rate * (reward + discount_factor * next_q - q_table[state_key][action])

    def decision(q_table: dict, state: np.ndarray, epsilon: float, discount_factor: float, learning_rate: float) -> str:
        """
        Uses the Q-table to decide on an action to take in the current game state.

        Args:
            q_table (dict): A dictionary representing the Q-table.
            state (np.ndarray): The current game state.
            epsilon (float): The probability of choosing a random action.
            discount_factor (float): The discount factor for future rewards.
            learning_rate (float): The learning rate for updating the Q-table.

        Returns:
            str: The action to take.
        """
        action_space = get_action_space()

        # Choose a random action with probability epsilon
        if np.random.uniform() < epsilon:
            action = np.random.choice(action_space)
        # Otherwise, choose the action with the highest Q-value for the current state
        else:
            state_key = str(state)
            q_values = q_table[state_key]
            max_q_value = max(q_values)
            max_q_indices = [i for i, q_value in enumerate(q_values) if q_value == max_q_value]
            max_q_index = np.random.choice(max_q_indices)
            action = action_space[max_q_index]

        return action