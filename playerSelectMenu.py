import pygame 
from button import Button, ButtonFactory

class PlayerSelectMenu():


    def __init__(self,screen: pygame.surface.Surface) -> None:
        self.caption = "Player Select" 
        self.characters = [] # The players that are left
        self.screen = screen
        self.font  = pygame.font.Font(None,72) 
        self.running = True
        self.buttons = [] 
        
        self.characeterImages = [
                "./assets/MsScarlett.png",
                "./assets/ColMustard.png",
                "./assets/MrsWhite.png",
                "./assets/MrGreen.png",
                "./assets/MrsPeacock.png",
                "./assets/ProfessorPlum.png"
        ]


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


    def createButtons(self):
        
        # Add more buttons here later if needed

        msScarlet = ButtonFactory.create_button(
            (400, 400),
            baseColor="White",
            hovering_color="Black",
            font=self.font,
            text_input="Play"
        )
        self.buttons.append(msScarlet)
         
