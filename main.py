import pygame
import constants
import json
import game
from game_state import GameState
from mainMenu import MainMenu
from turnMenu import TurnMenu
from customization_menu import CustomizationMenu
from network_client import NetworkClient
from messages import (
    DisproveMessage,
    ErrorMessage,
    MoveMessage,
    UpdateMessage,
    WelcomeMessage,
    StartTurnMessage,
    EndTurnMessage,
    StateUpdateMessage,
    JoinMessage,
    SuggestionMessage,
    AccusationMessage,
)
from defaults import Characters, Weapons, Rooms
import logging

# Configure logger
logger = logging.getLogger("pygame")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# For this example, assume:
# constants.WIDTH = 1200, constants.HEIGHT = 800, and constants.FPS is defined appropriately.
# Note: Adding 400 for the menu width

pygame.init()
SCREEN = pygame.display.set_mode((constants.WIDTH + 400, constants.HEIGHT))
pygame.display.set_caption("Clue-Less")
CLOCK = pygame.time.Clock()

# Define areas:
BOARD_AREA = pygame.Rect(0, 0, 800, 800)         # Left area for the board
TURN_MENU_AREA = pygame.Rect(800, 0, 400, 800)     # Right area for the turn menu

# Global variables
running_game = None
turn_menu = None
user_id = -1
game_state = GameState()
client = None

def main():
    global display_text, user_id, game_state, running_game, turn_menu, client
    running = True
    character_index = 0
       # Initialize the network client
    client = NetworkClient()
    client.connect()
    client_thread = client.start()
    # Show customization menu first
    customization_menu = CustomizationMenu(SCREEN)
    custom_names = customization_menu.run()

    if not custom_names:
        return
    
        # Initialize game components with custom names
    running_game = game.Game(SCREEN, custom_names)
    turn_menu = TurnMenu(SCREEN, TURN_MENU_AREA, running_game)

    game_state = GameState(custom_names)

    custom_names_payload = {
        "type": "custom_names",
        "user_id": user_id,
        "updates": {
            "characters": custom_names['characters'],
            "weapons": custom_names['weapons'],
            "rooms": custom_names['rooms']
        }
    }
    client.send_raw(json.dumps(custom_names_payload))

    available_characters = [
        running_game.CHARACTERS.get(c, c.value) for c in Characters
    ]
    turn_menu.set_available_characters(available_characters)
    
    while running:
        # Fill the entire screen with black.
        SCREEN.fill("Black")
        CLOCK.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                # Process custom pygame events containing server messages.
                message_object = event.message
                handle_server_message(message_object)
            # Pass events to the turn menu (and board, if needed)
            turn_menu.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if game_state.current_player == user_id and turn_menu.action != "end":
                    my_character = game_state.players[user_id].character
                    pos = running_game.characters[my_character].position
                    if event.key == pygame.K_UP:
                        new_pos = pos[0], pos[1] - 1
                    elif event.key == pygame.K_DOWN:
                        new_pos = pos[0], pos[1] + 1
                    elif event.key == pygame.K_LEFT:
                        new_pos = pos[0] - 1, pos[1]
                    elif event.key == pygame.K_RIGHT:
                        new_pos = pos[0] + 1, pos[1]
                    
                    client.send_message(MoveMessage(user_id, new_pos))
                else:
                    logger.debug(f"Player {running_game.current_player_index + 1}, it's not your turn yet!")

                # Process turn menu actions
        if turn_menu.action:
            process_turn_menu_action(turn_menu.action)
            turn_menu.action = None

        # Draw game components
        running_game.grid_draw()
        running_game.rooms_draw()
        running_game.characters_draw()
        turn_menu.draw()        
        pygame.display.update()
    pygame.quit()

def process_turn_menu_action(action):
    """Processes the action triggered by the turn menu."""
    global user_id, game_state, client, running_game

    if action.startswith("join:"):
        # Process join action
        selected_character = action.split(":", 1)[1]
        # Convert custom name back to enum for the join message
        character_enum = running_game.CHARACTERS_REVERSE[selected_character]
        join_message = JoinMessage(user_id, character_enum)
        logger.debug(f"Sending join message: {join_message}")
        client.send_message(join_message)

    elif action.startswith("suggest:"):
        # Process suggestion action
        parts = action.split(":")
        _, character, weapon, room = parts
        # Convert custom names back to enums
        character_enum = running_game.CHARACTERS_REVERSE[character]
        weapon_enum = running_game.WEAPONS_REVERSE[weapon]
        room_enum = running_game.ROOMS_REVERSE[room]
        suggestion_message = SuggestionMessage(user_id, character_enum, weapon_enum, room_enum)
        logger.debug(f"Sending suggestion message: {suggestion_message}")
        client.send_message(suggestion_message)

    elif action.startswith("accuse:"):
        # Process accusation action
        parts = action.split(":")
        _, character, weapon, room = parts
        # Convert custom names back to enums
        character_enum = running_game.CHARACTERS_REVERSE[character]
        weapon_enum = running_game.WEAPONS_REVERSE[weapon]
        room_enum = running_game.ROOMS_REVERSE[room]
        accusation_message = AccusationMessage(user_id, character_enum, weapon_enum, room_enum)
        logger.debug(f"Sending accusation message: {accusation_message}")
        client.send_message(accusation_message)

    elif action.startswith("disprove:"):
        parts = action.split(":", 1)
        if len(parts) == 2:
            card_str = parts[1]
            # Try to convert custom name back to enum
            card = None
            # Try characters first
            if card_str in running_game.CHARACTERS_REVERSE:
                card = running_game.CHARACTERS_REVERSE[card_str]
            # Try weapons
            elif card_str in running_game.WEAPONS_REVERSE:
                card = running_game.WEAPONS_REVERSE[card_str]
            # Try rooms
            elif card_str in running_game.ROOMS_REVERSE:
                card = running_game.ROOMS_REVERSE[card_str]
            else:
                logger.error(f"Could not convert custom name {card_str} back to enum")
                return
            
            disprove_message = DisproveMessage(user_id, card)
            logger.debug(f"Sending disprove message: {disprove_message}")
            client.send_message(disprove_message)

    elif action == "end":
        end_turn_message = EndTurnMessage(user_id)
        logger.debug(f"Sending end turn message: {end_turn_message}")
        client.send_message(end_turn_message)

def handle_server_message(message_object):
    global user_id, game_state, turn_menu, running_game, client

    if isinstance(message_object, ErrorMessage):
        logger.info(f"Error received: {message_object.reason}")
        turn_menu.set_text(message_object.reason)

    elif isinstance(message_object, UpdateMessage):
        msg = message_object.msg
        for enum_char in Characters:
            if str(enum_char) in msg:
                msg = msg.replace(str(enum_char), running_game.CHARACTERS[enum_char])
        logger.debug(f"Game updated: {msg}")
        turn_menu.set_text(msg)

    elif isinstance(message_object, WelcomeMessage):
        logger.info(
            f"Welcome Message: Assigned ID = {message_object.assigned_id}, "
            f"Available Characters = {message_object.available_characters}"
        )
        user_id = message_object.assigned_id
        turn_menu.user_id = user_id
        available_characters = [
            running_game.CHARACTERS.get(char, char.value) if isinstance(char, Characters) else char
            for char in message_object.available_characters
        ]
        turn_menu.set_available_characters(available_characters)

    elif isinstance(message_object, StateUpdateMessage):
        logger.debug(f"State Update: {message_object.updates}")
        custom_names = {
            'characters': {char: name for char, name in running_game.CHARACTERS.items()},
            'weapons': {weapon: name for weapon, name in running_game.WEAPONS.items()},
            'rooms': {room: name for room, name in running_game.ROOMS.items()}
        }
        game_state = GameState.from_dict(message_object.updates, custom_names)
        turn_menu.process_game_state(game_state)

    elif isinstance(message_object, dict) and message_object.get("type") == "custom_names_update":
        updated_chars = message_object.get("characters", [])
        updated_weapons = message_object.get("weapons", [])
        updated_rooms = message_object.get("rooms", [])

        # Update running_game mappings
        running_game.CHARACTERS.clear()
        running_game.CHARACTERS_REVERSE.clear()
        for enum_char, name in zip(Characters, updated_chars):
            running_game.CHARACTERS[enum_char] = name
            running_game.CHARACTERS_REVERSE[name] = enum_char

        running_game.WEAPONS.clear()
        running_game.WEAPONS_REVERSE.clear()
        for enum_weapon, name in zip(Weapons, updated_weapons):
            running_game.WEAPONS[enum_weapon] = name
            running_game.WEAPONS_REVERSE[name] = enum_weapon

        running_game.ROOMS.clear()
        running_game.ROOMS_REVERSE.clear()
        for enum_room, name in zip(Rooms, updated_rooms):
            running_game.ROOMS[enum_room] = name
            running_game.ROOMS_REVERSE[name] = enum_room

        logger.info("Custom names updated from server.")

        available_characters = [
            running_game.CHARACTERS.get(c, c.value) for c in Characters
        ]
        turn_menu.set_available_characters(available_characters)

    else:
        logger.warning(f"Unhandled message type! {type(message_object)}")

    

if __name__ == "__main__":
    main()
