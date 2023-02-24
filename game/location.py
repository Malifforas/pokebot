from random import random


class Location:
    """
    A class representing a location in the game world.
    """

    def __init__(self, name, pokemon=None, trainers=None, items=None):
        """
        Initializes a new Location instance.

        :param name: The name of the location.
        :param pokemon: A list of Pokemon that can be encountered in the location.
        :param trainers: A list of trainers that can be battled in the location.
        :param items: A list of items that can be found in the location.
        """
        self.name = name
        self.pokemon = pokemon or []
        self.trainers = trainers or []
        self.items = items or []

    def __str__(self):
        """
        Returns a string representation of the location.

        :return: The string representation of the location.
        """
        return self.name

    def get_wild_pokemon(self):
        """
        Returns a random Pokemon from the list of Pokemon that can be encountered in the location.

        :return: A random Pokemon from the list of Pokemon that can be encountered in the location.
        """
        if not self.pokemon:
            return None

        return random.choice(self.pokemon)

    def get_trainer(self):
        """
        Returns a random trainer from the list of trainers that can be battled in the location.

        :return: A random trainer from the list of trainers that can be battled in the location.
        """
        if not self.trainers:
            return None

        return random.choice(self.trainers)

    def get_item(self):
        """
        Returns a random item from the list of items that can be found in the location.

        :return: A random item from the list of items that can be found in the location.
        """
        if not self.items:
            return None

        return random.choice(self.items)