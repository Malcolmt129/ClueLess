import pygame
import sys
from characters import characters, Character  # Import characters and Character class

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROOM_SIZE = 150
HALLWAY_SIZE = 50
GRID_ROWS = 3
GRID_COLS = 3
FPS = 30

# Define colors
WHITE = (255, 255, 255)  # White color for the background
BLACK = (0, 0, 0)  # Black color for text and borders
HALLWAY_COLOR = (169, 169, 169)  # Dark Grey for hallways

# Define colors for rooms
room_colors = [
    (255, 182, 193),  # Kitchen - Light Pink
    (255, 223, 186),  # Ballroom - Peach
    (224, 255, 255),  # Conservatory - Light Blue
    (255, 239, 186),  # Dining Room - Light Yellow
    (204, 255, 204),  # Library - Light Green
    (255, 224, 178),  # Billiard Room - Light Orange
    (255, 240, 245),  # Lounge - Light Lavender
    (255, 255, 204),  # Hall - Light Cream
    (224, 204, 255),  # Study - Light Purple
]

# Room names
room_names = [
    "Kitchen", "Ballroom", "Conservatory",
    "Dining Room", "Library", "Billiard Room",
    "Lounge", "Hall", "Study"
]

game_characters = [Character(name, "Suspect") for name in characters]

# Initialize the player positions dictionary
player_positions = {char.name: (0, 0) for char in game_characters}  # All start at room (0, 0)
current_player = 0  # Track which player's turn it is

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clue-Less Game")

# Initialize clock for FPS
clock = pygame.time.Clock()

# Function to draw the game grid (rooms and hallways)
def draw_board():
    screen.fill(WHITE)
    
    # Draw rooms in a 3x3 grid
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            # Calculate room position
            x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            
            # Draw room rectangle
            pygame.draw.rect(screen, room_colors[row * 3 + col], (x, y, ROOM_SIZE, ROOM_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, ROOM_SIZE, ROOM_SIZE), 2)  # Borders
            
            # Draw room name
            font = pygame.font.Font(None, 24)
            room_text = font.render(room_names[row * 3 + col], True, BLACK)
            screen.blit(room_text, (x + ROOM_SIZE // 4, y + ROOM_SIZE // 3))

    # Draw hallways between rooms
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
            y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE

            # Draw horizontal hallways (between adjacent rooms)
            if col < GRID_COLS - 1:  
                hallway_x = x + ROOM_SIZE
                hallway_y = y + (ROOM_SIZE // 4)  
                pygame.draw.rect(screen, HALLWAY_COLOR, (hallway_x, y + (ROOM_SIZE // 4), HALLWAY_SIZE, ROOM_SIZE // 2))

            # Draw vertical hallways (between adjacent rooms)
            if row < GRID_ROWS - 1:  
                hallway_x = x + (ROOM_SIZE // 4)
                hallway_y = y + ROOM_SIZE
                pygame.draw.rect(screen, HALLWAY_COLOR, (x + (ROOM_SIZE // 4), hallway_y, ROOM_SIZE // 2, HALLWAY_SIZE))

# Function to draw characters
def draw_characters():
    for character in game_characters:
        row, col = player_positions[character.name]
        x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
        y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE + ROOM_SIZE // 2
        pygame.draw.circle(screen, BLACK, (x, y), 15)
        # Draw character name under the circle (for reference)
        font = pygame.font.Font(None, 24)
        text = font.render(character.name, True, BLACK)
        screen.blit(text, (x - text.get_width() // 2, y + 20))

# Function to handle events (movement, suggestions, etc.)
def handle_events():
    global current_player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            
            # Only allow the current player to move
            if current_player >= len(game_characters):
                return True  # If no more players left, do nothing

            # Check if the click was inside a room
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    room_x = col * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    room_y = row * (ROOM_SIZE + HALLWAY_SIZE) + HALLWAY_SIZE
                    if room_x <= x <= room_x + ROOM_SIZE and room_y <= y <= room_y + ROOM_SIZE:
                        # Move the current player to the clicked room
                        player_positions[game_characters[current_player].name] = (row, col)
                        print(f"Moved {game_characters[current_player].name} to Room {room_names[row * 3 + col]}")
                        
                        # After the move, update to the next player's turn
                        current_player = (current_player + 1) % len(game_characters)
                        return True  
    return True 

# Main game loop
running = True
while running:
    running = handle_events()

    # Draw the game board and characters
    draw_board()
    draw_characters()
    
    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
