import characters
import player
import card
import random
import room
import pygame
import constants
from defaults import starting_locations, Characters, RoomPositions, RoomsToRoomPositions, Rooms   # Import character positions
from button import ButtonFactory

class Game:
    
    CHARACTERS = ["Ms. Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    ROOMS = ["KITCHEN", "BALLROOM", "CONSERVATORY", "DINING ROOM", "BILLIARD ROOM", "LIBRARY", "LOUNGE", "HALL", "STUDY"]
    

    def __init__(self, screen=None):
        
        
        # This is basically a card factory... with the three different category
        self.deck = [card.Card(name, "Character") for name in self.CHARACTERS]\
                    + [card.Card(weapon, "Weapons") for weapon in self.WEAPONS]\
                    + [card.Card(room, "Room") for room in self.ROOMS]

        self.solution = {} # I'll make a function to implement the solution before the cards are given to players.
        self.players = [] # For when the players are making accusations
        self.rooms = {} # filled in by helper function _rooms_Create()
        self.characters = {} # filled in by helper function _characters_create()
        self.background = pygame.image.load("./assets/BoardBackground.png")
        self.num_players = len(self.characters)
        self.current_player_index = 0
        self.buttons = []
        self.startingPoints = {} # filled in by helper function startingPoints_create() 
        
        

        # This if statement is to differentiate behavior for testing... if no 
        # screen is set like what would happen for testing, just quit out of the
        # surface but you can still test the class
        if screen is None:
            self.screen = pygame.display.set_mode((800, 600))
            pygame.quit()  # Close the display to prevent the screen from showing
        else:
            self.screen = screen

        self._characters_create()
        self._rooms_Create()


    def solution_Create(self):
        
        self.solution["Character"] = random.choice(self.CHARACTERS) #Select a character card for solution
        self.solution["Weapon"] = random.choice(self.WEAPONS) #Select a weapon card for solution
        self.solution["Room"] = random.choice(self.ROOMS) #Select a room card for solution
        
        #This is list comprehension, basically remove card from deck if it has been chosen for solution
        self.deck = [card for card in self.deck if card.name not in self.solution.values()]
    


    def grid_draw(self):

        for row in range(constants.ROWS):
            for col in range(row % 2, constants.ROWS, 2):
                pygame.draw.rect(self.screen, constants.WHITE, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))



    def rooms_draw(self):
        
        #self.screen.blit(self.background, (0,0))
        for instance in self.rooms.values():
            instance.draw()

            if isinstance(instance, room.Room):  # Only check for secret passages in Rooms
                secret_size = constants.SQUARE_SIZE // 2
                room_pixel_x = instance.location[0] * constants.SQUARE_SIZE
                room_pixel_y = instance.location[1] * constants.SQUARE_SIZE

                corner_rooms = {Rooms.STUDY, Rooms.LOUNGE, Rooms.CONSERVATORY, Rooms.KITCHEN}

                try:
                    uppercase_room_name = instance.name.upper()
                    room_enum = Rooms(uppercase_room_name)
                    if room_enum in corner_rooms:
                        if room_enum == Rooms.STUDY:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("KITCHEN", (0, 0, 0)), (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                        elif room_enum == Rooms.LOUNGE:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("CONSERVATORY", (0, 0, 0)), (room_pixel_x + 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                        elif room_enum == Rooms.CONSERVATORY:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("LOUNGE", (0, 0, 0)), (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 3, secret_size, secret_size))
                        elif room_enum == Rooms.KITCHEN:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("STUDY", (0, 0, 0)), (room_pixel_x + 3, room_pixel_y + 3, secret_size, secret_size))
                except ValueError:
                    pass

    def characters_draw(self):

        for character in self.characters.values():
            character.drawProto(self.rooms)
            

    def _rooms_Create(self):
        
        # List of rooms (name, location)
        room_data = [
            (Rooms.STUDY, (3,2), (1,1)),   # Study
            (Rooms.HALL, (11,2), (3,1)),   # Hall
            (Rooms.LOUNGE, (19,2), (5,1)),  # Lounge
            (Rooms.DINING_ROOM, (19,10), (5,3)),  # Dining
            (Rooms.KITCHEN, (19,18), (5,5)), # Kitchen
            (Rooms.BALLROOM, (11,18), (3,5)),  # Ballroom
            (Rooms.CONSERVATORY, (3,18), (1,5)),  # Conservatory
            (Rooms.LIBRARY, (3,10), (1,3)),   # Library
            (Rooms.BILLIARD_ROOM, (11,10), (3,3)),   # Billiard Room
        ]

        # List of hallways (name, location, gridlocation, dimensions, connections)
        hallway_data = [
            ("studyToHall", (7,3), (2,1), (4,2)),
            ("studyToLibrary", (4,6), (1,2), (2,4)),
            ("hallToLounge", (15,3), (4,1), (4,2)),
            ("loungeToDining", (20,6), (5,2), (2,4)),
            ("diningToKitchen", (20,14), (5,4), (2,4)),
            ("ballroomToKitchen", (15,19), (4,5), (4,2)),
            ("conservToBallroom", (7,19), (2,5), (4,2)),
            ("libraryTocConserv", (4,14), (1,4), (2,4)),
            ("libraryToBilliard", (7,11), (2,3), (4,2)),
            ("billiardToDining", (15,11), (4,3), (4,2)),
            ("billiardToBallroom", (12,14), (3,4), (2,4)),
            ("hallToBilliard", (12,6), (3,2), (2,4)),
        ]

        starts_data = [

            ("Ms. Scarlet", (16,2), starting_locations[Characters.SCARLET],constants.CHARACTER_COLORS["Ms. Scarlet"]),
            ("Colonel Mustard", (22,7), starting_locations[Characters.MUSTARD], constants.CHARACTER_COLORS["Colonel Mustard"]),
            ("Mrs. White", (17, 21), starting_locations[Characters.WHITE], constants.CHARACTER_COLORS["Mrs. White"]),
            ("Mr. Green", (9,21), starting_locations[Characters.GREEN], constants.CHARACTER_COLORS["Mr. Green"]),
            ("Mrs. Peacock",(3,16), starting_locations[Characters.PEACOCK],constants.CHARACTER_COLORS["Mrs. Peacock"]),
            ("Professor Plum", (3,8), starting_locations[Characters.PLUM],constants.CHARACTER_COLORS["Professor Plum"]),
        ]

        # Create and add rooms
        for name, location, gridlocation in room_data:
            self.rooms[name] = room.RoomFactory.create_room(self.screen, name, location, gridlocation)

        # Create and add hallways
        for name, location, gridlocation, dimensions in hallway_data:
            self.rooms[name] = room.RoomFactory.create_hallway(self.screen, name, location, gridlocation, dimensions)
        
        for name, location, gridlocation, color in starts_data:
            self.rooms[name] = room.RoomFactory.create_startingPoint(self.screen, name, location, gridlocation, color)
    
    def _characters_create(self):
        

        character_list = [
            ("Ms. Scarlet", starting_locations[Characters.SCARLET],constants.CHARACTER_COLORS["Ms. Scarlet"]),
            ("Colonel Mustard", starting_locations[Characters.MUSTARD], constants.CHARACTER_COLORS["Colonel Mustard"]),
            ("Mrs. White", starting_locations[Characters.WHITE], constants.CHARACTER_COLORS["Mrs. White"]),
            ("Mr. Green", starting_locations[Characters.GREEN], constants.CHARACTER_COLORS["Mr. Green"]),
            ("Mrs. Peacock", starting_locations[Characters.PEACOCK], constants.CHARACTER_COLORS["Mrs. Peacock"]),
            ("Professor Plum", starting_locations[Characters.PLUM], constants.CHARACTER_COLORS["Professor Plum"]),

        ]

        for name, startPlace, color in character_list:
            self.characters[name] = characters.CharacterFactory.create_Character(self.screen, name, startPlace, color)


        for charact in self.characters.values():
            self.players.append(charact.name)

    def move_character(self, direction: str, character_index: int = 0):
        """Move a specific character based on their index."""

        key = list(self.characters.keys())[character_index]
        if 0 <= character_index < len(self.characters):
            ret = self.characters[key].move(direction)
            if self.num_players > 0:
                self._next_turn()
        # Move to the next player's turn
        else:
            print("It's not your turn!")
        
        return ret
    def _next_turn(self):
        """Switch to the next player's turn."""
        if self.num_players > 0:  # Ensure there are players
            self.current_player_index = (self.current_player_index + 1) % self.num_players
            print(f"It's now {self.characters[self.current_player_index].name}'s turn!")

        else:
            print("No players to switch turns!")


    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel positions."""
        cell_size = 80  # Adjust based on board size
        offset_x, offset_y = 40, 40  # Center characters in cells
        return (grid_x * cell_size + offset_x, grid_y * cell_size + offset_y)
    
