import characters
import player
import card
import random
import room
import pygame
import constants
from defaults import starting_locations, Characters, RoomPositions, RoomsToRoomPositions, Rooms  # Import character positions
from button import ButtonFactory

class Game:

    CHARACTERS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    ROOMS = ["KITCHEN", "BALLROOM", "CONSERVATORY", "DINING ROOM", "BILLARD ROOM", "LIBRARY", "LOUNGE", "HALL", "STUDY"]


    def __init__(self, screen=None):


        # This is basically a card factory... with the three different category
        self.deck = [card.Card(name, "Character") for name in self.CHARACTERS]\
                    + [card.Card(weapon, "Weapons") for weapon in self.WEAPONS]\
                    + [card.Card(room, "Room") for room in self.ROOMS]

        self.solution = {} # I'll make a function to implement the solution before the cards are given to players.
        self.playerSeq = {} # For when the players are making accusations
        self.rooms = [] # filled in by helper function _rooms_Create()
        self.characters = [] # filled in by helper function _characters_create()
        self.background = pygame.image.load("./assets/BoardBackground.png")
        self.num_players = len(self.characters)
        self.current_player_index = 0
        self.buttons = []

        #Need to find a way to store the players


        # Need to make sure that we add the ability to keep track of real players


        # This if statement is to differentiate behavior for testing... if no
        # screen is set like what would happen for testing, just quit out of the
        # surface but you can still test the class
        if screen is None:
            self.screen = pygame.display.set_mode((800, 600))
            pygame.quit()  # Close the display to prevent the screen from showing
        else:
            self.screen = screen

        self._rooms_Create()
        self._characters_create()

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
        font = pygame.font.Font(None, 20)  # Small font for room names

        #self.screen.blit(self.background, (0, 0))
        for instance in self.rooms:

            if type(instance) == room.Room:
                room_color = constants.ROOM_COLORS.get(instance.name.upper(), constants.GREY)
                room_rect = pygame.Rect(
                    instance.location[0] * constants.SQUARE_SIZE,
                    instance.location[1] * constants.SQUARE_SIZE,
                    4 * constants.SQUARE_SIZE, 
                    4 * constants.SQUARE_SIZE
                )
                pygame.draw.rect(self.screen, room_color, room_rect)

                # Calculate room label position
                label_x = room_rect.centerx
                label_y = room_rect.centery
                text = font.render(instance.name, True, constants.BLACK)
                text_rect = text.get_rect(center=(label_x, label_y))
                self.screen.blit(text, text_rect)

                # Draw small shaded squares for secret passages in the four corner rooms
                secret_size = constants.SQUARE_SIZE // 2

                corner_rooms = {Rooms.STUDY, Rooms.LOUNGE, Rooms.CONSERVATORY, Rooms.KITCHEN}

                try:
                    uppercase_room_name = instance.name.upper()
                    print(f"Trying to create enum for: '{uppercase_room_name}'") # DEBUG
                    room_enum = Rooms(uppercase_room_name)
                    print(f"Successfully created enum: {room_enum}") # DEBUG
                    if room_enum in corner_rooms:
                        print(f"  {room_enum} is a corner room at location: {instance.location}") # DEBUG
                        room_pixel_x = instance.location[0] * constants.SQUARE_SIZE
                        room_pixel_y = instance.location[1] * constants.SQUARE_SIZE

                        if room_enum == Rooms.STUDY:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("KITCHEN", (0, 0, 0)), (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                        elif room_enum == Rooms.LOUNGE:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("CONSERVATORY", (0, 0, 0)), (room_pixel_x + 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                        elif room_enum == Rooms.CONSERVATORY:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("LOUNGE", (0, 0, 0)), (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 3, secret_size, secret_size))
                        elif room_enum == Rooms.KITCHEN:
                            pygame.draw.rect(self.screen, constants.ROOM_COLORS.get("STUDY", (0, 0, 0)), (room_pixel_x + 3, room_pixel_y + 3, secret_size, secret_size))
                except ValueError:
                    print(f"ValueError for room: {instance.name.upper()}") # DEBUG
                    pass

            elif type(instance) == room.Hallway:
                for row in range(instance.dimensions[0]):
                    for column in range(instance.dimensions[1]):
                        pygame.draw.rect(self.screen, constants.GREY,
                                         ((row + instance.location[0]) * constants.SQUARE_SIZE,
                                          (column + instance.location[1]) * constants.SQUARE_SIZE,
                                          constants.SQUARE_SIZE,
                                          constants.SQUARE_SIZE))
                        
    def startingPoints_draw(self):
        pass

    def _rooms_Create(self):

        # List of rooms (name, location)
        room_data = [
            (self.ROOMS[8], (3,2), [self.ROOMS[0],"studyToHall", "studyToLibrary"]),   # Study
            (self.ROOMS[7], (11,2), ["studyToHall", "hallToLounge"]),   # Hall
            (self.ROOMS[6], (19,2), [self.ROOMS[2], "hallToLounge", "loungeToDining"]),  # Lounge
            (self.ROOMS[3], (19,10), ["billiardToDining", "loungeToDining", "diningToKitchen"]),  # Dining
            (self.ROOMS[0], (19,18), [self.ROOMS[8], "diningToKitchen", "ballroomToKitchen"]), # Kitchen
            (self.ROOMS[1], (11,18), ["billiardToBallroom", "conservToBallroom", "ballroomToKitchen"]),   # Ballroom
            (self.ROOMS[2], (3,18), [self.ROOMS[6], "conservToBallroom", "libraryTocConserv"]),  # Conservatory
            (self.ROOMS[5], (3,10), ["libraryTocConserv", "libraryToBilliard", "studyToLibrary"]),    # Library
            (self.ROOMS[4], (11,10), ["billiardToBallroom", "billiardToDining", "libraryToBilliard","hallToBilliard"]),    # Billiard Room
        ]

        # List of hallways (name, location, dimensions)
        hallway_data = [
            ("studyToHall", (7,3), (4,2), [self.ROOMS[8], self.ROOMS[7]]),
            ("studyToLibrary", (4,6), (2,4), [self.ROOMS[8], self.ROOMS[5]]),
            ("hallToLounge", (15,3), (4,2), [self.ROOMS[7], self.ROOMS[6]]),
            ("loungeToDining", (20,6), (2,4), [self.ROOMS[6], self.ROOMS[3]]),
            ("diningToKitchen", (20,14), (2,4), [self.ROOMS[3], self.ROOMS[0]]),
            ("ballroomToKitchen", (15,19), (4,2), [self.ROOMS[1], self.ROOMS[0]]),
            ("conservToBallroom", (7,19), (4,2), [self.ROOMS[2], self.ROOMS[1]]),
            ("libraryTocConserv", (4,14), (2,4), [self.ROOMS[5], self.ROOMS[2]]),
            ("libraryToBilliard", (7,11), (4,2), [self.ROOMS[5], self.ROOMS[4]]),
            ("billiardToDining", (15,11), (4,2), [self.ROOMS[4], self.ROOMS[3]]),
            ("billiardToBallroom", (12,14), (2,4), [self.ROOMS[4], self.ROOMS[1]]),
            ("hallToBilliard", (12,6), (2,4), [self.ROOMS[7], self.ROOMS[4]]),
        ]

        # Create and add rooms
        for name, location, connections in room_data:
            self.rooms.append(room.RoomFactory.create_room(name, location, connections))

        # Create and add hallways
        for name, location, dimensions, connections in hallway_data:
            self.rooms.append(room.RoomFactory.create_hallway(name, location, dimensions, connections))

    def _characters_create(self):
        """Assign characters to their starting locations, avoiding duplicates."""
        self.characters = []  # Clear list to avoid duplicates
        seen = set()

        for character, (grid_x, grid_y) in starting_locations.items():
            if character.value not in seen and grid_x >= 0:
                seen.add(character.value)
                pixel_x, pixel_y = self.grid_to_pixel(grid_x, grid_y)
                self.characters.append(characters.Character(character.value, (pixel_x, pixel_y), constants.CHARACTER_COLORS[character.value]))

        self.players = self.characters  # Assign players correctly
        self.num_players = len(self.players)
        self.current_player_index = 0  # Start with Player 1

        print(f"Characters: {[char.name for char in self.characters]}")  # Debugging output


    def move_character(self, direction: str, character_index: int = 0):
        """Move a specific character based on their index."""
        if 0 <= character_index < len(self.characters):
            self.characters[character_index].move(direction)
            if self.num_players > 0:
                self._next_turn()
# Move to the next player's turn
        else:
            print("It's not your turn!")

    def _next_turn(self):
        """Switch to the next player's turn."""
        if self.num_players > 0:  # Ensure there are players
            self.current_player_index = (self.current_player_index + 1) % self.num_players
            print(f"It's now {self.characters[self.current_player_index].name}'s turn!")

        else:
            print("No players to switch turns!")


    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel positions."""
        cell_size = constants.SQUARE_SIZE # Use the defined square size
        offset_x, offset_y = cell_size // 2, cell_size // 2  # Center characters in cells
        return (grid_x * cell_size + offset_x, grid_y * cell_size + offset_y)

    def draw_characters(self):
        for character in self.characters:
            pygame.draw.circle(self.screen, character.color, character.startingPos, 20)  # Token size = 20px