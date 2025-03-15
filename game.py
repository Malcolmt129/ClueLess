import characters
import player
import card
import random
import room
import pygame
import constants


class Game:
    
    CHARACTERS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    ROOMS = ["KITCHEN", "BALLROOM", "CONSERVATORY", "DINING ROOM", "BILLIARD ROOM", "LIBRARY", "LOUNGE", "HALL", "STUDY"]
    

    def __init__(self, window=None):
        
        
        # This is basically a card factory... with the three different category
        self.deck = [card.Card(name, "Character") for name in self.CHARACTERS]\
                    + [card.Card(weapon, "Weapons") for weapon in self.WEAPONS]\
                    + [card.Card(room, "Room") for room in self.ROOMS]

        self.solution = {} # I'll make a function to implement the solution before the cards are given to players.
        self.playerSeq = {} # For when the players are making accusations
        self.rooms = [] # filled in by helper function _rooms_Create()
        self.characters = [] # filled in by helper function _characters_create()
        #Need to find a way to store the players 
        
        # Need to make sure that we add the ability to keep track of real players
        

        # This if statement is to differentiate behavior for testing... if no 
        # window is set like what would happen for testing, just quit out of the
        # surface but you can still test the class
        if window is None:
            self.window = pygame.display.set_mode((800, 600))
            pygame.quit()  # Close the display to prevent the window from showing
        else:
            self.window = window

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
                    pygame.draw.rect(self.window, constants.WHITE, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

    def doorways_draw(self):

        for room in self.rooms: 
            for row in range(constants.ROWS):
                for col in range(constants.COLS):
                    
                    if (row, col) in room.doorways:

                        pygame.draw.rect(self.window, constants.SPRING_GREEN, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))



    def rooms_draw(self):
        font = pygame.font.Font(None, 24)  # Small font for room names
        

        for room in self.rooms:
            for row in range(room.dimensions[0]):

                for column in range(room.dimensions[1]):
                    
                    if (row,column) in room.omissions:
                        continue
                    pygame.draw.rect(self.window, constants.GREY, 
                                    ((row + room.location[0]) * constants.SQUARE_SIZE, 
                                     (column + room.location[1]) * constants.SQUARE_SIZE, 
                                    constants.SQUARE_SIZE, 
                                    constants.SQUARE_SIZE))
            # Calculate room label position (approx. center of first tile)
            label_x = ((room.location[0] * constants.SQUARE_SIZE)) + ((room.dimensions[0] - 1) * constants.SQUARE_SIZE   // 2)
            label_y = ((room.location[1] * constants.SQUARE_SIZE)) + ((room.dimensions[1] - 1)* constants.SQUARE_SIZE   // 2)

            # Draw text label for the room
            text = font.render(room.name, True, constants.BLACK)
            text_rect = text.get_rect(center=(label_x, label_y))
            self.window.blit(text, text_rect)
    
    def startingPoints_draw(self):
        pass

    def _rooms_Create(self):
         
        kitchen = room.Room(self.ROOMS[0], (0,1), (6,6), [(0,5)],[(4,7)])
        self.rooms.append(kitchen)

        dining = room.Room(self.ROOMS[3], (0,9), (8,7), [(7,0), (6,0), (5,0)], [(6,18), (8,12)])
        self.rooms.append(dining)                                             
        
        ballroom = room.Room(self.ROOMS[1], (8,1), (8,7),[(0,0),(1,0),(6,0),(7,0)], [(7,5), (9,8),(14,8), (16,5)]) 
        self.rooms.append(ballroom)

        conserv = room.Room(self.ROOMS[2], (18,1), (6,5), [(0,4), (5,4)], [(18,5)]) 
        self.rooms.append(conserv)

        billiard = room.Room(self.ROOMS[4], (18,8), (6,5), [], [(17,9),(22,13)]) 
        self.rooms.append(billiard)


        library = room.Room(self.ROOMS[5], (17,14), (7,5), [(0,0), (6,0), (0,4),(6,4)], [(20,13), (16,16)]) 
        self.rooms.append(library)


        study = room.Room(self.ROOMS[8], (17,21), (7,4),[(0,3)], [(17,20)]) 
        self.rooms.append(study)

        hall = room.Room(self.ROOMS[7], (9,18), (6,7), [], [(15,20), (12,17), (11,17)]) 
        self.rooms.append(hall)

        lounge = room.Room(self.ROOMS[6], (0,19), (7,6), [(6,5)], [(6,16)]) 
        self.rooms.append(lounge)

        centerRoom = room.Room("Center Room", (10,10), (5,7), [], []) 
        self.rooms.append(centerRoom)

    def _characters_create(self):
    
        scarlet = characters.Character("Miss Scarlet",(8,24), constants.CHARACTER_COLORS["Miss Scarlet"])
        self.characters.append(scarlet)

        mustard = characters.Character("Colonel Mustard", (0,17) , constants.CHARACTER_COLORS["Colonel Mustard"])
        self.characters.append(mustard)

        mWhite = characters.Character("Mrs. White", (10,0), constants.CHARACTER_COLORS["Mrs. White"])
        self.characters.append(mWhite)

        mGreen = characters.Character("Mr. Green", (10,0), constants.CHARACTER_COLORS["Mr. Green"])
        self.characters.append(mGreen)

        mPeacock = characters.Character("Mrs. Peacock", (10,0), constants.CHARACTER_COLORS["Mrs. Peacock"])
        self.characters.append(mPeacock)

        pPlum = characters.Character("Professor Plum", (10,0), constants.CHARACTER_COLORS["Professor Plum"])
        self.characters.append(pPlum)
