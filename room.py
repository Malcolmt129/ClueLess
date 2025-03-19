


class Room():

    def __init__(self, name: str, location: tuple) -> None:
        

        self.name = name
        self.location = location
        self.connections = []  
    


    def setConnections(self, connections: list):
        for room in connections:
            self.connections.append(room)

    def __repr__(self) -> str:
        return f" Room: {self.name}"


#Making this distinction so it can be drawn different for the hallway
class Hallway(Room):

    def __init__(self, name: str, location: tuple, dimensions: tuple) -> None:

        super().__init__(name, location)
        self.dimensions = dimensions
        self.connections = []  
    
    def setConnections(self, connections: list):
        for room in connections:
            self.connections.append(room)



class RoomFactory:

    @staticmethod
    def create_room(name, location):
        return Room(name, location)



    @staticmethod
    def create_hallway(name, location, dimensions):
        return Hallway(name, location, dimensions)
