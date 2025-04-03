import pygame 
from button import Button  # Assuming Button is defined elsewhere

class TurnMenu:
    def __init__(self, screen, player_name, menu_rect):
        """
        Initializes the TurnMenu.
        
        Args:
            screen (pygame.Surface): The surface on which to draw.
            player_name (str): The current player's name.
            menu_rect (pygame.Rect): The rectangle defining the menu area.
        """
        self.screen = screen
        self.player_name = player_name
        self.menu_rect = menu_rect  # A pygame.Rect defining the menu area
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = []
        self.create_buttons()
        self.action = None  # Captures the current selected action ("suggest", "accuse", or "end")
        self.text_message = ""  # Holds the text to be displayed in the text box

    def create_buttons(self):
        # Calculate center x-coordinate within the menu_rect
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        # Create buttons with positions relative to the menu_rect
        self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Make Suggestion"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 250), "White", "Black", self.small_font, "Make Accusation"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 350), "White", "Black", self.small_font, "End Turn"))

    def draw(self):
        # Draw a background panel for the turn menu
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect)

        # Draw the player's turn header at the top of the panel
        header_text = self.font.render(f"{self.player_name}'s Turn", True, "white")
        header_rect = header_text.get_rect(center=(self.menu_rect.x + self.menu_rect.width // 2, self.menu_rect.y + 50))
        self.screen.blit(header_text, header_rect)

        # Draw buttons, updating their colors based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))
        
        # Draw the multiline text box at the bottom of the turn menu area
        textbox_height = 100  # Make the text box taller
        textbox_rect = pygame.Rect(
            self.menu_rect.x + 10,                             # 10 pixels padding from the left edge
            self.menu_rect.bottom - textbox_height - 10,       # 10 pixels padding from the bottom of the menu
            self.menu_rect.width - 20,                         # Padding on both sides
            textbox_height
        )
        # Draw the border of the text box.
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 2)
        # Draw wrapped text inside the text box.
        self.draw_wrapped_text(self.text_message, textbox_rect, self.small_font, "white")

    def handle_event(self, event):
        # Process mouse click events for the buttons.
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

    def set_text(self, msg):
        """
        Updates the text that will be displayed in the text box.
        
        Args:
            msg (str): The new text to display.
        """
        self.text_message = msg

    def draw_wrapped_text(self, text, rect, font, color):
        """
        Draw text in a rectangular area, wrapping words to new lines if necessary.
        
        Args:
            text (str): The text to draw.
            rect (pygame.Rect): The rectangle in which to draw the text.
            font (pygame.font.Font): The font used to render the text.
            color (str or tuple): The color of the text.
        """
        words = text.split(" ")
        lines = []
        current_line = ""
        # Split text into multiple lines that fit inside rect.width
        for word in words:
            test_line = f"{current_line} {word}".strip() if current_line else word
            if font.size(test_line)[0] <= rect.width - 10:  # A little extra padding
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Render each line and blit it inside the rect
        line_height = font.get_linesize()
        y_offset = rect.y + 5  # Start with a 5px padding from top
        for line in lines:
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (rect.x + 5, y_offset))
            y_offset += line_height
