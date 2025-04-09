from enum import StrEnum, Enum

class Characters(StrEnum):
    SCARLET = 'Ms. Scarlet'
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

class RoomPositions(Enum):
    STUDY = (1,1)
    HALL = (1,3)
    LOUNGE = (1,5) 
    BILLIARD_ROOM = (3,1)
    LIBRARY = (3,3)
    DINING_ROOM = (3,5) 
    CONSERVATORY = (5,1)
    BALLROOM = (5,3)
    KITCHEN = (5,5)


def RoomsToRoomPositions(room: Rooms) -> RoomPositions:
    room_position_mapping = {
        Rooms.STUDY: RoomPositions.STUDY,
        Rooms.HALL: RoomPositions.HALL,
        Rooms.LOUNGE: RoomPositions.LOUNGE,
        Rooms.BILLIARD_ROOM: RoomPositions.BILLIARD_ROOM,
        Rooms.LIBRARY: RoomPositions.LIBRARY,
        Rooms.DINING_ROOM: RoomPositions.DINING_ROOM,
        Rooms.CONSERVATORY: RoomPositions.CONSERVATORY,
        Rooms.BALLROOM: RoomPositions.BALLROOM,
        Rooms.KITCHEN: RoomPositions.KITCHEN,
    }
    return room_position_mapping.get(room)


def RoomPositionsToRooms(position: RoomPositions) -> Rooms:
    position_to_room_mapping = {
        RoomPositions.STUDY: Rooms.STUDY,
        RoomPositions.HALL: Rooms.HALL,
        RoomPositions.LOUNGE: Rooms.LOUNGE,
        RoomPositions.BILLIARD_ROOM: Rooms.BILLIARD_ROOM,
        RoomPositions.LIBRARY: Rooms.LIBRARY,
        RoomPositions.DINING_ROOM: Rooms.DINING_ROOM,
        RoomPositions.CONSERVATORY: Rooms.CONSERVATORY,
        RoomPositions.BALLROOM: Rooms.BALLROOM,
        RoomPositions.KITCHEN: Rooms.KITCHEN,
    }
    return position_to_room_mapping.get(position)


starting_locations = {
#    Characters.SCARLET: (-1, -1),
   Characters.SCARLET: (4, 0),
   Characters.MUSTARD: (6, 2),
   Characters.WHITE: (4, 6),
   Characters.GREEN: (2, 6),
   Characters.PEACOCK: (0, 4),
   Characters.PLUM: (0, 2),
}

hallways = {
    (0,1), (0,3),
    (1,0), (1,2), (1,4),
    (2,1), (2,3),
    (3,0), (3,2), (3,4),
    (4,1), (4,3)
}

valid_moves = {
    starting_locations[Characters.SCARLET]: [(0,3)], # Scarlet starting move
    starting_locations[Characters.MUSTARD]: [(1,4)], # Mustard starting move
    starting_locations[Characters.WHITE]: [(4,3)], # White starting move
    starting_locations[Characters.GREEN]: [(4,1)], # Green starting move
    starting_locations[Characters.PEACOCK]: [(3,0)], # Peacock starting move
    starting_locations[Characters.PLUM]: [(1,0)], # Plum starting move
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
