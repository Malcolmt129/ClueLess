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
        suggest = json.dumps({"type": "sugggestion","person": "mustard",  "room": "bathroom","weapon": "revolver"})
        move = json.dumps({"type": "move","coordinate": 0})
        join = json.dumps({"type": "join","character": "Mrs. White"})
        disprove = json.dumps({"type": "disprove", "card": ""})
        end_turn = json.dumps({"type": "end_turn"})
        self.accusation_button = Button(self.screen, 700, button_y_coord, 400, 100, 'Accusation', lambda : self.client_socket.sendall(accuse.encode()))
        button_y_coord += 110
        self.suggestion_button = Button(self.screen, 700, button_y_coord, 400, 100, 'Suggestion', lambda : self.client_socket.sendall(suggest.encode()))
        # button_y_coord += 110
        # self.move_button = Button(self.screen, 700, button_y_coord, 400, 100, 'Move', lambda : self.client_socket.sendall(move.encode()))
        button_y_coord += 110
        self.join_button = Button(self.screen, 700, button_y_coord, 400, 100, 'Join', lambda : self.client_socket.sendall(join.encode()))    
        button_y_coord += 110    
        self.disprove_button = Button(self.screen, 700, button_y_coord, 400, 100, 'Disprove', lambda : self.client_socket.sendall(disprove.encode()))       
        button_y_coord += 110    
        self.end_turn_button = Button(self.screen, 700, button_y_coord, 400, 100, 'End Turn', lambda : self.client_socket.sendall(end_turn.encode()))  
        # self.buttons = [self.accusation_button, self.suggestion_button, self.move_button, self.join_button, self.disprove_button, self.end_turn_button]
        self.buttons = [self.accusation_button, self.suggestion_button, self.join_button, self.disprove_button, self.end_turn_button]

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

    def handle_events(self):
        try:
            response = self.client_socket.recv(1024)  # Buffer size
            if response:
                print(f"Received: {response.decode()}")
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
                        self.players[self.current_player].set_position(room.row, room.col)
                        print(f"Moved {self.players[self.current_player].name} to {room.name}")
                        move = json.dumps({"type": "move","coordinate": room.name})
                        self.client_socket.sendall(move.encode())
                        self.current_player = (self.current_player + 1) % len(self.players)
                        return

    def run(self):
        while self.running:
            self.handle_events()
            self.process_network_events()
            self.draw_board()
            self.draw_characters()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
