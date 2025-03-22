from enum import Enum

class Characters(str, Enum):
    SCARLET = 'Miss Scarlet'
    MUSTARD = 'Colonel Mustard'
    WHITE = 'Mrs. White'
    GREEN = 'Mr. Green'
    PEACOCK = 'Mrs. Peacock'
    PLUM = 'Professor Plum'

class Weapons(str, Enum):
    CANDLESTICK = 'Candlestick',
    DAGGER = 'Dagger',
    LEAD_PIPE = 'Lead Pipe',
    REVOLVER = 'Revolver',
    ROPE = 'Rope',
    WRENCH = 'Wrench'

class Rooms(str, Enum):
    STUDY = 'Study', 
    HALL = 'Hall',
    LOUNGE = 'Lounge', 
    BILLIARD_ROOM = 'Billiard Room',
    LIBRARY = 'Library',
    DINING_ROOM = 'Dining Room', 
    CONSERVATORY = 'Conservatory',
    BALLROOM = 'Ballroom',
    KITCHEN = 'Kitchen'

starting_locations = {
   Characters.SCARLET: (0, 3),
   Characters.MUSTARD: (1, 4),
   Characters.WHITE: (4, 3),
   Characters.GREEN: (4, 1),
   Characters.PEACOCK: (3, 0),
   Characters.PLUM: (1, 0),
}

valid_moves = {
    (0,0): [(0,1), (1,0), (4,4)],
    (0,1): [(0,0), (0,2)],
    (0,2): [(0,1), (1,1), (0,3)],
    (0,3): [(0,2), (0,4)],
    (0,4): [(0,3), (1,4), (4,0)],
    (1,0): [(0,0), (2,0)],
    (1,1): [],
    (1,2): [(0,2), (2,2)],
    (1,3): [],
    (1,4): [(0,4), (2,4)],
    (2,0): [(1,0), (3,0), (2,1)],
    (2,1): [(2,0), (2,2)],
    (2,2): [(2,1), (1,2), (3,2), (2,3)],
    (2,3): [(2,2), (2,4)],
    (2,4): [(2,3), (1,4), (3,4)],
    (3,0): [(2, 0), (4,0)],
    (3,1): [],
    (3,2): [(2,2), (4,2)],
    (3,3): [],
    (3,4): [(2,4), (4,4)],
    (4,0): [(3,0), (4,1), (0,4)],
    (4,1): [(4,0), (4,2)],
    (4,2): [(4,1), (3,2), (4,3)],
    (4,3): [(4,2), (4,4)],
    (4,4): [(4,3), (3,4), (0,0)]
}
