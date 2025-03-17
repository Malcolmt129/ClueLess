import pygame
from player import Player
from characters import characters
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ROOM_SIZE, HALLWAY_SIZE,
                       GRID_ROWS, GRID_COLS, WHITE, BLACK, HALLWAY_COLOR)
from room import create_rooms
from button import Button
import socket
import select
import json

class Board:
    

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Clue-Less Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Start client connection
        server_address = '127.0.0.1'  # Replace with the server's IP address
        server_port = 12345           # Replace with the server's port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))
        self.client_socket.setblocking(False)
        print(f"Connected to {server_address}:{server_port}")

        # Initialize rooms
        self.rooms = create_rooms()

        # Initialize players
        self.players = [Player(name) for name in characters]
        for player in self.players:
            player.set_position(0, 0)

        self.current_player = 0         
        button_y_coord = 30        
        accuse = json.dumps({"type": "accusation", "person": "mustard", "room": "bathroom","weapon": "revolver"})
        suggest = json.dumps({"type": "suggestion","person": "mustard",  "room": "bathroom","weapon": "revolver"})
        move = json.dumps({"type": "move","coordinate": 0})
        join = json.dumps({"type": "join","character": "Mrs. White"})
        disprove = json.dumps({"type": "disprove", "card": ""})
        end_turn = json.dumps({"type": "end_turn"})

    def draw_board(self):
        self.screen.fill(WHITE)

        for room in self.rooms:
            x = room.col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            y = room.row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE

            pygame.draw.rect(self.screen, room.color, (x, y, ROOM_SIZE, ROOM_SIZE))
            pygame.draw.rect(self.screen, BLACK, (x, y, ROOM_SIZE, ROOM_SIZE), 2)

            font = pygame.font.Font(None, 24)
            room_text = font.render(room.name, True, BLACK)
            self.screen.blit(room_text, (x + ROOM_SIZE // 4, y + ROOM_SIZE // 3))

        for button in self.buttons:
            button.process()

        # Draw hallways
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE

                if col < GRID_COLS - 1:  
                    hallway_x = x + ROOM_SIZE
                    pygame.draw.rect(self.screen, HALLWAY_COLOR, (hallway_x, y + (ROOM_SIZE // 4), HALLWAY_SIZE, ROOM_SIZE // 2))

                if row < GRID_ROWS - 1:  
                    hallway_y = y + ROOM_SIZE
                    pygame.draw.rect(self.screen, HALLWAY_COLOR, (x + (ROOM_SIZE // 4), hallway_y, ROOM_SIZE // 2, HALLWAY_SIZE))

    def draw_characters(self):
        for player in self.players:
            row, col = player.get_position() 
            x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
            y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
            pygame.draw.circle(self.screen, BLACK, (x, y), 15)

            font = pygame.font.Font(None, 24)
            text = font.render(player.name, True, BLACK)
            self.screen.blit(text, (x - text.get_width() // 2, y + 20))

