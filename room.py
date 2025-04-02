<<<<<<< HEAD



class Room():

    def __init__(self, name: str, location: tuple, connections: list) -> None:
        

        self.name = name
        self.location = location
        self.connections = []  
        self.opacity = 50 


    def setConnections(self, connections: list):
        for room in connections:
            self.connections.append(room)

    def __repr__(self) -> str:
        return f" Room: {self.name}"


#Making this distinction so it can be drawn different for the hallway
class Hallway(Room):

    def __init__(self, name: str, location: tuple, dimensions: tuple, connections: list) -> None:

        super().__init__(name, location, connections)
        self.dimensions = dimensions
        self.connections = []  
    
    def setConnections(self, connections: list):
        for room in connections:
            self.connections.append(room)



class RoomFactory:

    @staticmethod
    def create_room(name, location, connections: list):
        return Room(name, location, connections)



    @staticmethod
    def create_hallway(name, location, dimensions, connections: list):
        return Hallway(name, location, dimensions, connections)
=======
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
>>>>>>> feature/tyler_backend
