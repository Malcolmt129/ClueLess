import pygame
from player import Player
from characters import characters
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ROOM_SIZE, HALLWAY_SIZE,
                       GRID_ROWS, GRID_COLS, WHITE, BLACK, HALLWAY_COLOR)
from room import create_rooms

class Board:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Clue-Less Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize rooms
        self.rooms = create_rooms()

        # Initialize players
        self.players = [Player(name) for name in characters]
        for player in self.players:
            player.set_position(0, 0)

        self.current_player = 0  

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

                        self.current_player = (self.current_player + 1) % len(self.players)
                        return

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            self.draw_characters()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
