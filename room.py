from constants import room_names, room_colors, GRID_ROWS, GRID_COLS

class Room:
    def __init__(self, name, color, row, col):
        self.name = name
        self.color = color
        self.row = row
        self.col = col
        self.occupied = False  # Track if a player is in the room

    def __repr__(self):
        return f"Room({self.name}, {self.row}, {self.col})"

    def is_occupied(self):
        return self.occupied

    def set_occupied(self, status):
        self.occupied = status

def create_rooms():
    rooms = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            index = row * GRID_COLS + col
            room = Room(room_names[index], room_colors[index], row, col)
            rooms.append(room)
    return rooms
