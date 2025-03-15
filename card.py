import characters


class Card:

    def __init__(self, name, category):
        self.name = name
        self.category = category


    def __repr__(self) -> str:
        return self.name
