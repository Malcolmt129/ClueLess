import pygame
import constants 
import room


class Board:

    def __init__(self):
        self.board = []
        self.players = []
        self.rooms = []
        
    def grid_draw(self, window):

        for row in range(constants.ROWS):
            for col in range(row % 2, constants.ROWS, 2):
                pygame.draw.rect(window, constants.WHITE, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

    def createRooms(self):

        kitchen = room.Room("Kitchen", 0,0, (6,6))
        kitchen.setDrawingOmissions([(0,5)])
        self.rooms.append(kitchen)


        dining = room.Room("Dining", 0,8, (8,7))
        dining.setDrawingOmissions([(7,0), (6,0), (5,0)])
        self.rooms.append(dining)

    def rooms_draw(self, window):
        font = pygame.font.Font(None, 24)  # Small font for room names
        
        self.createRooms()

        for room in self.rooms:
            for row in range(room.dimensions[0]):
                for column in range(room.dimensions[1]):

                    if (row,column) in room.omissions:
                        continue
                    pygame.draw.rect(window, constants.GREY, 
                                    ((row + room.x) * constants.SQUARE_SIZE, 
                                    (column + room.y) * constants.SQUARE_SIZE, 
                                    constants.SQUARE_SIZE, 
                                    constants.SQUARE_SIZE))
            
            # Calculate room label position (approx. center of first tile)
            label_x = ((room.x * constants.SQUARE_SIZE)) + ((room.dimensions[0] - 1) * constants.SQUARE_SIZE   // 2)
            label_y = ((room.y * constants.SQUARE_SIZE)) + ((room.dimensions[1] - 1)* constants.SQUARE_SIZE   // 2)

            # Draw text label for the room
            text = font.render(room.name, True, constants.BLACK)
            text_rect = text.get_rect(center=(label_x, label_y))
            window.blit(text, text_rect)
