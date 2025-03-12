class Player:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)  # Default starting position

    def set_position(self, row, col):
        """Sets the player's position on the board."""
        self.position = (row, col)

    def get_position(self):
        """Returns the player's current position."""
        return self.position
