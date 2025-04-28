import pygame
from button import Button, ButtonFactory

class CustomizationMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.running = True
        self.buttons = []
        self.input_boxes = []
        self.input_texts = []  # Store text for each input box
        self.active_input = None  # Track which input box is active
        self.custom_names = {
            'characters': [],
            'weapons': [],
            'rooms': []
        }
        self.current_category = 'characters'
        self.default_names = {
            'characters': ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"],
            'weapons': ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"],
            'rooms': ["KITCHEN", "BALLROOM", "CONSERVATORY", "DINING ROOM", "BILLIARD ROOM", "LIBRARY", "LOUNGE", "HALL", "STUDY"]
        }
        # Initialize custom_names with default values
        for category in self.default_names:
            self.custom_names[category] = self.default_names[category].copy()
        
        # Scrolling variables
        self.scroll_y = 0
        self.scroll_speed = 20
        self.max_visible_items = 6  # Maximum number of items visible at once
        self.create_ui()

    def create_ui(self):
        # Title
        title = self.title_font.render("Customize Game Names", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 50))
        
        # Category buttons and Done button at the top
        char_btn = ButtonFactory.create_button(
            (200, 150),
            baseColor="White",
            hovering_color="Gray",
            font=self.font,
            text_input="Characters"
        )
        weapon_btn = ButtonFactory.create_button(
            (400, 150),
            baseColor="White",
            hovering_color="Gray",
            font=self.font,
            text_input="Weapons"
        )
        room_btn = ButtonFactory.create_button(
            (600, 150),
            baseColor="White",
            hovering_color="Gray",
            font=self.font,
            text_input="Rooms"
        )
        
        # Done button moved to top
        done_btn = ButtonFactory.create_button(
            (700, 150),
            baseColor="Green",
            hovering_color="Dark Green",
            font=self.font,
            text_input="Done"
        )
        
        self.buttons.extend([char_btn, weapon_btn, room_btn, done_btn])
        
        # Create input boxes for current category
        self.update_input_boxes()

    def update_input_boxes(self):
        """Update input boxes for the current category"""
        self.input_boxes = []
        self.input_texts = []
        
        # Calculate how many items to show based on category
        items_to_show = min(len(self.custom_names[self.current_category]), self.max_visible_items)
        
        for i in range(items_to_show):
            input_box = pygame.Rect(200, 250 + i*60, 400, 40)
            self.input_boxes.append(input_box)
            # Get the correct item based on scroll position
            item_index = i + (self.scroll_y // 60)
            if item_index < len(self.custom_names[self.current_category]):
                self.input_texts.append(self.custom_names[self.current_category][item_index])
            else:
                self.input_texts.append("")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check if clicking on input boxes
            for i, box in enumerate(self.input_boxes):
                if box.collidepoint(pos):
                    self.active_input = i
                    break
            else:
                self.active_input = None
                
            # Check if clicking on buttons
            for i, button in enumerate(self.buttons):
                if button.checkForInput(pos):
                    if i == 0:  # Characters button
                        # Save current changes before switching
                        for j, text in enumerate(self.input_texts):
                            item_index = j + (self.scroll_y // 60)
                            if item_index < len(self.custom_names[self.current_category]):
                                self.custom_names[self.current_category][item_index] = text
                        self.current_category = 'characters'
                        self.scroll_y = 0
                        self.update_input_boxes()
                    elif i == 1:  # Weapons button
                        # Save current changes before switching
                        for j, text in enumerate(self.input_texts):
                            item_index = j + (self.scroll_y // 60)
                            if item_index < len(self.custom_names[self.current_category]):
                                self.custom_names[self.current_category][item_index] = text
                        self.current_category = 'weapons'
                        self.scroll_y = 0
                        self.update_input_boxes()
                    elif i == 2:  # Rooms button
                        # Save current changes before switching
                        for j, text in enumerate(self.input_texts):
                            item_index = j + (self.scroll_y // 60)
                            if item_index < len(self.custom_names[self.current_category]):
                                self.custom_names[self.current_category][item_index] = text
                        self.current_category = 'rooms'
                        self.scroll_y = 0
                        self.update_input_boxes()
                    elif i == 3:  # Done button
                        # Save final changes and exit
                        for j, text in enumerate(self.input_texts):
                            item_index = j + (self.scroll_y // 60)
                            if item_index < len(self.custom_names[self.current_category]):
                                self.custom_names[self.current_category][item_index] = text
                        self.running = False
                        return self.custom_names
                        
        elif event.type == pygame.KEYDOWN:
            if self.active_input is not None:
                if event.key == pygame.K_RETURN:
                    # Move to next box
                    self.active_input = (self.active_input + 1) % len(self.input_boxes)
                elif event.key == pygame.K_BACKSPACE:
                    self.input_texts[self.active_input] = self.input_texts[self.active_input][:-1]
                else:
                    self.input_texts[self.active_input] += event.unicode
                    
        elif event.type == pygame.MOUSEWHEEL:
            # Handle scrolling
            if self.current_category == 'rooms':  # Only allow scrolling for rooms
                max_scroll = max(0, (len(self.custom_names['rooms']) - self.max_visible_items) * 60)
                new_scroll = self.scroll_y - event.y * self.scroll_speed
                self.scroll_y = max(0, min(new_scroll, max_scroll))
                self.update_input_boxes()

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title = self.title_font.render("Customize Game Names", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)
        
        # Draw category buttons and Done button
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.draw(self.screen, (70, 70, 70))
            
        # Draw input boxes
        for i, box in enumerate(self.input_boxes):
            color = (255, 255, 255) if i == self.active_input else (200, 200, 200)
            pygame.draw.rect(self.screen, color, box, 2)
            text_surface = self.font.render(self.input_texts[i], True, (255, 255, 255))
            self.screen.blit(text_surface, (box.x + 5, box.y + 5))
            
        # Draw current category
        category_text = self.font.render(f"Current Category: {self.current_category.capitalize()}", True, (255, 255, 255))
        self.screen.blit(category_text, (200, 200))
        
        # Draw scroll indicator for rooms
        if self.current_category == 'rooms':
            total_items = len(self.custom_names['rooms'])
            if total_items > self.max_visible_items:
                # Draw scroll bar
                scroll_bar_height = (self.max_visible_items / total_items) * 300
                scroll_bar_y = 250 + (self.scroll_y / (total_items * 60)) * 300
                pygame.draw.rect(self.screen, (100, 100, 100), (620, 250, 20, 300))
                pygame.draw.rect(self.screen, (200, 200, 200), (620, scroll_bar_y, 20, scroll_bar_height))
        
        # Draw instructions
        instructions = [
            "Modify the existing names for each category",
            "Press Enter to move to next box",
            "Use mouse wheel to scroll through rooms",
            "Click Done when all changes are complete"
        ]
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (200, 600 + i*30))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                self.handle_event(event)
            self.draw()
        return self.custom_names 
