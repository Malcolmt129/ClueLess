<<<<<<< HEAD
from types import FunctionType
import pygame

class Button():
    def __init__(self, position, baseColor, hovering_color,font, text_input):
        self.position = position 
        self.x_pos = position[0] 
        self.y_pos = position[1] 
        self.text_input = text_input
        self.font = font 
        self.baseColor, self.hovering_color = baseColor, hovering_color
        self.text = self.font.render(self.text_input, True, self.baseColor)
        self.rect  = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.padding = 10 
        self.buttonGB = self.createButtonBackground() # Using this for centering multiple buttons on a screen.


    def createButtonBackground(self):
        """
        Returns a background rectangle for the button by inflating the text's rect
        with the specified padding.
        """
        # Make a copy of the text rect
        bg_rect = self.rect.copy()
        # Inflate the rectangle by padding on all sides 
        bg_rect.inflate_ip(self.padding , self.padding)
        return bg_rect

    def draw(self, surface, bg_color):
        """
        Draws the button background and then the text on the given surface.
        """
        # Draw the background rectangle
        bg_rect = self.createButtonBackground()
        pygame.draw.rect(surface, bg_color, bg_rect)


        # Blit the text on top of the background
        surface.blit(self.text, self.rect)



    def checkForInput(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom)


    def changeColor(self, position):
        
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input, True, self.baseColor)



class ButtonFactory:
    
    @staticmethod
    def create_button(postion,  baseColor, hovering_color, font, text_input):
        return Button(postion, baseColor, hovering_color, font, text_input)
=======
import pygame

class Button():
    def __init__(self, screen, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#339999',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = pygame.font.SysFont('Arial', 40).render(buttonText, True, (20, 20, 20))
        self.alreadyPressed = False
        self.screen = screen


    def process(self):
        mousePos = pygame.mouse.get_pos()       
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)

def myFunction():
    print('Button Pressed')
>>>>>>> feature/tyler_backend
