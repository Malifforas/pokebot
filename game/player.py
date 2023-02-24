from game.location import Location


class Player:
    def __init__(self, name):
        self.name = name
        self.current_location = None
        self.party = []
        self.pokedex = []
        self.money = 3000

    def travel(self, location):
        if isinstance(location, Location):
            self.current_location = location
            print(f"{self.name} traveled to {location.name}")
        else:
            print(f"{location.name} is not a valid location.")

    def add_pokemon_to_party(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            print(f"{pokemon.name} was added to {self.name}'s party!")
        else:
            print(f"{self.name}'s party is full!")

    def add_pokemon_to_pokedex(self, pokemon):
        if pokemon not in self.pokedex:
            self.pokedex.append(pokemon)
            print(f"{pokemon.name} was added to {self.name}'s Pokedex!")
        else:
            print(f"{pokemon.name} is already in {self.name}'s Pokedex.")

    def deposit_pokemon(self, pokemon):
        if pokemon in self.party:
            self.party.remove(pokemon)
            print(f"{pokemon.name} was deposited into {self.name}'s PC!")
        else:
            print(f"{pokemon.name} is not in {self.name}'s party.")

    def withdraw_pokemon(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            print(f"{pokemon.name} was withdrawn from {self.name}'s PC!")
        else:
            print(f"{self.name}'s party is full, can't withdraw {pokemon.name}.")