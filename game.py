import characters
import player
import card
import random

class Game:
    
    CHARACTERS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]
    

    def __init__(self):
        
        # Need to make sure that we add the ability to keep track of real players
        
        # This is basically a card factory... with the three different category
        self.deck = [card.Card(name, "Character") for name in self.CHARACTERS]\
                    + [card.Card(weapon, "Weapons") for weapon in self.WEAPONS]\
                    + [card.Card(room, "Room") for room in self.ROOMS]


        self.solution = {} # I'll make a function to implement the solution before the cards are given to players.
        self.board = {} # Have to provide a way to represent the board well, with the rooms and the spaces between
        self.current_turn = {} # For determining whos turn it is maybe?
        self.playerSeq = {} # For when the players are making accusations
        
    def solutionCreate(self):
        
        self.solution["Character"] = random.choice(self.CHARACTERS) #Select a character card for solution
        self.solution["Weapon"] = random.choice(self.WEAPONS) #Select a weapon card for solution
        self.solution["Room"] = random.choice(self.ROOMS) #Select a room card for solution
        
        #This is list comprehension, basically remove card from deck if it has been chosen for solution
        self.deck = [card for card in self.deck if card.name not in self.solution.values()]

