import pygame
import board
from button import Button
import json


class TurnInterface():


    def __init__(self): 

        self.buttons = []
        self.button_y_coord = 30        


    def _buttons_create(self,screen: pygame.Surface):
        

        accuse = json.dumps({"type": "accusation", "person": "mustard", "room": "bathroom","weapon": "revolver"})
        suggest = json.dumps({"type": "suggestion","person": "mustard",  "room": "bathroom","weapon": "revolver"})
        move = json.dumps({"type": "move","coordinate": 0})
        join = json.dumps({"type": "join","character": "Mrs. White"})
        disprove = json.dumps({"type": "disprove", "card": ""})
        end_turn = json.dumps({"type": "end_turn"})

        self.accusation_button = Button(screen, 700, self.button_y_coord, 400, 100, 'Accusation', lambda : self.game.client_socket.sendall(accuse.encode()))
        self.button_y_coord += 110
        self.suggestion_button = Button(screen, 700, self.button_y_coord, 400, 100, 'Suggestion', lambda : self.game.client_socket.sendall(suggest.encode()))
        # self.button_y_coord += 110
        # self.move_button = Button(self.board.screen, 700, self.button_y_coord, 400, 100, 'Move', lambda : self.game.client_socket.sendall(move.encode()))
        self.button_y_coord += 110
        self.join_button = Button(screen, 700, self.button_y_coord, 400, 100, 'Join', lambda : self.game.client_socket.sendall(join.encode()))    
        self.button_y_coord += 110    
        self.disprove_button = Button(screen, 700, self.button_y_coord, 400, 100, 'Disprove', lambda : self.game.client_socket.sendall(disprove.encode()))       
        self.button_y_coord += 110    
        self.end_turn_button = Button(screen, 700, self.button_y_coord, 400, 100, 'End Turn', lambda : self.game.client_socket.sendall(end_turn.encode()))  
        # self.buttons = [self.accusation_button, self.suggestion_button, self.move_button, self.join_button, self.disprove_button, self.end_turn_button]
        self.buttons = [self.accusation_button, self.suggestion_button, self.join_button, self.disprove_button, self.end_turn_button]


    
