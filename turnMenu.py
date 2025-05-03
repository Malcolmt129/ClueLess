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

# Build lists from the enums.
CHARACTERS = [character.value for character in Characters]
WEAPONS = [weapon.value[0] if isinstance(weapon.value, tuple) else weapon.value for weapon in Weapons]
ROOMS = [room.value[0] if isinstance(room.value, tuple) else room.value for room in Rooms]

class TurnMenu:
    def __init__(self, screen, menu_rect):
        """
        Initializes the TurnMenu.

        Args:
            screen (pygame.Surface): The surface on which to draw.
            menu_rect (pygame.Rect): The rectangle defining the menu area.
        """
        self.screen = screen
        self.title_text = "Players joining..."
        self.menu_rect = menu_rect  # Turn menu area.
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)
        self.buttons = []
        # Modes: "main", "character_selection", "weapon_selection", "room_selection", 
        # "disprove_selection", "chat_view" (shows chat log), "chat_send" (target selection), 
        # "chat_compose" (message composition)
        self.mode = "main"
        self.action = None  # Final action string for game events.
        self.text_message = "Welcome to Clue-Less!"
        # Selections
        self.suggested_character = None
        self.suggested_weapon = None
        self.suggested_room = None
        self.suggestion_type = None  # "join", "suggest", "accuse"
        self.disprove_cards = []
        self.available_characters = CHARACTERS
        self.is_current_turn = False
        self.has_game_started = False
        self.is_disprover = False
        self.in_suggest_loop = False
        self.player_cards = []  # Player's cards

        # Chat-related attributes.
        self.chat_log = []       # List of chat lines (each line is a string).
        self.chat_input = ""     # Message being composed.
        self.selected_target = None  # Chat target, e.g., "Broadcast" or a player's character name.
        self.joined_characters = []  # List of joined players' character names.
        self.chat_scroll_offset = 0  # Scroll offset for the chat log.
        self.chat_max_scroll = 0     # Maximum scroll value (computed dynamically).
        self.last_read_message_count = 0  # How many messages have been read (once scrolled to the bottom).

        self.create_main_buttons()

    def create_main_buttons(self):
        """Creates the main set of buttons based on game state."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2

        # Always include a Chat button.
        self.buttons.append(Button((center_x, self.menu_rect.y + 100), "White", "Black", self.small_font, "Chat"))
        if not self.has_game_started:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Join Game"))
            logger.debug("Created 'Join Game' button.")
        elif self.is_current_turn and not self.in_suggest_loop:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Make Suggestion"))
            self.buttons.append(Button((center_x, self.menu_rect.y + 250), "White", "Black", self.small_font, "Make Accusation"))
            self.buttons.append(Button((center_x, self.menu_rect.y + 350), "White", "Black", self.small_font, "End Turn"))
            logger.debug("Created main game buttons for current turn.")
        elif self.is_disprover:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Disprove"))
        else:
            self.buttons.append(Button((center_x, self.menu_rect.y + 150), "White", "Black", self.small_font, "Wait...")) 

        # Add "View My Cards" button if the game has started.
        if self.has_game_started:
            self.buttons.append(Button((center_x, self.menu_rect.y + 450), "White", "Black", self.small_font, "View My Cards"))       
        self.mode = "main"

    def show_character_selection(self):
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, character in enumerate(self.available_characters):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, character))
        self.buttons.append(Button((center_x, start_y + len(self.available_characters) * spacing), "White", "Black", self.small_font, "Back"))
        self.mode = "character_selection"
        logger.debug(f"Character selection: {len(self.buttons)} buttons.")

    def show_weapon_selection(self):
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, weapon in enumerate(WEAPONS):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, weapon))
        self.buttons.append(Button((center_x, start_y + len(WEAPONS) * spacing), "White", "Black", self.small_font, "Back"))
        self.mode = "weapon_selection"
        logger.debug(f"Weapon selection: {len(self.buttons)} buttons.")

    def show_room_selection(self):
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, room in enumerate(ROOMS):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, room))
        self.buttons.append(Button((center_x, start_y + len(ROOMS) * spacing), "White", "Black", self.small_font, "Back"))
        self.mode = "room_selection"
        logger.debug(f"Room selection: {len(self.buttons)} buttons.")

    def show_disprove_selection(self):
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        for i, card in enumerate(self.disprove_cards):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, card))
        self.buttons.append(Button((center_x, start_y + len(self.disprove_cards) * spacing), "White", "Black", self.small_font, "Back"))
        self.mode = "disprove_selection"
        logger.debug(f"Disprove selection: {len(self.buttons)} buttons.")

    def show_chat_view(self):
        """Switch to chat view: shows chat log (within a box) plus Compose and Back buttons."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        self.buttons.append(Button((center_x, self.menu_rect.y + 450), "White", "Black", self.small_font, "Compose Message"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 550), "White", "Black", self.small_font, "Back"))
        self.mode = "chat_view"
        logger.debug("Switched to chat view mode.")

    def show_chat_send(self):
        """Switch to target-selection mode for chat.
        Only shows 'Broadcast' plus joined characters.
        """
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        start_y = self.menu_rect.y + 100
        spacing = 50
        options = ["Broadcast"] + self.joined_characters
        for i, target in enumerate(options):
            y_pos = start_y + i * spacing
            self.buttons.append(Button((center_x, y_pos), "White", "Black", self.small_font, target))
        self.buttons.append(Button((center_x, start_y + len(options) * spacing), "White", "Black", self.small_font, "Cancel"))
        self.mode = "chat_send"
        self.chat_input = ""
        self.selected_target = None
        logger.debug(f"Switched to chat send mode; options: {options}")

    def show_chat_compose(self):
        """Switch to message composition mode."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        self.buttons.append(Button((center_x, self.menu_rect.y + 400), "White", "Black", self.small_font, "Send"))
        self.buttons.append(Button((center_x, self.menu_rect.y + 500), "White", "Black", self.small_font, "Cancel"))
        self.mode = "chat_compose"
        self.chat_input = ""
        logger.debug(f"Switched to chat compose mode with target '{self.selected_target}'.")

    def show_card_view(self):
        """Switch to the player's card view."""
        self.buttons = []
        center_x = self.menu_rect.x + self.menu_rect.width // 2
        self.buttons.append(Button((center_x, self.menu_rect.y + 550), "White", "Black", self.small_font, "Back"))
        self.mode = "card_view"
        logger.debug("Switched to card view mode.")
        
    def process_game_state(self, user_id: int, gs: GameState):
        self.is_current_turn = user_id == gs.current_player
        self.has_game_started = gs.game_started
        self.in_suggest_loop = gs.disprover > 0
        self.is_disprover = user_id == gs.disprover
        if self.is_disprover:
            self.set_disprove_cards(gs.players[user_id].cards.intersection(set(gs.suggestion)))
        else:
            self.set_disprove_cards(set())
        if self.has_game_started:
            self.title_text = f"{gs.players[gs.current_player].character}'s Turn"
            self.available_characters = CHARACTERS
        else:
            self.available_characters = list(gs.available_characters)
            self.title_text = "Players joining..."
        # Update joined_characters from players who have assigned characters.
        self.joined_characters = [p.character.value for p in gs.players.values() if p.character is not None]
        if user_id in gs.players:
            self.player_cards = [card.value for card in gs.players[user_id].cards]
        self.redraw_buttons()

    def set_available_characters(self, available_characters):
        self.available_characters = available_characters

    def set_disprove_cards(self, cards):
        self.disprove_cards = cards

    def redraw_buttons(self):
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
        elif self.mode == "chat_view":
            self.show_chat_view()
        elif self.mode == "chat_send":
            self.show_chat_send()
        elif self.mode == "chat_compose":
            self.show_chat_compose()
        else:
            logger.debug(f"Unknown mode '{self.mode}', no buttons to redraw.")
        logger.debug(f"Buttons redrawn for mode '{self.mode}'.")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.checkForInput(mouse_pos):
                    label = button.text_input
                    logger.debug(f"Button '{label}' clicked in mode '{self.mode}'")
                    if self.mode == "main":
                        if label == "View My Cards":
                            self.show_card_view()
                        elif label == "Join Game":
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
                        elif label == "Chat":
                            self.show_chat_view()                    
                    elif self.mode == "card_view":
                        if label == "Back":
                            self.create_main_buttons()
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
                    elif self.mode == "chat_view":
                        if label == "Compose Message":
                            self.show_chat_send()
                        elif label == "Back":
                            self.create_main_buttons()
                    elif self.mode == "chat_send":
                        if label == "Cancel":
                            self.show_chat_view()
                        else:
                            self.selected_target = label
                            self.show_chat_compose()
                    elif self.mode == "chat_compose":
                        if label == "Send":
                            self.action = f"chat:{self.selected_target}:{self.chat_input}"
                            self.selected_target = None
                            self.chat_input = ""
                            self.show_chat_view()
                        elif label == "Cancel":
                            self.show_chat_view()
                    break

        if event.type == pygame.KEYDOWN:
            # Capture text input in chat compose mode.
            if self.mode == "chat_compose":
                if event.key == pygame.K_RETURN:
                    self.action = f"chat:{self.selected_target}:{self.chat_input}"
                    self.selected_target = None
                    self.chat_input = ""
                    self.show_chat_view()
                elif event.key == pygame.K_BACKSPACE:
                    self.chat_input = self.chat_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.show_chat_view()
                else:
                    self.chat_input += event.unicode
            # Use arrow keys for scrolling in chat view.
            if self.mode == "chat_view":
                if event.key == pygame.K_UP:
                    self.chat_scroll_offset = max(self.chat_scroll_offset - 1, 0)
                elif event.key == pygame.K_DOWN:
                    font = self.small_font
                    line_height = font.get_linesize()
                    visible_lines_count = 200 // line_height  # textbox_height = 200
                    self.chat_scroll_offset = min(self.chat_scroll_offset + 1, max(len(self.chat_log) - visible_lines_count, 0))
        if event.type == pygame.MOUSEWHEEL:
            if self.mode == "chat_view":
                if event.y > 0:
                    self.chat_scroll_offset = max(self.chat_scroll_offset - 1, 0)
                elif event.y < 0:
                    font = self.small_font
                    line_height = font.get_linesize()
                    visible_lines_count = 200 // line_height
                    self.chat_scroll_offset = min(self.chat_scroll_offset + 1, max(len(self.chat_log) - visible_lines_count, 0))

    def draw(self):
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect)
        header_text = self.title_text
        font_size = 60
        font = pygame.font.Font(None, font_size)
        header_width = font.size(header_text)[0]
        while header_width > self.menu_rect.width - 20 and font_size > 10:
            font_size -= 2
            font = pygame.font.Font(None, font_size)
            header_width = font.size(header_text)[0]
        header_surface = font.render(header_text, True, "white")
        header_rect = header_surface.get_rect(center=(self.menu_rect.x + self.menu_rect.width//2, self.menu_rect.y+50))
        self.screen.blit(header_surface, header_rect)

        if self.mode == "card_view":
            textbox_rect = pygame.Rect(self.menu_rect.x + 10, self.menu_rect.y + 80, self.menu_rect.width - 20, 200)
            pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 2)
            self.draw_wrapped_text(", ".join(self.player_cards), textbox_rect, self.small_font, "white")

        if self.mode == "chat_view":
            textbox_height = 200
            textbox_rect = pygame.Rect(self.menu_rect.x+10, self.menu_rect.y+80, self.menu_rect.width-20, textbox_height)
            # No background fill (transparent)
            font = self.small_font
            line_height = font.get_linesize()
            visible_lines_count = textbox_height // line_height
            # Check if we are scrolled to the bottom.
            auto_scroll = (self.chat_scroll_offset == self.chat_max_scroll)
            new_max = max(len(self.chat_log) - visible_lines_count, 0)
            self.chat_max_scroll = new_max
            if auto_scroll:
                self.chat_scroll_offset = new_max
                self.last_read_message_count = len(self.chat_log)
            # Border color: yellow if new messages exist beyond those read.
            if len(self.chat_log) > self.last_read_message_count:
                border_color = (255, 255, 0)  # Yellow
            else:
                border_color = (255, 255, 255)  # White
            pygame.draw.rect(self.screen, border_color, textbox_rect, 2)
            visible_lines = self.chat_log[self.chat_scroll_offset:self.chat_scroll_offset+visible_lines_count]
            y_offset = textbox_rect.y + 5
            for line in visible_lines:
                line_surface = font.render(line, True, (255, 255, 255))
                self.screen.blit(line_surface, (textbox_rect.x+5, y_offset))
                y_offset += line_height
        elif self.mode == "chat_compose":
            textbox_height = 100
            textbox_rect = pygame.Rect(self.menu_rect.x+10, self.menu_rect.bottom-textbox_height-10, self.menu_rect.width-20, textbox_height)
            pygame.draw.rect(self.screen, (50, 50, 50), textbox_rect)
            input_surface = self.small_font.render("Message: " + self.chat_input, True, (255, 255, 0))
            self.screen.blit(input_surface, (textbox_rect.x+5, textbox_rect.y+5))
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))
        if self.mode not in ["chat_view", "chat_compose"]:
            textbox_height = 150
            textbox_rect = pygame.Rect(self.menu_rect.x+10, self.menu_rect.bottom-textbox_height-10, self.menu_rect.width-20, textbox_height)
            pygame.draw.rect(self.screen, (255, 255, 255), textbox_rect, 2)
            self.draw_wrapped_text(self.text_message, textbox_rect, self.small_font, "white")

    def draw_wrapped_text(self, text, rect, font, color):
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
            self.screen.blit(line_surface, (rect.x+5, y_offset))
            y_offset += line_height

    def set_text(self, msg):
        self.text_message = msg
