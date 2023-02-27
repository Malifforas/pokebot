from .move import Move
from .game_state import GameState
import poke_env
from enum import Enum
from state import State, PlayerRole
from game_state import GameState
class Action:
    def __init__(self):
        pass

    def perform(self, game_state: GameState) -> bool:
        """
        Performs the action and returns True if successful, False otherwise.
        """
        raise NotImplementedError

class UseMoveAction(Action):
    def __init__(self, move: Move, pokemon_index: int):
        super().__init__()
        self.move = move
        self.pokemon_index = pokemon_index

    def perform(self, game_state: GameState) -> bool:
        """
        Uses a move and returns True if successful, False otherwise.
        """
        # Select the current Pokemon
        current_pokemon = game_state.current_pokemon
        if current_pokemon.fainted:
            return False

        # Select the move
        move_slot = current_pokemon.get_move_slot(self.move)
        if not move_slot:
            return False
        move = move_slot.move

        # Check if the move was successful
        target = game_state.opponent_active_pokemon if self.move.target == Target.OPPONENT else game_state.player_active_pokemon
        success = move.use(current_pokemon, target)
        return success

class SwitchPokemonAction(Action):
    def __init__(self, from_index: int, to_index: int):
        super().__init__()
        self.from_index = from_index
        self.to_index = to_index

    def perform(self, game_state: GameState) -> bool:
        """
        Switches the current Pokemon with another Pokemon and returns True if successful, False otherwise.
        """
        # Get the source and target Pokemon indices
        source_index = self.from_index
        target_index = self.to_index

        # Select the source Pokemon
        source_pokemon = game_state.get_player_pokemon_by_index(source_index)
        if not source_pokemon:
            return False

        # Select the target Pokemon
        target_pokemon = game_state.get_player_pokemon_by_index(target_index)
        if not target_pokemon:
            return False

        # Switch the Pokemon
        game_state.player_team.switch(source_pokemon, target_pokemon)
        return True

    class SwitchPokemonAction(Action):
        def __init__(self, from_index: int, to_index: int):
            super().__init__()
            self.from_index = from_index
            self.to_index = to_index

        def perform(self, game_state: GameState) -> bool:
            # Press the right button to access the Pokemon menu
            if not game_state.is_menu_open:
                game_state.press_key(GameState.RIGHT_KEY)

            # Select the current Pokemon
            current_pokemon_index = game_state.get_current_pokemon_index()
            if current_pokemon_index != self.from_index:
                game_state.press_key(GameState.DOWN_KEY * abs(self.from_index - current_pokemon_index))
                game_state.press_key(GameState.A_KEY)

            # Select the second pokemon
            game_state.press_key(GameState.DOWN_KEY * abs(self.to_index - self.from_index))
            game_state.press_key(GameState.A_KEY)

            # Confirm the switch
            game_state.press_key(GameState.A_KEY)

            # Check if the switch was successful
            return game_state.get_current_pokemon_index() == self.to_index

    class UseItemAction(Action):
        def __init__(self, item_index: int, pokemon_index: int = None):
            super().__init__()
            self.item_index = item_index
            self.pokemon_index = pokemon_index

        def perform(self, game_state: GameState) -> bool:
            bag_index = self.item_index + 1  # index in bag is 1-based
            # Open the bag
            if not game_state.menu.open_bag():
                return False

            # Select the item
            if not game_state.menu.select_item(bag_index):
                return False

            # Select the Pokemon to use the item on (if applicable)
            if self.pokemon_index is not None:
                if not game_state.menu.choose_pokemon(self.pokemon_index):
                    return False

            # Use the item
            if not game_state.menu.use_item():
                return False

            # Check if the item was used successfully
            return game_state.menu.choose_menu_index(1)  # confirm that the item was used

    class RunAction(Action):
        def __init__(self):
            super().__init__()

        def perform(self, game_state: GameState) -> bool:
            # Press the 'RUN' button
            run_button = game_state.screen.grab(run_button_region)
            run_button_location = game_state.screen.search(run_button)
            game_state.input_controller.click(run_button_location)

            # Check if the player successfully escaped
            return game_state.menu_helper.choose_if_present([
                ('text', 'Where will you go?'),
                ('text', 'Got away safely!')]) is not None
class TalkToAction(Action):
    def __init__(self):
        super().__init__()

    def perform(self, game_state: GameState) -> bool:
        # Press the 'A' button to interact with an NPC
        game_state.press_button(Button.A)

        # Wait for the interaction to complete
        time.sleep(1)

        # Check if the player successfully interacted
        return game_state.screen != Screen.OVERWORLD


class WaitAction(Action):
    def __init__(self, duration: float):
        super().__init__()
        self.duration = duration

    def perform(self, game_state: GameState) -> bool:
        start_time = time.monotonic()
        while time.monotonic() - start_time < self.duration:
            pass
        return True


class SequenceAction(Action):
    def __init__(self, actions: List[Action]):
        super().__init__()
        self.actions = actions

    def perform(self, game_state: GameState) -> bool:
        for action in self.actions:
            if not action.perform(game_state):
                return False
        return True


class ConditionalAction(Action):
    def __init__(self, condition: Callable[[], bool], action: Action):
        super().__init__()
        self.condition = condition
        self.action = action

    def perform(self, game_state: GameState) -> bool:
        # Check the condition, and perform the action if it is True
        if self.condition():
            return self.action.perform(game_state)
        return True
class UntilFailAction(Action):
    def __init__(self, action: Action):
        super().__init__()
        self.action = action

    def perform(self, game_state: GameState) -> bool:
        while True:
            success = self.action.perform(game_state)
            if not success:
                break
        return True


class UntilSuccessAction(Action):
    def __init__(self, action: Action):
        super().__init__()
        self.action = action

    def perform(self, game_state: GameState) -> bool:
        while True:
            success = self.action.perform(game_state)
            if success:
                break
        return True


class UntilTimeoutAction(Action):
    def __init__(self, action: Action, timeout: float):
        super().__init__()
        self.action = action
        self.timeout = timeout

    def perform(self, game_state: GameState) -> bool:
        start_time = time.monotonic()
        while True:
            success = self.action.perform(game_state)
            if success:
                return True
            elapsed_time = time.monotonic() - start_time
            if elapsed_time > self.timeout:
                return False
