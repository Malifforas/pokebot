from typing import List, Dict, Any

class Pokemon:
    def __init__(self, data: Dict[str, Any]):
        self.name = data['name']
        self.hp = data['hp']
        self.max_hp = data['max_hp']
        self.status = data['status']
        self.moves = data['moves']
        self.active = data['active']

class Opponent:
    def __init__(self, data: Dict[str, Any]):
        self.name = data['name']
        self.hp = data['hp']
        self.max_hp = data['max_hp']
        self.status = data['status']

class GameState:
    def __init__(self, player_data: Dict[str, Any], opponent_data: Dict[str, Any]):
        self.player = Pokemon(player_data)
        self.opponent = Opponent(opponent_data)