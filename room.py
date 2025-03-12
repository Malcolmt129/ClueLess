


class Room():

    def __init__(self, name: str, x: int, y: int, dimensions: tuple) -> None:
        

        self.name = name
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.omissions = []

    def setDrawingOmissions(self, coordinates: list):

        for coordinate in coordinates:
            self.omissions.append(coordinate)





    



