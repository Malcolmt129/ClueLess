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

offsets = {
   Characters.SCARLET: (2, -0.25),
   Characters.WHITE: (2, 1),
   Characters.PEACOCK: (2, 2.25),
   Characters.MUSTARD: (0, -0.25),
   Characters.GREEN: (0, 1),
   Characters.PLUM: (0, 2.25)
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
        self.positionMap = {
                            (0,2): (3.5, 8.5), (0, 4): (3.5, 16.5), #starting locations
                            (4, 0): (16.5, 2.5), (2, 6): (9.5, 21.5), #Starting locations
                            (1, 1): (4, 3), (2, 1): (8, 4), (3, 1): (12, 3), (4, 1): (16, 4), (5, 1): (20, 3), 
                            (1, 2): (5, 7), (3, 2): (13, 7), (5, 2): (21, 7),  
                            (1, 3): (4, 11), (2, 3): (8, 12), (3, 3): (12, 11), (4, 3): (16, 12), (5, 3): (20, 11), 
                            (1, 4): (5, 15), (3, 4): (13, 15), (5, 4): (21, 15),   
                            (1, 5): (4, 19), (2, 5): (8, 20), (3, 5): (12, 19), (4, 5): (16, 20), (5, 5): (20, 19), 
                            (6, 2): (22.5, 7.5), (4, 6): (17.5, 21.5) #Starting locations
                            }
    

    def positionConversion(self, position: tuple[int, int]):
        
        coords = self.positionMap.get(position, (0,0)) 

        if any(self.position == room_pos.value for room_pos in RoomPositions):

            self.pixel_position = ((coords[0] + offsets[self.name][0]) * SQUARE_SIZE, (coords[1] + offsets[self.name][1]) * SQUARE_SIZE)
        
        else:

            self.pixel_position = (coords[0] * SQUARE_SIZE, coords[1] * SQUARE_SIZE)
        
        return  self.pixel_position



    def draw(self):
            pos = self.positionConversion(self.position)
            pygame.draw.circle(self.screen, self.color, pos, 20)  # Token size = 20px
    


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


# This is a module level helper function, not a class function
def _name_to_enum(name: str)-> Characters:
    for char in Characters:
        if char.value == name:
            return char

    raise ValueError(f"No character enum matches name '{name}'")
