import constants
import pygame

class Room():

    def __init__(self, screen: pygame.Surface, name: str, location: tuple, gridLocation: tuple) -> None:
        
        self.screen = screen
        self.name = name
        self.location = location
        self.gridLocation = gridLocation 
        self.playersInroom = set() 
        self.tile_offsets = [
            (1, 1), (2, 1),
            (1, 2), (2, 2),
            (0, 0), (3, 3),  # extras in case >4
        ]
    
    def draw(self):

        font = pygame.font.Font(None, 20)  # Small font for room names

        for row in range(4):

            for column in range(4):

                pygame.draw.rect(self.screen, constants.GREY, 
                                ((row + self.location[0] ) * constants.SQUARE_SIZE, 
                                (column + self.location[1]) * constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE))
        # Calculate room label position (approx. center of first tile)
        label_x = (self.location[0] * constants.SQUARE_SIZE) + ((4 * constants.SQUARE_SIZE)) // 2
        label_y = (self.location[1] * constants.SQUARE_SIZE) + ((4 * constants.SQUARE_SIZE)) // 2

        # Draw text label for the room
        text = font.render(self.name, True, constants.BLACK)
        text_rect = text.get_rect(center=(label_x, label_y))
        self.screen.blit(text, text_rect)

    def __repr__(self) -> str:
        return f" Room: {self.name}"


#Making this distinction so it can be drawn different for the hallway
class Hallway(Room):

    def __init__(self, screen: pygame.Surface, name: str, location: tuple, gridLocation: tuple, dimensions: tuple) -> None:

        super().__init__(screen, name, location, gridLocation)
        self.dimensions = dimensions
        self.player = None
        self.occupied = False
    
    def draw(self):
        for row in range(self.dimensions[0]):

            for column in range(self.dimensions[1]):

                pygame.draw.rect(self.screen, constants.GREY, 
                                ((row + self.location[0] ) * constants.SQUARE_SIZE, 
                                (column + self.location[1]) * constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE))


class StartingPoint(Room):
    def __init__(self, screen: pygame.Surface, name: str, location: tuple[int, int], gridLocation: tuple[int,int], color):
        super().__init__(screen, name, location, gridLocation)
        self.playersInroom = set() 
        self.name = f"{name} Start"
        self.color = color 
    def draw(self):

        
                pygame.draw.rect(self.screen, self.color, 
                                ((self.location[0] ) * constants.SQUARE_SIZE, 
                                ( self.location[1]) * constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE, 
                                constants.SQUARE_SIZE))


class RoomFactory:

    @staticmethod
    def create_room(screen, name, location, gridLocation):
        return Room(screen, name, location, gridLocation) 


    @staticmethod
    def create_hallway(screen, name, location, gridLocation, dimensions):
        return Hallway(screen, name, location, gridLocation, dimensions)

    @staticmethod
    def create_startingPoint(screen, name, location, gridLocation, color):
        return StartingPoint(screen, name, location, gridLocation, color) 
