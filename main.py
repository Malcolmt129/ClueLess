from player import Player
from characters import characters
import pygame
import sys


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROOM_SIZE = 150
HALLWAY_SIZE = 50
GRID_ROWS = 3
GRID_COLS = 3
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HALLWAY_COLOR = (169, 169, 169)

room_colors = [
    (255, 182, 193), (255, 223, 186), (224, 255, 255),
    (255, 239, 186), (204, 255, 204), (255, 224, 178),
    (255, 240, 245), (255, 255, 204), (224, 204, 255),
]

room_names = [
    "Kitchen", "Ballroom", "Conservatory",
    "Dining Room", "Library", "Billiard Room",
    "Lounge", "Hall", "Study"
]

game_players = [Player(name) for name in characters]

# Set all players to start in the top-left room (0,0)
for player in game_players:
    player.set_position(0, 0)

player_positions = {player.name: player for player in game_players}
current_player = 0 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clue-Less Game")
clock = pygame.time.Clock()

def draw_board():
    screen.fill(WHITE)
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            
            pygame.draw.rect(screen, room_colors[row * 3 + col], (x, y, ROOM_SIZE, ROOM_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, ROOM_SIZE, ROOM_SIZE), 2)

            font = pygame.font.Font(None, 24)
            room_text = font.render(room_names[row * 3 + col], True, BLACK)
            screen.blit(room_text, (x + ROOM_SIZE // 4, y + ROOM_SIZE // 3))

    # Draw hallways
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE

            if col < GRID_COLS - 1:  
                hallway_x = x + ROOM_SIZE
                hallway_y = y + (ROOM_SIZE // 4)
                pygame.draw.rect(screen, HALLWAY_COLOR, (hallway_x, y + (ROOM_SIZE // 4), HALLWAY_SIZE, ROOM_SIZE // 2))

            if row < GRID_ROWS - 1:  
                hallway_x = x + (ROOM_SIZE // 4)
                hallway_y = y + ROOM_SIZE
                pygame.draw.rect(screen, HALLWAY_COLOR, (x + (ROOM_SIZE // 4), hallway_y, ROOM_SIZE // 2, HALLWAY_SIZE))

def draw_characters():
    for player in game_players:
        row, col = player.get_position() 
        x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
        y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
        pygame.draw.circle(screen, BLACK, (x, y), 15)

        font = pygame.font.Font(None, 24)
        text = font.render(player.name, True, BLACK)
        screen.blit(text, (x - text.get_width() // 2, y + 20))

def handle_events():
    global current_player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            if current_player >= len(game_players):
                return True

            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    room_x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    room_y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    if room_x <= x <= room_x + ROOM_SIZE and room_y <= y <= room_y + ROOM_SIZE:
                        game_players[current_player].set_position(row, col)
                        print(f"Moved {game_players[current_player].name} to Room {room_names[row * 3 + col]}")

                        current_player = (current_player + 1) % len(game_players)
                        return True  
    return True 

running = True
while running:
    running = handle_events()
    draw_board()
    draw_characters()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
