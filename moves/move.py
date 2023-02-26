from api import get_move_data


class Move:
    def __init__(self, name):
        self.name = name
        self.data = get_move_data(name)

    @property
    def power(self):
        return self.data['power']

    @property
    def type(self):
        return self.data['type']['name']

    @property
    def accuracy(self):
        return self.data['accuracy']

    @property
    def pp(self):
        return self.data['pp']

    def __repr__(self):
        return f"Move(name={self.name}, type={self.type})"
