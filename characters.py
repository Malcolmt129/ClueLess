from enum import Enum

class Characters(str, Enum):
    SCARLET = "Miss Scarlet"
    MUSTARD = "Colonel Mustard"
    WHITE = "Mrs. White"
    GREEN = "Mr. Green"
    PEACOCK = "Mrs. Peacock"
    PLUM = "Professor Plum"

characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]

class Character:
<<<<<<< HEAD

    def __init__(self, name, startingPos: tuple, color):
        self.name = name
        self.startingPos = startingPos
        self.color = ()



=======
    def __init__(self, name, category):
        self.name = name
        self.category = category
>>>>>>> feature/tyler_backend
    def __repr__(self):
        return self.name
