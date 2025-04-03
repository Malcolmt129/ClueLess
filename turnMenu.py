import pygame 
from button import Button  # Assuming Button is defined elsewhere

class TurnMenu:
    def __init__(self, screen, player_name, menu_rect):
        self.screen = screen
        self.player_name = player_name
        self.menu_rect = menu_rect  # A pygame.Rect defining the menu area
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = []
        self.create_buttons()
        self.action = None  # Will record the action selected by the user

    def create_buttons(self):
        # Calculate button positions relative to self.menu_rect
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        # For example, vertically stack buttons with some spacing:
        self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Make Suggestion"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 250), "White", "Black", self.small_font, "Make Accusation"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 350), "White", "Black", self.small_font, "End Turn"))

    def draw(self):
        # Draw a background panel for the turn menu
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect)
        # Draw the player's turn title at the top of the panel
        text = self.font.render(f"{self.player_name}'s Turn", True, "white")
        text_rect = text.get_rect(center=(self.menu_rect.x + self.menu_rect.width // 2, self.menu_rect.y + 50))
        self.screen.blit(text, text_rect)
        # Draw the buttons (update their colors based on the mouse position)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))

    def handle_event(self, event):
        # Check for mouse click events within the turn menu area
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].checkForInput(pygame.mouse.get_pos()):
                print("Making Suggestion...")
                self.action = "suggest"
            elif self.buttons[1].checkForInput(pygame.mouse.get_pos()):
                print("Making Accusation...")
                self.action = "accuse"
            elif self.buttons[2].checkForInput(pygame.mouse.get_pos()):
                print("Ending Turn...")
                self.action = "end"
