from types import FunctionType
import pygame

class Button():
    def __init__(self, position, baseColor, hovering_color,font, text_input, on_click=None, bgImage=None):
        self.position = position 
        self.x_pos = position[0] 
        self.y_pos = position[1] 
        self.text_input = text_input
        self.font = font
        self.on_click = on_click 
        self.baseColor, self.hovering_color = baseColor, hovering_color
        self.text = self.font.render(self.text_input, True, self.baseColor)
        self.rect  = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.padding = 10 
        self.buttonGB = self.createButtonBackground() # Using this for centering multiple buttons on a screen.
        self.bgImage = bgImage 
        self.bgImagenotLoaded = True 



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

        if self.bgImage != None:
            image_size = self.rect.height
            bg_rect = self.rect.copy()
            bg_rect.inflate_ip(image_size, 0)

            image = pygame.transform.scale(self.bgImage, (image_size, image_size))
            surface.blit(image, self.rect)
            
            image_rect = image.get_rect()
            image_rect.left = self.rect.left
            image_rect.centery = self.rect.centery
            surface.blit(image, image_rect)

            text_rect = self.text.get_rect()
            text_rect.left = image_rect.right + 10  # 10px padding from image
            text_rect.centery = self.rect.centery
            surface.blit(self.text, text_rect)

        else:
            
            # Draw the background rectangle
            bg_rect = self.createButtonBackground()
            pygame.draw.rect(surface, bg_color, bg_rect)

            # Blit the text on top of the background
            surface.blit(self.text, self.rect)



    def checkForInput(self, position, flag: bool = False):
        if self.rect.collidepoint(position):  # Check if clicked
            if self.on_click and isinstance(self.on_click, FunctionType):
                self.on_click()  # Execute the function
            return True
        return False


    def changeColor(self, position):
        
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)

        else:
            self.text = self.font.render(self.text_input, True, self.baseColor)



class ButtonFactory:
    
    @staticmethod
    def create_button(postion,  baseColor, hovering_color, font, text_input):
        return Button(postion, baseColor, hovering_color, font, text_input)
