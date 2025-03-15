


class Room():

    def __init__(self, name: str, location: tuple, dimensions: tuple, omissions: list[tuple], doorways: list[tuple]) -> None:
        

        self.name = name
        self.location = location
        self.dimensions = dimensions
        self.omissions = omissions 
        self.doorways = doorways 

    def setDrawingOmissions(self, coordinates: list):

        for coordinate in coordinates:
            self.omissions.append(coordinate)





    



