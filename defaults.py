from enum import StrEnum, Enum

class Characters(StrEnum):
    SCARLET = 'Miss Scarlet'
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
    STUDY = (1,1)
    HALL = (3,1)
    LOUNGE = (5,1)
    BILLIARD_ROOM = (1,3)
    LIBRARY = (3,3)
    DINING_ROOM = (5,3)
    CONSERVATORY = (1,5)
    BALLROOM = (3,5)
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
    starting_locations[Characters.SCARLET]: [(4,1)],
    starting_locations[Characters.MUSTARD]: [(5,2)],
    starting_locations[Characters.WHITE]: [(4,5)],
    starting_locations[Characters.GREEN]: [(2,5)],
    starting_locations[Characters.PEACOCK]: [(1,4)],
    starting_locations[Characters.PLUM]: [(1,2)],
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
    (4,1): [(3,1), (5,1)],
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

# NEW GLOBAL MAPPINGS
character_name_mapping = {char: char.value for char in Characters}
weapon_name_mapping = {weapon: weapon.value for weapon in Weapons}
room_name_mapping = {room: room.value for room in Rooms}
