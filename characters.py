from constants import SQUARE_SIZE
from defaults import Characters, RoomPositions, RoomPositionsToRooms, starting_locations, valid_moves, hallways
import pygame

import room
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
        return (position[0] * SQUARE_SIZE, position[1] * SQUARE_SIZE)
       

    def draw(self):

            if self.position == self.startingPos:  
                pygame.draw.circle(self.screen, self.color, self.positionConversion(self.startingPos), 20)  # Token size = 20px
            # This means that the player has moved before and any movement now needs to be converted
            # to an area of a particular room.
            else:
                pygame.draw.circle(self.screen, self.color, self.pixel_position, 20)
                # Use the postion given by the room to draw the player.
    

    def drawProto(self, rooms):
        
        try:

            currentRoomName = self.getRoomKey()
            pygame.draw.circle(self.screen, self.color, self.positionConversion(rooms[currentRoomName].location), 20)  # Token size = 20px

        except ValueError:
            

            if self.position in hallways:
                
                for room in rooms.values():

                    if self.position == room.location:
                        currentRoomName = room.name 
                        pygame.draw.circle(self.screen, self.color, self.positionConversion(rooms[currentRoomName].location), 20)  # Token size = 20px

   



    def getRoomKey(self):

        if self.position == self.startingPos:

            for char_enum, start_pos in starting_locations.items():

                if self.position == start_pos:
                    return char_enum.value

        else:
            room_pos = RoomPositions(self.position)
            return RoomPositionsToRooms(room_pos)


    def move(self, direction: str):
        x,y = self.position


        if self.position == self.startingPos:
            self.position = valid_moves[self.startingPos]
            
        if direction == "UP":
            if self.position == self.startingPos:
                self.position = valid_moves[self.startingPos]
            self.position = (x, y - 1)
        
        elif direction == "DOWN":
            
            if self.position == self.startingPos:
                self.position = valid_moves[self.startingPos]

            self.position = ( x, y + 1 )
            

        elif direction == "LEFT":
            
            if self.position == self.startingPos:
                self.position = valid_moves[self.startingPos]

            self.position = (x - 1, y)
        
        elif direction == "RIGHT":
            if self.position == self.startingPos:
                self.position = valid_moves[self.startingPos]

            self.position = (x + 1, y)
        
        return self.position



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
