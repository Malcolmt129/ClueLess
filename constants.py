<<<<<<< HEAD

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 25, 25
FPS = 60
SQUARE_SIZE = WIDTH // COLS

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192) 
SPRING_GREEN = (0, 255, 127) # To mark doorways

CHARACTER_COLORS = {
    "Miss Scarlet": (255, 36, 0),      # Red
    "Colonel Mustard": (255, 219, 88), # Yellow
    "Mrs. White": (255, 255, 255),     # White
    "Mr. Green": (0, 128, 0),          # Green
    "Mrs. Peacock": (31, 117, 254),    # Blue
    "Professor Plum": (128, 0, 128)    # Purple
}

=======
# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 30

# Grid settings
ROOM_SIZE = 150
HALLWAY_SIZE = 50
GRID_ROWS = 3
GRID_COLS = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HALLWAY_COLOR = (169, 169, 169)

room_colors = [
    (255, 182, 193), (255, 223, 186), (224, 255, 255),
    (255, 239, 186), (204, 255, 204), (255, 224, 178),
    (255, 240, 245), (255, 255, 204), (224, 204, 255),
]

room_names = [
    'Study', 'Hall', 'Lounge', 
    'Billiard Room', 'Library', 'Dining Room', 
    'Conservatory', 'Ballroom', 'Kitchen'
]
>>>>>>> feature/tyler_backend
