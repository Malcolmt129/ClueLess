import pygame 
from button import Button  # Assuming Button is defined elsewhere
from defaults import Characters, Weapons, Rooms
from game_state import GameState
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TurnMenu:
    def __init__(self, screen, menu_rect, game_instance=None):
        """
        Initializes the TurnMenu.

        Args:
            screen (pygame.Surface): The surface on which to draw.
            title_text (str): The current player's name.
            menu_rect (pygame.Rect): The rectangle defining the menu area.
            game_instance (Game): The game instance to get custom names from.
        """
        self.screen = screen
        self.title_text = "Players joining..."
        self.menu_rect = menu_rect  # Defines the turn menu area.
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = []
        self.mode = "main"  # Modes: "main", "character_selection", "weapon_selection", "room_selection", "disprove_selection"
        self.action = None  # Final action string: for join, suggest, accuse, disprove, or "end"
        self.text_message = "Welcome to Clue-Less!"  # Text displayed in the text box.
        # Variables to store selections.
        self.suggested_character = None
        self.suggested_weapon = None
        self.suggested_room = None
        # Indicates the type of multi‑step process: 
        # "join" for joining (only choose a character), "suggest" for suggestion, "accuse" for accusation.
        self.suggestion_type = None
        
        # Initialize game state
        self.game_state = None
        self.user_id = -1
        
        # Use custom names from game instance if available
        if game_instance:
            self.CHARACTERS = game_instance.CHARACTERS
            self.WEAPONS = game_instance.WEAPONS
            self.ROOMS = game_instance.ROOMS
        else:
            # Fallback to defaults
            self.CHARACTERS = [character.value for character in Characters]
            self.WEAPONS = [weapon.value[0] if isinstance(weapon.value, tuple) else weapon.value for weapon in Weapons]
            self.ROOMS = [room.value[0] if isinstance(room.value, tuple) else room.value for room in Rooms]
        self.available_characters = self.CHARACTERS
        self.is_current_turn = False
        self.has_game_started = False
        self.is_disprover = False
        self.in_suggest_loop = False
        
        self.create_main_buttons()  # Create the main set of buttons.

    def create_main_buttons(self):
        """Creates the default (main) set of buttons based on the game state."""
        self.buttons = []  # Clear any existing buttons.
        center_x = self.menu_rect.x + self.menu_rect.width // 2

        # If the game has not started, only show "Join Game."
        if not self.has_game_started:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Join Game"))
            logger.debug("Game has not started. Created the 'Join Game' button only.")
        elif self.is_current_turn and not self.in_suggest_loop:
            # Game started: Show all main menu options.
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Make Suggestion"))
            self.buttons.append(Button((center_x, self.menu_rect.y + 250), "White", "Black", self.small_font, "Make Accusation"))
            self.buttons.append(Button((center_x, self.menu_rect.y + 350), "White", "Black", self.small_font, "End Turn"))
            logger.debug("Game has started. Created all main menu buttons.")
        elif self.is_disprover:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Disprove"))
        self.mode = "main"

    def show_character_selection(self):
        """Clears current buttons and shows buttons for character selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []  # Clear current buttons.
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100  # Starting vertical position.
        spacing = 50  # Vertical spacing between buttons.
        for i, character in enumerate(self.available_characters):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, character))
        # Add a "Back" button immediately after the list.
        y_pos = start_y + len(self.available_characters) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "character_selection"
        logger.debug(f"Switched to character selection mode: {len(self.buttons)} buttons created.")

    def show_weapon_selection(self):
        """Clears current buttons and shows buttons for weapon selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        # Use custom weapon names from game instance
        weapons = [self.WEAPONS[weapon] for weapon in Weapons]
        for i, weapon in enumerate(weapons):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, weapon))
        y_pos = start_y + len(weapons) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "weapon_selection"
        logger.debug(f"Switched to weapon selection mode: {len(self.buttons)} buttons created.")

    def show_room_selection(self):
        """Clears current buttons and shows buttons for room selection,
        then adds a 'Back' button as the next item."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        # Use custom room names from game instance
        rooms = [self.ROOMS[room] for room in Rooms]
        for i, room in enumerate(rooms):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, room))
        y_pos = start_y + len(rooms) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "room_selection"
        logger.debug(f"Switched to room selection mode: {len(self.buttons)} buttons created.")

    def show_disprove_selection(self):
        """
        Clears current buttons and displays a button for each
        available card for disproving from self.disprove_cards,
        then adds a 'Back' button as the next item.
        """
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        
        # Convert enum cards to custom names
        custom_cards = []
        for card in self.disprove_cards:
            if isinstance(card, Characters) and card in self.CHARACTERS:
                custom_cards.append(self.CHARACTERS[card])
            elif isinstance(card, Weapons) and card in self.WEAPONS:
                custom_cards.append(self.WEAPONS[card])
            elif isinstance(card, Rooms) and card in self.ROOMS:
                custom_cards.append(self.ROOMS[card])
            else:
                custom_cards.append(str(card))
                
        for i, card in enumerate(custom_cards):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, card))
        # Add a "Back" button.
        y_pos = start_y + len(custom_cards) * spacing
        self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, "Back"))
        self.mode = "disprove_selection"
        logger.debug(f"Switched to disprove selection mode: {len(self.buttons)} buttons created.")

    def process_game_state(self, game_state):
        """Update the menu based on the current game state."""
        # Store the game state
        self.game_state = game_state
        
        # Update game state flags
        self.has_game_started = game_state.game_started
        self.in_suggest_loop = game_state.disprover > 0
        
        # Update current turn and disprover status
        if hasattr(game_state, 'current_player'):
            self.is_current_turn = game_state.current_player == self.user_id
        else:
            self.is_current_turn = False
            
        if hasattr(game_state, 'disprover'):
            self.is_disprover = game_state.disprover == self.user_id
        else:
            self.is_disprover = False

        # Update available characters with custom names
        if hasattr(self, 'CHARACTERS') and isinstance(self.CHARACTERS, dict):
            self.available_characters = []
            for char in game_state.available_characters:
                if isinstance(char, Characters):
                    self.available_characters.append(self.CHARACTERS[char])
                else:
                    try:
                        enum_char = Characters(char)
                        self.available_characters.append(self.CHARACTERS[enum_char])
                    except ValueError:
                        self.available_characters.append(char)

            # Update title text with custom names
            if self.has_game_started and game_state.current_player in game_state.players:
                current_char = game_state.players[game_state.current_player].character
                if isinstance(current_char, Characters):
                    self.title_text = f"{self.CHARACTERS[current_char]}'s Turn"
                else:
                    try:
                        enum_char = Characters(current_char)
                        self.title_text = f"{self.CHARACTERS[enum_char]}'s Turn"
                    except ValueError:
                        self.title_text = f"{current_char}'s Turn"
            else:
                self.title_text = "Players joining..."
        else:
            # Fallback to default names
            self.available_characters = [
                char.value if isinstance(char, Characters) else char
                for char in game_state.available_characters
            ]
            if self.has_game_started and game_state.current_player in game_state.players:
                current_char = game_state.players[game_state.current_player].character
                self.title_text = f"{current_char.value if isinstance(current_char, Characters) else current_char}'s Turn"
            else:
                self.title_text = "Players joining..."

        if self.is_disprover and hasattr(game_state, 'suggestion'):
            self.set_disprove_cards(game_state.players[self.user_id].cards.intersection(set(game_state.suggestion)))
        else:
            self.set_disprove_cards(set())

        self.redraw_buttons()

    def set_available_characters(self, available_characters):
        """Set the available characters for selection, using custom names if available."""
        # Convert enum values to custom names if we have a game instance with custom names
        if hasattr(self, 'CHARACTERS') and isinstance(self.CHARACTERS, dict):
            # If CHARACTERS is a dict (custom names), convert enum values to custom names
            self.available_characters = []
            for char in available_characters:
                if isinstance(char, Characters):
                    # Use custom name if available
                    self.available_characters.append(self.CHARACTERS[char])
                else:
                    # Try to find the matching enum and use its custom name
                    try:
                        enum_char = Characters(char)
                        self.available_characters.append(self.CHARACTERS[enum_char])
                    except ValueError:
                        # If conversion fails, use the name as is
                        self.available_characters.append(char)
        else:
            # If no custom names, use the values directly
            self.available_characters = [
                char.value if isinstance(char, Characters) else char
                for char in available_characters
            ]
        # Don't redraw so you don't accidentally click wrong player

    def set_disprove_cards(self, cards):
        self.disprove_cards = cards

    def handle_event(self, event):
        """Processes mouse click events based on the current mode."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    label = button.text_input
                    logger.debug(f"Button '{label}' clicked in mode '{self.mode}'")
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
                        elif label == "Disprove":
                            self.show_disprove_selection()
                        elif label == "End Turn":
                            self.action = "end"
                    elif self.mode == "character_selection":
                        if label == "Back":
                            self.create_main_buttons()
                        else:
                            self.suggested_character = label
                            if self.suggestion_type == "join":
                                self.action = f"join:{self.suggested_character}"
                                self.create_main_buttons()
                            else:
                                self.show_weapon_selection()
                    elif self.mode == "weapon_selection":
                        if label == "Back":
                            self.show_character_selection()
                        else:
                            self.suggested_weapon = label
                            self.show_room_selection()
                    elif self.mode == "room_selection":
                        if label == "Back":
                            self.show_weapon_selection()
                        else:
                            self.suggested_room = label
                            self.action = f"{self.suggestion_type}:{self.suggested_character}:{self.suggested_weapon}:{self.suggested_room}"
                            self.create_main_buttons()
                    elif self.mode == "disprove_selection":
                        if label == "Back":
                            self.create_main_buttons()
                        else:
                            self.action = f"disprove:{label}"
                            self.create_main_buttons()
                    break

    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect)

        # Draw header text with dynamic scaling to fit inside the rect.
        header_text = self.title_text
        font_size = 60  # Start with the default font size.
        font = pygame.font.Font(None, font_size)
        header_width = font.size(header_text)[0]

        # Dynamically reduce font size until the text fits within the rect width.
        while header_width > self.menu_rect.width - 20 and font_size > 10:
            font_size -= 2
            font = pygame.font.Font(None, font_size)
            header_width = font.size(header_text)[0]

        # Render the header text and center it in the rect.
        header_surface = font.render(header_text, True, "white")
        header_rect = header_surface.get_rect(center=(self.menu_rect.x + self.menu_rect.width // 2, self.menu_rect.y + 50))
        self.screen.blit(header_surface, header_rect)

        # Draw each button.
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))

        # Draw a multi-line text box at the bottom.
        textbox_height = 150
        textbox_rect = pygame.Rect(
            self.menu_rect.x + 10,
            self.menu_rect.bottom - textbox_height - 10,
            self.menu_rect.width - 20,
            textbox_height
        )
        pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 2)
        self.draw_wrapped_text(self.text_message, textbox_rect, self.small_font, "white")


    def draw_wrapped_text(self, text, rect, font, color):
        """Renders text word-wrap inside a given rectangle."""
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

    def set_text(self, msg):
        """Updates the text message shown in the turn menu's text box."""
        self.text_message = msg

    def redraw_buttons(self):
        """Redraws buttons dynamically based on the current mode."""
        if self.mode == "main":
            self.create_main_buttons()
        elif self.mode == "character_selection":
            self.show_character_selection()
        elif self.mode == "weapon_selection":
            self.show_weapon_selection()
        elif self.mode == "room_selection":
            self.show_room_selection()
        elif self.mode == "disprove_selection":
            self.show_disprove_selection()
        else:
            logger.debug(f"Unknown mode '{self.mode}', no buttons to redraw.")

        logger.debug(f"Buttons redrawn for mode '{self.mode}'.")
