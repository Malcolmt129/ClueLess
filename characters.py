from constants import SQUARE_SIZE, HEIGHT, WIDTH, SQUARE_SIZE_DRAWN
from defaults import Characters, RoomPositions, RoomPositionsToRooms, starting_locations, valid_moves, hallways
import pygame
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Store custom name mappings
_custom_name_to_enum = {}

offsets = {
   Characters.SCARLET: (2 * SQUARE_SIZE, 1.25*SQUARE_SIZE),
   Characters.WHITE: (2 * SQUARE_SIZE, 0),
   Characters.PEACOCK: (2 * SQUARE_SIZE, -1.25*SQUARE_SIZE),
   Characters.MUSTARD: (0, 1.25*SQUARE_SIZE),
   Characters.GREEN: (0, 0),
   Characters.PLUM: (0, -1.25*SQUARE_SIZE)
}

class Character:

    def __init__(self, screen: pygame.Surface, name, startingPos: tuple, color: tuple):
        
        self.name = name
        self.enumRep = _name_to_enum(name) #For getting the representation of character in enum
        self.startingPos = startingPos
        self.position = startingPos 
        self.pixel_position = startingPos        
        self.color = color
        self.screen = screen
    

    def positionConversion(self, position: tuple[int, int]):
        
        # x = (position[0] * SQUARE_SIZE_DRAWN) + (SQUARE_SIZE_DRAWN // 2) - (SQUARE_SIZE)
        # y = (position[1] * SQUARE_SIZE_DRAWN) + (SQUARE_SIZE_DRAWN // 2) - (SQUARE_SIZE*2)
        x = (position[0] * SQUARE_SIZE_DRAWN) + offsets[self.enumRep][0]
        y = (position[1] * SQUARE_SIZE_DRAWN) + offsets[self.enumRep][1]
        return (x, y)
       

    def draw(self):
            pos = self.positionConversion(self.startingPos)
            if self.position == self.startingPos:  
                pygame.draw.circle(self.screen, self.color, self.positionConversion(self.startingPos), 20)  # Token size = 20px
            # This means that the player has moved before and any movement now needs to be converted
            # to an area of a particular room.
            else:
                pygame.draw.circle(self.screen, self.color, self.pixel_position, 20)
                # Use the postion given by the room to draw the player.
    

    def drawProto(self, rooms):
        pos = self.positionConversion(self.position)
        logger.debug(f"{self.name} -> {self.position} {pos}")
        pygame.draw.circle(self.screen, self.color, pos, 20)  # Token size = 20px
        # try:

        #     currentRoomName = self.getRoomKey()
        #     pos = self.positionConversion(rooms[currentRoomName].location)
        #     logger.info(f"{self.name} -> {rooms[currentRoomName].location} {pos}")
        #     pygame.draw.circle(self.screen, self.color, self.positionConversion(rooms[currentRoomName].location), 20)  # Token size = 20px

        # except ValueError:
            
        #     logger.debug(f"{self.name} -> ValueError")
        #     if self.position in hallways:
        #         logger.debug(f"{self.name} -> in hallway")
        #         for room in rooms.values():

        #             if self.position == room.location:
        #                 currentRoomName = room.name 
        #                 pos = self.positionConversion(rooms[currentRoomName].location)
        #                 logger.info(f"{self.name} -> {pos}")
        #                 pygame.draw.circle(self.screen, self.color, self.positionConversion(rooms[currentRoomName].location), 20)  # Token size = 20px
        #                 return
                


    def getRoomKey(self):
        if self.position == self.startingPos:
            for char_enum, start_pos in starting_locations.items():
                if self.position == start_pos:
                    return char_enum.value
        else:
            room_pos = RoomPositions(self.position)
            return RoomPositionsToRooms(room_pos)


    def __repr__(self):
        return f"Character name: {self.name}, Postion: {self.position}" 

class CharacterFactory:
 
    @staticmethod
    def create_Character(screen: pygame.Surface, name, startingPos, color: tuple):
        return Character(screen, name, startingPos, color)


def set_custom_names(custom_names_dict):
    """Set up custom name mappings for characters."""
    global _custom_name_to_enum
    _custom_name_to_enum = {}
    if custom_names_dict and 'characters' in custom_names_dict:
        for enum_char, custom_name in zip(Characters, custom_names_dict['characters']):
            _custom_name_to_enum[custom_name] = enum_char

def _name_to_enum(name: str) -> Characters:
    """Convert a character name (custom or default) to its enum representation."""
    # First check if it's a custom name
    if name in _custom_name_to_enum:
        return _custom_name_to_enum[name]
    
    # Then check if it matches any enum values
    for char in Characters:
        if char.value == name:
            return char

    raise ValueError(f"No character enum matches name '{name}'")
