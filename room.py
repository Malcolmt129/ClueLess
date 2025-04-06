


class Room():

    def __init__(self, name: str, location: tuple, connections: list) -> None:
        

        self.name = name
        self.location = location
        self.gridLocation = ()
        self.connections = []  

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
        self.occupied = False
    
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
