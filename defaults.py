from enum import StrEnum

class Characters(StrEnum):
    SCARLET = 'Miss Scarlet'
    MUSTARD = 'Colonel Mustard'
    WHITE = 'Mrs. White'
    GREEN = 'Mr. Green'
    PEACOCK = 'Mrs. Peacock'
    PLUM = 'Professor Plum'

class Weapons(StrEnum):
    CANDLESTICK = 'Candlestick',
    DAGGER = 'Dagger',
    LEAD_PIPE = 'Lead Pipe',
    REVOLVER = 'Revolver',
    ROPE = 'Rope',
    WRENCH = 'Wrench'

class Rooms(StrEnum):
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
   Characters.SCARLET: (-1, -1),
   Characters.MUSTARD: (-1, -2),
   Characters.WHITE: (-1, -3),
   Characters.GREEN: (-1, -4),
   Characters.PEACOCK: (-1, -5),
   Characters.PLUM: (-1, -6),
}

hallways = {
    (0,1), (0,3),
    (1,0), (1,2), (1,4),
    (2,1), (2,3),
    (3,0), (3,2), (3,4),
    (4,1), (4,3)
}

valid_moves = {
    (-1,-1): [(0,3)], # Scarlet starting move
    (-1,-2): [(1,4)], # Mustard starting move
    (-1,-3): [(4,3)], # White starting move
    (-1,-4): [(4,1)], # Green starting move
    (-1,-5): [(3,0)], # Peacock starting move
    (-1,-6): [(1,0)], # Plum starting move
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
