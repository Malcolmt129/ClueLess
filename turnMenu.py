import pygame 
from button import Button  # Assuming Button is defined elsewhere
from defaults import Characters, Weapons, Rooms

# Build lists for options from the enums.
# For Characters, you will get the string directly.
CHARACTERS = [character.value for character in Characters]
# For Weapons and Rooms, if your values are tuples due to the trailing comma,
# you can extract the first element (or remove the trailing comma in defaults.py).
WEAPONS = [weapon.value[0] if isinstance(weapon.value, tuple) else weapon.value for weapon in Weapons]
ROOMS = [room.value[0] if isinstance(room.value, tuple) else room.value for room in Rooms]

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
        self.menu_rect = menu_rect  # Defines the turn menu area.
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = []
        self.mode = "main"  # Modes: "main", "character_selection", "weapon_selection", "room_selection"
        self.action = None  # Final action string: for join, suggest, accuse, or "end"
        self.text_message = ""  # Text displayed in the text box.
        # Variables to store selections.
        self.suggested_character = None
        self.suggested_weapon = None
        self.suggested_room = None
        # Indicates the type of multi‑step process: 
        # "join" for joining (only choose a character), 
        # "suggest" for suggestion, and "accuse" for accusation.
        self.suggestion_type = None  
        
        self.create_main_buttons()  # Create the main set of buttons.

    def create_main_buttons(self):
        """Creates the default (main) set of buttons."""
        self.buttons = []  # Clear any existing buttons.
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        # Create buttons with vertical spacing.
        # Order: Join Game, Make Suggestion, Make Accusation, End Turn.
        self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Join Game"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 250), "White", "Black", self.small_font, "Make Suggestion"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 350), "White", "Black", self.small_font, "Make Accusation"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 450), "White", "Black", self.small_font, "End Turn"))
        self.mode = "main"
        print(f"[DEBUG] Created main buttons: {len(self.buttons)} buttons.")

    def show_character_selection(self):
        """Clears current buttons and shows buttons for character selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []  # Clear current buttons.
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100  # Starting vertical position.
        spacing = 50  # Vertical spacing between buttons.
        for i, character in enumerate(CHARACTERS):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, character))
        # Add a "Back" button immediately after the list.
        y_pos = start_y + len(CHARACTERS) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "character_selection"
        print(f"[DEBUG] Switched to character selection mode: {len(self.buttons)} buttons created.")

    def show_weapon_selection(self):
        """Clears current buttons and shows buttons for weapon selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, weapon in enumerate(WEAPONS):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, weapon))
        y_pos = start_y + len(WEAPONS) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "weapon_selection"
        print(f"[DEBUG] Switched to weapon selection mode: {len(self.buttons)} buttons created.")

    def show_room_selection(self):
        """Clears current buttons and shows buttons for room selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, room in enumerate(ROOMS):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, room))
        y_pos = start_y + len(ROOMS) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "room_selection"
        print(f"[DEBUG] Switched to room selection mode: {len(self.buttons)} buttons created.")

    def draw(self):
        """Draws the turn menu panel, buttons, and text box."""
        # Draw the background panel.
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect)

        # Draw header text.
        header_text = self.font.render(f"{self.player_name}'s Turn", True, "white")
        header_rect = header_text.get_rect(center=(self.menu_rect.x + self.menu_rect.width // 2, self.menu_rect.y + 50))
        self.screen.blit(header_text, header_rect)

        # Draw each button.
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))

        # Draw a multi-line text box at the bottom.
        textbox_height = 100
        textbox_rect = pygame.Rect(
            self.menu_rect.x + 10,
            self.menu_rect.bottom - textbox_height - 10,
            self.menu_rect.width - 20,
            textbox_height
        )
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 2)
        self.draw_wrapped_text(self.text_message, textbox_rect, self.small_font, "white")

    def handle_event(self, event):
        """Processes events based on the current mode."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"[DEBUG] Mouse click at: {mouse_pos}")
            for button in self.buttons:
                print(f"[DEBUG] Checking button '{button.text_input}' with rect: {button.buttonGB}")
                if button.checkForInput(mouse_pos):
                    label = button.text_input
                    print(f"[DEBUG] Button '{label}' detected a click!")
                    if self.mode == "main":
                        if label == "Join Game":
                            self.suggestion_type = "join"
                            self.show_character_selection()
                        elif label == "Make Suggestion":
                            self.suggestion_type = "suggest"
                            self.show_character_selection()
                        elif label == "Make Accusation":
                            self.suggestion_type = "accuse"
                            self.show_character_selection()
                        elif label == "End Turn":
                            print("Ending Turn...")
                            self.action = "end"
                    elif self.mode == "character_selection":
                        if label == "Back":
                            self.create_main_buttons()
                        else:
                            self.suggested_character = label
                            if self.suggestion_type == "join":
                                self.action = f"join:{self.suggested_character}"
                                print(f"Final join action: {self.action}")
                                self.create_main_buttons()
                            else:
                                print(f"Selected character: {self.suggested_character}")
                                self.show_weapon_selection()
                    elif self.mode == "weapon_selection":
                        if label == "Back":
                            self.show_character_selection()
                        else:
                            self.suggested_weapon = label
                            print(f"Selected weapon: {self.suggested_weapon}")
                            self.show_room_selection()
                    elif self.mode == "room_selection":
                        if label == "Back":
                            self.show_weapon_selection()
                        else:
                            self.suggested_room = label
                            print(f"Selected room: {self.suggested_room}")
                            self.action = f"{self.suggestion_type}:{self.suggested_character}:{self.suggested_weapon}:{self.suggested_room}"
                            print(f"Final {self.suggestion_type} action: {self.action}")
                            self.create_main_buttons()
                    break  # Process only one button per click.

    def set_text(self, msg):
        """Updates the text in the text box."""
        self.text_message = msg

    def draw_wrapped_text(self, text, rect, font, color):
        """
        Draws text within a rectangular area, wrapping words onto new lines if needed.
        """
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip() if current_line else word
            if font.size(test_line)[0] <= rect.width - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        line_height = font.get_linesize()
        y_offset = rect.y + 5
        for line in lines:
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (rect.x + 5, y_offset))
            y_offset += line_height
