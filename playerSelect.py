import pygame 
from button import Button, ButtonFactory

class PlayerSelect():


    def __init__(self,screen: pygame.surface.Surface) -> None:
        self.caption = "Player Select" 
        self.characters = [] # The players that are left
        self.screen = screen
        self.font  = pygame.font.Font(None,72) 
        self.running = True
        

        self.createButtons()

    def display(self):
        
        while self.running:

            pygame.display.set_caption(self.caption) 

            mouse = pygame.mouse.get_pos() 
            self.screen.fill("black")


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                       self.running = False 
            pygame.display.update()


    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw all buttons
        mouse = pygame.mouse.get_pos()

        for button in self.buttons:
            button.changeColor(mouse)
            button.draw(self.screen, (90, 90, 90, 50))


    def createButtons(self):
        pass
        
         
