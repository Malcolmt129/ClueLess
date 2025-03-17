from board import Board
from characters import characters
from turnInterface import TurnInterface
import player
import card
import random
from constants import ROOM_SIZE, HALLWAY_SIZE 
import pygame
import json
import socket



class Game:
    
    CHARACTERS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]
    

    def __init__(self, window=None):
        
        # Need to make sure that we add the ability to keep track of real players
        
        # This is basically a card factory... with the three different category
        self.deck = [card.Card(name, "Character") for name in self.CHARACTERS]\
                    + [card.Card(weapon, "Weapons") for weapon in self.WEAPONS]\
                    + [card.Card(room, "Room") for room in self.ROOMS]



        self.solution = {} # I'll make a function to implement the solution before the cards are given to players.
        self.board = Board() # Have to provide a way to represent the board well, with the rooms and the spaces between
        self.current_player = 0 # For determining whos turn it is maybe?
        self.players = [player.Player(name) for name in characters] # For when the players are making accusations
        self.rooms = []
        self.turn_interface = TurnInterface() 


        if window is None:
            self.window = pygame.display.set_mode((800,800))
            pygame.quit()

        else:
            self.window = window



        # Start client connection
        server_address = '127.0.0.1'  # Replace with the server's IP address
        server_port = 12345           # Replace with the server's port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))
        self.client_socket.setblocking(False)
        print(f"Connected to {server_address}:{server_port}")

    def solutionCreate(self):
        
        self.solution["Character"] = random.choice(self.CHARACTERS) #Select a character card for solution
        self.solution["Weapon"] = random.choice(self.WEAPONS) #Select a weapon card for solution
        self.solution["Room"] = random.choice(self.ROOMS) #Select a room card for solution
        
        #This is list comprehension, basically remove card from deck if it has been chosen for solution
        self.deck = [card for card in self.deck if card.name not in self.solution.values()]

    def handle_events(self):
        try:
            response = self.client_socket.recv(1024)  # Buffer size
            if response:
                print(f"Received: {response.decode()}")

                # if move
                message = json.loads(response.decode())
                message_type = message.get("type")
                if(message_type=="move_response"):
                    row, col = message.get("row"), message.get("col")
                    self.players[self.current_player].set_position(row, col)
                    self.current_player = (self.current_player + 1) % len(self.players)    
        except BlockingIOError:
            # No data available to read yet
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                if self.current_player >= len(self.players):
                    return

                for room in self.rooms:
                    room_x = room.col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    room_y = room.row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    if room_x <= x <= room_x + ROOM_SIZE and room_y <= y <= room_y + ROOM_SIZE:
                        # self.players[self.current_player].set_position(room.row, room.col)
                        print(f"Trying to move {self.players[self.current_player].name} to {room.name}")
                        move = json.dumps({"type": "move","coordinate": room.name, "row": room.row, "col": room.col})
                        self.client_socket.sendall(move.encode())
                        # self.current_player = (self.current_player + 1) % len(self.players)
                        return
