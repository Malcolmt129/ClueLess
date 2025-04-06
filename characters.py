from enum import Enum
import constants
from room import Room
class Characters(str, Enum):
    SCARLET = "Ms. Scarlet"
    MUSTARD = "Colonel Mustard"
    WHITE = "Mrs. White"
    GREEN = "Mr. Green"
    PEACOCK = "Mrs. Peacock"
    PLUM = "Professor Plum"


class Character:

    def __init__(self, name, startingPos: tuple, color: tuple):
        self.name = name
        self.startingPos = startingPos
        self.position = startingPos 
        self.color = color

    def move(self, direction: str):
        """Move the character in a specific direction."""
        x, y = self.startingPlace
        if direction == 'UP' and y > 0:
            self.startingPlace = (x, y - constants.SQUARE_SIZE)  # Move up
        elif direction == 'DOWN' and y < constants.SQUARE_SIZE * (constants.ROWS - 1):
            self.startingPlace = (x, y + constants.SQUARE_SIZE)  # Move down
        elif direction == 'LEFT' and x > 0:
            self.startingPlace = (x - constants.SQUARE_SIZE, y)  # Move left
        elif direction == 'RIGHT' and x < constants.SQUARE_SIZE * (constants.COLS - 1):
            self.startingPlace = (x + constants.SQUARE_SIZE, y)  # Move right

    def updatePostion(self, position: tuple):
        self.postion = position

    def __repr__(self):
        return f"Character name: {self.name}, Postion: {self.position}" 

class CharacterFactory:

    @staticmethod
    def create_Character(name, startingPlace, color: tuple):
        return Character(name, startingPlace, color)
