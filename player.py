from defaults import Characters, Weapons, Rooms, starting_locations
from typing import Union

class Player:
    def __init__(self, id: int, character: Characters, cards: set[Union[Characters, Weapons, Rooms]] = set(), position: tuple[int,int] = None):
        self._id = id
        self._character = character
        self._position = position if position else starting_locations[character]  # Default starting position
        self._cards = cards
        self._eligable: bool = True
        self._can_move: int = False
        self._can_suggest: bool = False

    @property
    def id(self):
        """Getter for the id attribute"""
        return self._id

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
        if not isinstance(value, tuple):
            raise TypeError("Argument must be a tuple[int, int]")
        self._position = value

    @property
    def can_suggest(self):
        """Getter for the can_suggest attribute"""
        return self._can_suggest

    @can_suggest.setter
    def can_suggest(self, value: bool):
        """Setter for the can_suggest attribute"""
        if not isinstance(value, bool):
            raise TypeError("Argument must be a bool")
        self._can_suggest = value

    @property
    def can_move(self):
        """Getter for the can_move attribute"""
        return self._can_move

    @can_move.setter
    def can_move(self, value: bool):
        """Setter for the can_move attribute"""
        if not isinstance(value, bool):
            raise TypeError("Argument must be a bool")
        self._can_move = value

    @property
    def eligable(self):
        """Getter for the eligable attribute"""
        return self._eligable

    @eligable.setter
    def eligable(self, value: bool):
        """Setter for the eligable attribute"""
        if not isinstance(value, bool):
            raise TypeError("Argument must be a bool")
        self._eligable = value

    def add_card(self, card: Union[Characters, Weapons, Rooms]):
        if not isinstance(card, (Characters, Weapons, Rooms)):
            raise TypeError("Argument must be of type Characters, Weapons, or Rooms")
        self._cards.add(card)       

    def __repr__(self):
        return (f"Player(id={self._id!r}, "
                f"character={self._character!r}, "
                f"position={self._position!r}, "
                f"cards={list(self._cards)!r}, "
                f"eligable={self._eligable!r}, "
                f"can_suggest={self._can_suggest!r})")
