from poke_env.environment.side_condition import SideCondition
from poke_env.environment.status import Status
from poke_env.environment.weather import Weather
from poke_env.environment.field import Field
from poke_env.environment.game_state import GameState
class PlayerRole(Enum):
    ATTACKER = 1
    DEFENDER = 2

class Target(Enum):
    OPPONENT = 1
    PLAYER = 2

class GameState:
    def __init__(self, player_role):
        self.player_role = player_role
        self.opponent_hp = 100
        self.player_hp = 100
        self.current_turn = 1

    def get_opponent_hp(self):
        return self.opponent_hp

    def get_player_hp(self):
        return self.player_hp

    def set_opponent_hp(self, hp):
        self.opponent_hp = hp

    def set_player_hp(self, hp):
        self.player_hp = hp

    def get_current_turn(self):
        return self.current_turn

    def set_current_turn(self, turn):
        self.current_turn = turn

    def get_player_role(self):
        return self.player_role

class State:
    def __init__(self):
        self.game_state = GameState(PlayerRole.ATTACKER)

    def update(self, player_action, opponent_action):
        if self.game_state.get_player_role() == PlayerRole.ATTACKER:
            self.update_attacker(player_action, opponent_action)
        else:
            self.update_defender(player_action, opponent_action)

    def update_attacker(self, player_action, opponent_action):
        player_move = player_action.move
        opponent_move = opponent_action.move
        player_dmg = player_move.damage
        opponent_dmg = opponent_move.damage

        if player_move.type == opponent_move.type:
            if player_move.priority > opponent_move.priority:
                self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
                self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)
            elif opponent_move.priority > player_move.priority:
                self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)
                self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
            else:
                if player_move.speed > opponent_move.speed:
                    self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
                    self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)
                elif opponent_move.speed > player_move.speed:
                    self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)
                    self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
                else:
                    self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
                    self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)
        elif player_move.type == "attack":
            self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - player_dmg)
        elif opponent_move.type == "attack":
            self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_dmg)

        self.game_state.set_current_turn(self.game_state.get_current_turn() + 1)

    def update_defender(self, player_action, opponent_action):
        if opponent_action.target == Target.OPPONENT:
            self.game_state.set_opponent_hp(self.game_state.get_opponent_hp() - opponent_action.move.damage)
        else:
            self.game_state.set_player_hp(self.game_state.get_player_hp() - opponent_action.move.damage)

        self.game_state.set_current_turn(self.game_state.get_current_turn() + 1)

        if self.game_state.get_current_turn() % 3 == 0:
            self.game_state.set_weather(random.choice(list(Weather)))

            if self.game_state.get_weather() == Weather.HAIL:
                self.game_state.set_player_hp(
                    self.game_state.get_player_hp() - int(self.game_state.get_player_max_hp() / 16))
                self.game_state.set_opponent_hp(
                    self.game_state.get_opponent_hp() - int(self.game_state.get_opponent_max_hp() / 16))
            elif self.game_state.get_weather() == Weather.SAND:
                self.game_state.set_player_hp(
                    self.game_state.get_player_hp() - int(self.game_state.get_player_max_hp() / 16))
                self.game_state.set_opponent_hp(
                    self.game_state.get_opponent_hp() - int(self.game_state.get_opponent_max_hp() / 16))
            elif self.game_state.get_weather() == Weather.SUN:
                if Move.FIRE in player_action.move.type:
                    self.game_state.set_opponent_hp(
                        self.game_state.get_opponent_hp() - int(opponent_action.move.damage / 2))
                elif Move.WATER in player_action.move.type:
                    self.game_state.set_opponent_hp(
                        self.game_state.get_opponent_hp() - int(opponent_action.move.damage * 2))
            elif self.game_state.get_weather() == Weather.RAIN:
                if Move.FIRE in player_action.move.type:
                    self.game_state.set_opponent_hp(
                        self.game_state.get_opponent_hp() - int(opponent_action.move.damage * 2))
                elif Move.WATER in player_action.move.type:
                    self.game_state.set_opponent_hp(
                        self.game_state.get_opponent_hp() - int(opponent_action.move.damage / 2))

        if self.game_state.get_player_hp() <= 0:
            self.game_state.set_winner(PlayerRole.OPPONENT)
        elif self.game_state.get_opponent_hp() <= 0:
            self.game_state.set_winner(PlayerRole.PLAYER)