import pygame
import constants 
import room

class Board:

    def __init__(self):
        self.board = []
        self.players_pos = []
        self.rooms = []
        self.doorways = [(4,7), (7,5), (9,8), 
                         (14,8), (16,5), (18,5),
                         (17,9),(20,13),(22,13),
                         (16,16), (17,20), (15,20),
                         (12,17), (11,17), (6,16),
                         (6,18), (8,12)]
        self.startingPoints = []
        
    def grid_draw(self, window):

        for row in range(constants.ROWS):
            for col in range(row % 2, constants.ROWS, 2):
                    pygame.draw.rect(window, constants.WHITE, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
    

    def doorways_draw(self, window):

        for row in range(constants.ROWS):
            for col in range(constants.COLS):
                
                if (row, col) in self.doorways:

                    pygame.draw.rect(window, constants.SPRING_GREEN, (row*constants.SQUARE_SIZE, col*constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))


    def createRooms(self):

        kitchen = room.Room("Kitchen", 0,1, (6,6))
        kitchen.setDrawingOmissions([(0,5)])
        self.rooms.append(kitchen)


        dining = room.Room("DINING ROOM", 0,9, (8,7))
        dining.setDrawingOmissions([(7,0), (6,0), (5,0)])
        self.rooms.append(dining)
        
        ballroom = room.Room("BALLROOM", 8,1, (8,7)) 
        ballroom.setDrawingOmissions([(0,0),(1,0),(6,0),(7,0)])
        self.rooms.append(ballroom)

        conserv = room.Room("CONSERVATORY", 18,1, (6,5)) 
        conserv.setDrawingOmissions([(0,4), (5,4)])
        self.rooms.append(conserv)

        billiard = room.Room("BILLIARD ROOM", 18,8, (6,5)) 
        self.rooms.append(billiard)


        library = room.Room("LIBRARY", 17,14, (7,5)) 
        library.setDrawingOmissions([(0,0), (6,0), (0,4),(6,4)])
        self.rooms.append(library)


        study = room.Room("STUDY", 17,21, (7,4)) 
        study.setDrawingOmissions([(0,3)])
        self.rooms.append(study)

        hall = room.Room("HALL", 9,18, (6,7)) 
        self.rooms.append(hall)

        lounge = room.Room("LOUNGE", 0,19, (7,6)) 
        lounge.setDrawingOmissions([(6,5)])
        self.rooms.append(lounge)

        centerRoom = room.Room("", 10,10, (5,7)) 
        self.rooms.append(centerRoom)


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
