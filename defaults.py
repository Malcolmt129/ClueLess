from enum import StrEnum, Enum

class Characters(StrEnum):
    SCARLET = 'Ms. Scarlet'
    MUSTARD = 'Colonel Mustard'
    WHITE = 'Mrs. White'
    GREEN = 'Mr. Green'
    PEACOCK = 'Mrs. Peacock'
    PLUM = 'Professor Plum'

class Weapons(StrEnum):
    CANDLESTICK = 'Candlestick'
    DAGGER = 'Dagger'
    LEAD_PIPE = 'Lead Pipe'
    REVOLVER = 'Revolver'
    ROPE = 'Rope'
    WRENCH = 'Wrench'

class Rooms(StrEnum):
    STUDY = 'Study'
    HALL = 'Hall'
    LOUNGE = 'Lounge' 
    BILLIARD_ROOM = 'Billiard Room'
    LIBRARY = 'Library'
    DINING_ROOM = 'Dining Room' 
    CONSERVATORY = 'Conservatory'
    BALLROOM = 'Ballroom'
    KITCHEN = 'Kitchen'

class RoomPositions(Enum):
    STUDY = (0,0)
    HALL = (0,2)
    LOUNGE = (0,4) 
    BILLIARD_ROOM = (2,0)
    LIBRARY = (2,2)
    DINING_ROOM = (2,4) 
    CONSERVATORY = (4,0)
    BALLROOM = (4,2)
    KITCHEN = (4,4)


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
   Characters.SCARLET: (4, 0),
   Characters.MUSTARD: (6, 2),
   Characters.WHITE: (4, 6),
   Characters.GREEN: (2, 6),
   Characters.PEACOCK: (0, 4),
   Characters.PLUM: (0, 2)
}

hallways = {
    (1,2), (1,4),
    (2,1), (2,3), (2,5),
    (3,2), (3,4),
    (4,1), (4,3), (4,5),
    (5,2), (5,4)
}

valid_moves = {
    starting_locations[Characters.SCARLET]: [(4,1)], # Scarlet starting move
    starting_locations[Characters.MUSTARD]: [(5,2)], # Mustard starting move
    starting_locations[Characters.WHITE]: [(4,5)], # White starting move
    starting_locations[Characters.GREEN]: [(2,5)], # Green starting move
    starting_locations[Characters.PEACOCK]: [(1,4)], # Peacock starting move
    starting_locations[Characters.PLUM]: [(1,2)], # Plum starting move
    (1,1): [(1,2), (2,1), (5,5)],
    (1,2): [(1,1), (1,3)],
    (1,3): [(1,2), (2,3), (1,4)],
    (1,4): [(1,3), (1,5)],
    (1,5): [(1,4), (2,5), (5,1)],
    (2,1): [(1,1), (3,1)],
    (2,2): [],
    (2,3): [(1,3), (3,3)],
    (2,4): [],
    (2,5): [(1,5), (3,5)],
    (3,1): [(2,1), (4,1), (3,2)],
    (3,2): [(3,1), (3,3)],
    (3,3): [(3,2), (2,3), (4,3), (3,4)],
    (3,4): [(3,3), (3,5)],
    (3,5): [(3,4), (2,5), (4,5)],
    (4,1): [(3, 1), (5,1)],
    (4,2): [],
    (4,3): [(3,3), (5,3)],
    (4,4): [],
    (4,5): [(3,5), (5,5)],
    (5,1): [(4,1), (5,2), (1,5)],
    (5,2): [(5,1), (5,3)],
    (5,3): [(5,2), (4,3), (5,4)],
    (5,4): [(5,3), (5,5)],
    (5,5): [(5,4), (4,5), (1,1)]
}
