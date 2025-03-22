from defaults import Characters, Weapons, Rooms, starting_locations
from typing import Union

class Player:
    def __init__(self, character: Characters):
        self._character = character
        self._position = starting_locations[character]  # Default starting position
        self._cards = set()

    @property
    def character(self):
        """Getter for the character attribute"""
        return self._character
    
    @property
    def position(self):
        """Getter for the position attribute"""
        return self._position
    
    @property
    def cards(self):
        """Getter for the cards attribute"""
        return self._cards

    @position.setter
    def position(self, value: tuple[int, int]):
        """Setter for the position attribute"""
        if not isinstance(value, tuple[int, int]):
            raise TypeError("Argument must be a tuple[int, int]")
        self._position = value

    def add_card(self, card: Union[Characters, Weapons, Rooms]):
        if not isinstance(card, (Characters, Weapons, Rooms)):
            raise TypeError("Argument must be of type Characters, Weapons, or Rooms")
        self._cards.add(card)       

    def __repr__(self):
        return (f"Player(character={self._character!r}, "
                f"position={self._position!r}, "
                f"cards={list(self._cards)!r})") 