WIDTH, HEIGHT = 800, 800
ROWS, COLS = 25, 25
FPS = 60
SQUARE_SIZE = WIDTH // COLS

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192,192) 
SPRING_GREEN = (0, 255, 127) # To mark doorways

CHARACTER_COLORS = {
    "Ms. Scarlet": (255, 36, 0),      # Red
    "Colonel Mustard": (255, 219, 88), # Yellow
    "Mrs. White": (255, 255, 255),     # White
    "Mr. Green": (0, 128, 0),          # Green
    "Mrs. Peacock": (31, 117, 254),    # Blue
    "Professor Plum": (128, 0, 128)    # Purple
}

ROOM_COLORS = {
    "KITCHEN": (255, 200, 200),
    "BALLROOM": (200, 255, 200),
    "CONSERVATORY": (200, 255, 255),
    "DINING ROOM": (255, 255, 200),
    "BILLARD ROOM": (150, 255, 150),
    "LIBRARY": (255, 230, 200),
    "LOUNGE": (255, 200, 255),
    "HALL": (200, 200, 255),
    "STUDY": (230, 230, 230)
}