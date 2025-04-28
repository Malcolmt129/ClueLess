import characters
import player
import card
import random
import room
import pygame
import constants
from defaults import starting_locations, Characters, Weapons, RoomPositions, RoomsToRoomPositions, Rooms   # Import character positions
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Game:
    
    def __init__(self, screen=None, custom_names=None):
        # Create bidirectional mappings between enums and custom names
        self.CHARACTERS = {}  # enum -> custom name
        self.CHARACTERS_REVERSE = {}  # custom name -> enum
        self.WEAPONS = {}
        self.WEAPONS_REVERSE = {}
        self.ROOMS = {}
        self.ROOMS_REVERSE = {}
        
        # Initialize with custom names if provided, otherwise use defaults
        if custom_names and 'characters' in custom_names:
            for enum_char, custom_name in zip(Characters, custom_names['characters']):
                self.CHARACTERS[enum_char] = custom_name
                self.CHARACTERS_REVERSE[custom_name] = enum_char
            # Set up custom names in the characters module
            characters.set_custom_names(custom_names)
        else:
            for enum_char in Characters:
                self.CHARACTERS[enum_char] = enum_char.value
                self.CHARACTERS_REVERSE[enum_char.value] = enum_char

        if custom_names and 'weapons' in custom_names:
            for enum_weapon, custom_name in zip(Weapons, custom_names['weapons']):
                self.WEAPONS[enum_weapon] = custom_name
                self.WEAPONS_REVERSE[custom_name] = enum_weapon
        else:
            for enum_weapon in Weapons:
                self.WEAPONS[enum_weapon] = enum_weapon.value
                self.WEAPONS_REVERSE[enum_weapon.value] = enum_weapon

        if custom_names and 'rooms' in custom_names:
            for enum_room, custom_name in zip(Rooms, custom_names['rooms']):
                self.ROOMS[enum_room] = custom_name
                self.ROOMS_REVERSE[custom_name] = enum_room
        else:
            for enum_room in Rooms:
                self.ROOMS[enum_room] = enum_room.value
                self.ROOMS_REVERSE[enum_room.value] = enum_room

        # Create deck using custom names
        self.deck = [card.Card(self.CHARACTERS[char], "Character") for char in Characters] + \
                   [card.Card(self.WEAPONS[weapon], "Weapons") for weapon in Weapons] + \
                   [card.Card(self.ROOMS[room], "Room") for room in Rooms]

        self.solution = {}
        self.players = []
        self.rooms = {}
        self.characters = {}  # Will store Character objects by enum
        self.characters_by_name = {}  # Will store Character objects by custom name
        self.background = pygame.image.load("./assets/BoardBackground.png")
        self.num_players = len(self.characters)
        self.current_player_index = 0
        self.buttons = []
        self.startingPoints = {}

        if screen is None:
            self.screen = pygame.display.set_mode((800, 600))
            pygame.quit()
        else:
            self.screen = screen

        self._characters_create()
        self._rooms_Create()

    def solution_Create(self):
        # Select random enums for solution
        char_enum = random.choice(list(Characters))
        weapon_enum = random.choice(list(Weapons))
        room_enum = random.choice(list(Rooms))
        
        # Store custom names in solution
        self.solution["Character"] = self.CHARACTERS[char_enum]
        self.solution["Weapon"] = self.WEAPONS[weapon_enum]
        self.solution["Room"] = self.ROOMS[room_enum]
        
        # Remove cards from deck using custom names
        self.deck = [card for card in self.deck if card.name not in self.solution.values()]

    def grid_draw(self):

        for row in range(constants.ROWS):
            for col in range(row % 2, constants.ROWS, 2):
                pygame.draw.rect(self.screen, constants.WHITE, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))



    def rooms_draw(self):
        
        #self.screen.blit(self.background, (0,0))
        for room_key, instance in self.rooms.items():
            instance.draw()

            if isinstance(instance, room.Room):  # Only check for secret passages in Rooms
                secret_size = constants.SQUARE_SIZE // 2
                room_pixel_x = instance.location[0] * constants.SQUARE_SIZE
                room_pixel_y = instance.location[1] * constants.SQUARE_SIZE

                corner_rooms = {Rooms.STUDY, Rooms.LOUNGE, Rooms.CONSERVATORY, Rooms.KITCHEN}

                if isinstance(room_key, Rooms) and room_key in corner_rooms:
                    if room_key == Rooms.STUDY:
                        pygame.draw.rect(self.screen, constants.ROOM_COLORS.get(self.ROOMS[Rooms.KITCHEN].upper(), (0, 0, 0)), 
                                      (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                    elif room_key == Rooms.LOUNGE:
                        pygame.draw.rect(self.screen, constants.ROOM_COLORS.get(self.ROOMS[Rooms.CONSERVATORY].upper(), (0, 0, 0)), 
                                      (room_pixel_x + 3, room_pixel_y + 4 * constants.SQUARE_SIZE - secret_size - 3, secret_size, secret_size))
                    elif room_key == Rooms.CONSERVATORY:
                        pygame.draw.rect(self.screen, constants.ROOM_COLORS.get(self.ROOMS[Rooms.LOUNGE].upper(), (0, 0, 0)), 
                                      (room_pixel_x + 4 * constants.SQUARE_SIZE - secret_size - 3, room_pixel_y + 3, secret_size, secret_size))
                    elif room_key == Rooms.KITCHEN:
                        pygame.draw.rect(self.screen, constants.ROOM_COLORS.get(self.ROOMS[Rooms.STUDY].upper(), (0, 0, 0)), 
                                      (room_pixel_x + 3, room_pixel_y + 3, secret_size, secret_size))

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

        # Create and add rooms
        for room_enum, location, gridlocation in room_data:
            # Use custom name from the mapping
            room_name = self.ROOMS[room_enum]
            self.rooms[room_enum] = room.RoomFactory.create_room(self.screen, room_name, location, gridlocation)

        # List of hallways (name, location, gridlocation, dimensions)
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

        # Update starting points with custom names
        starts_data = [
            (Characters.SCARLET, (16,2), starting_locations[Characters.SCARLET], constants.CHARACTER_COLORS["Miss Scarlet"]),
            (Characters.MUSTARD, (22,7), starting_locations[Characters.MUSTARD], constants.CHARACTER_COLORS["Colonel Mustard"]),
            (Characters.WHITE, (17, 21), starting_locations[Characters.WHITE], constants.CHARACTER_COLORS["Mrs. White"]),
            (Characters.GREEN, (9,21), starting_locations[Characters.GREEN], constants.CHARACTER_COLORS["Mr. Green"]),
            (Characters.PEACOCK, (3,16), starting_locations[Characters.PEACOCK], constants.CHARACTER_COLORS["Mrs. Peacock"]),
            (Characters.PLUM, (3,8), starting_locations[Characters.PLUM], constants.CHARACTER_COLORS["Professor Plum"]),
        ]
        
        for char_enum, location, gridlocation, color in starts_data:
            char_name = self.CHARACTERS[char_enum]
            self.rooms[char_enum] = room.RoomFactory.create_startingPoint(self.screen, char_name, location, gridlocation, color)
    
    def _characters_create(self):
        character_list = [
            (Characters.SCARLET, self.CHARACTERS[Characters.SCARLET], starting_locations[Characters.SCARLET], constants.CHARACTER_COLORS["Miss Scarlet"]),
            (Characters.MUSTARD, self.CHARACTERS[Characters.MUSTARD], starting_locations[Characters.MUSTARD], constants.CHARACTER_COLORS["Colonel Mustard"]),
            (Characters.WHITE, self.CHARACTERS[Characters.WHITE], starting_locations[Characters.WHITE], constants.CHARACTER_COLORS["Mrs. White"]),
            (Characters.GREEN, self.CHARACTERS[Characters.GREEN], starting_locations[Characters.GREEN], constants.CHARACTER_COLORS["Mr. Green"]),
            (Characters.PEACOCK, self.CHARACTERS[Characters.PEACOCK], starting_locations[Characters.PEACOCK], constants.CHARACTER_COLORS["Mrs. Peacock"]),
            (Characters.PLUM, self.CHARACTERS[Characters.PLUM], starting_locations[Characters.PLUM], constants.CHARACTER_COLORS["Professor Plum"]),
        ]

        for enum_char, name, startPlace, color in character_list:
            character = characters.CharacterFactory.create_Character(self.screen, name, startPlace, color)
            self.characters[enum_char] = character  # Store by enum
            self.characters_by_name[name] = character  # Store by custom name
            self.players.append(name)

    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel positions."""
        cell_size = 80  # Adjust based on board size
        offset_x, offset_y = 40, 40  # Center characters in cells
        return (grid_x * cell_size + offset_x, grid_y * cell_size + offset_y)
    
