from enum import Enum
import constants

class Characters(str, Enum):
    SCARLET = "Miss Scarlet"
    MUSTARD = "Colonel Mustard"
    WHITE = "Mrs. White"
    GREEN = "Mr. Green"
    PEACOCK = "Mrs. Peacock"
    PLUM = "Professor Plum"

characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]

class Character:

    def __init__(self, name, startingPos: tuple, color):
        self.name = name
        self.startingPos = startingPos
        self.color = color

    def move(self, direction: str):
        """Move the character in a specific direction."""
        x, y = self.startingPos
        if direction == 'UP' and y > 0:
            self.startingPos = (x, y - constants.SQUARE_SIZE)  # Move up
        elif direction == 'DOWN' and y < constants.SQUARE_SIZE * (constants.ROWS - 1):
            self.startingPos = (x, y + constants.SQUARE_SIZE)  # Move down
        elif direction == 'LEFT' and x > 0:
            self.startingPos = (x - constants.SQUARE_SIZE, y)  # Move left
        elif direction == 'RIGHT' and x < constants.SQUARE_SIZE * (constants.COLS - 1):
            self.startingPos = (x + constants.SQUARE_SIZE, y)  # Move right


    def __repr__(self):
        return self.name
