import characters


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.location = None
    
    def receive_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        return f"{self.name} (Card: {self.cards})"

