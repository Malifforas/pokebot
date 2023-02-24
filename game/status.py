from typing import List, Tuple
from game.location import Location

class Status:
    def __init__(self, name: str, team: List[Tuple[str, int]]):
        self.name = name
        self.team = team
        self.current_location = Location("New Bark Town", "home")
        self.pokedex = {}

    def get_name(self):
        return self.name

    def get_team(self):
        return self.team

    def get_location(self):
        return self.current_location

    def set_location(self, location: Location):
        self.current_location = location

    def add_to_pokedex(self, pokemon: str):
        if pokemon not in self.pokedex:
            self.pokedex[pokemon] = 0
