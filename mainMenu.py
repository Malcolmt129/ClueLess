import pygame
from button import Button, ButtonFactory

class MainMenu:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.caption = "Main Menu"
        self.screen = screen
        self.font = pygame.font.Font(None, 72)
        self.running = True
        self.buttons = []
        
        self.background_image = pygame.image.load("./assets/ClueLessOpeningScreen.png")
        self.background_image = pygame.transform.smoothscale(self.background_image, (800, 800))
        
        self.create_buttons()

    def create_buttons(self):
        # Add more buttons here later if needed
        play_button = ButtonFactory.create_button(
            (400, 400),
            baseColor="White",
            hovering_color="Black",
            font=self.font,
            text_input="Play"
        )
        self.buttons.append(play_button)

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw all buttons
        mouse = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse)
            button.draw(self.screen, (90, 90, 90, 50))

    def display(self):
        while self.running:
            pygame.display.set_caption(self.caption)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.buttons[0].checkForInput(mouse):
                        self.running = False

            pygame.display.update()
