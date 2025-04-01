import pygame 
from button import Button, ButtonFactory
import sys

class TurnMenu():


    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)

        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons.append(Button((400, 300), "White", "Black", self.small_font, "Make Suggestion"))
        self.buttons.append(Button((400, 400), "White", "Black", self.small_font, "Make Accusation"))
        self.buttons.append(Button((400, 500), "White", "Black", self.small_font, "End Turn"))

    def draw(self):
        self.screen.fill((30, 30, 30))  # Dark background

        # Draw player name at top
        text = self.font.render(f"{self.player_name}'s Turn", True, "white")
        text_rect = text.get_rect(center=(400, 100))
        self.screen.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))

    def run(self):
        running = True
        action = None

        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons[0].checkForInput(pygame.mouse.get_pos()):
                        print("Making Suggestion...")
                        action = "suggest"
                        running = False

                    elif self.buttons[1].checkForInput(pygame.mouse.get_pos()):
                        print("Making Accusation...")
                        action = "accuse"
                        running = False

                    elif self.buttons[2].checkForInput(pygame.mouse.get_pos()):
                        print("Ending turn...")
                        action = "end"
                        running = False

            pygame.display.flip()

        return action
         
