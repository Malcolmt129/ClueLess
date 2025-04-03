import pygame
import constants
import game
from game_state import GameState
from mainMenu import MainMenu
from turnMenu import TurnMenu
from network_client import NetworkClient
from messages import (
    ErrorMessage,
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

# Initialize game components:
# running_game is your board drawing the grid/rooms.
running_game = game.Game(SCREEN)
# Pass the menu drawing area to the TurnMenu instance.
turn_menu = TurnMenu(SCREEN, "Player1", TURN_MENU_AREA)

# Initialize the network client.
client = NetworkClient()
client.connect()
client_thread = client.start()

user_id = -1
display_text = "Welcome to Clue-Less!"
game_state = GameState()

def main():
    global display_text, user_id, game_state
    running = True
    character_index = 0
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
            # running_game.handle_event(event)  # Uncomment if your board has interactivity

            if event.type == pygame.KEYDOWN:
                if running_game.current_player_index == character_index and turn_menu.action != "end":
                    if event.key == pygame.K_UP:
                        running_game.move_character('UP', character_index)
                    elif event.key == pygame.K_DOWN:
                        running_game.move_character('DOWN', character_index)
                    elif event.key == pygame.K_LEFT:
                        running_game.move_character('LEFT', character_index)
                    elif event.key == pygame.K_RIGHT:
                        running_game.move_character('RIGHT', character_index)
                else:
                    print(f"Player {running_game.current_player_index + 1}, it's not your turn yet!")

            if turn_menu.action == "end":
                print("Action: End Turn")
                # Notify the server that the turn has ended
                client.send_message(EndTurnMessage(user_id))  # Replace with your actual user_id
                turn_menu.action = None
                running_game._next_turn()

        # Draw the board on its area.
        running_game.grid_draw()
        running_game.rooms_draw()
        running_game.draw_characters()

        # Draw the turn menu in the right-hand area.
        turn_menu.draw()

        pygame.display.update()

        # Process any action that the turn menu has set.
        if turn_menu.action is not None:
            if isinstance(turn_menu.action, str):
                # Process a join message, expected in the format "join:{character}"
                if turn_menu.action.startswith("join:"):
                    parts = turn_menu.action.split(":", 1)
                    if len(parts) == 2:
                        selected_character = parts[1]
                        # Create a JoinMessage using the enum value from Characters.
                        join_message = JoinMessage(
                            user_id=user_id, 
                            character=Characters(selected_character)
                        )
                        print("Sending join message:", join_message)
                        client.send_message(join_message)
                # Process a suggestion message, expected in the format "suggest:{character}:{weapon}:{room}"
                elif turn_menu.action.startswith("suggest:"):
                    parts = turn_menu.action.split(":")
                    if len(parts) == 4:
                        _, character, weapon, room = parts
                        suggestion_message = SuggestionMessage(
                            user_id=user_id,
                            character=Characters(character),
                            weapon=Weapons(weapon),
                            room=Rooms(room)
                        )
                        print("Sending suggestion message:", suggestion_message)
                        client.send_message(suggestion_message)
                # Process an accusation message, expected in the format "accuse:{character}:{weapon}:{room}"
                elif turn_menu.action.startswith("accuse:"):
                    parts = turn_menu.action.split(":")
                    if len(parts) == 4:
                        _, character, weapon, room = parts
                        accusation_message = AccusationMessage(
                            user_id=user_id,
                            character=Characters(character),
                            weapon=Weapons(weapon),
                            room=Rooms(room)
                        )
                        print("Sending accusation message:", accusation_message)
                        client.send_message(accusation_message)
                # Process an end turn action
                elif turn_menu.action == "end":
                    end_turn_message = EndTurnMessage(user_id=user_id)
                    print("Sending end turn message:", end_turn_message)
                    client.send_message(end_turn_message)
            # Reset the action after processing.
            turn_menu.action = None

        # Optionally, update any status text in the turn menu.
        turn_menu.set_text(display_text)

    pygame.quit()

def handle_server_message(message_object):
    """Process server messages and update game state accordingly."""
    global user_id, display_text, game_state
    if isinstance(message_object, ErrorMessage):
        print(f"Error received: {message_object.reason}")
        display_text = message_object.reason
    elif isinstance(message_object, UpdateMessage):
        print(f"Game updated: {message_object}")
        display_text = message_object.msg
    elif isinstance(message_object, WelcomeMessage):
        print(
            f"Welcome Message: Assigned ID = {message_object.assigned_id}, "
            f"Available Characters = {message_object.available_characters}"
        )
        user_id = message_object.assigned_id
    elif isinstance(message_object, StartTurnMessage):
        print(f"Your turn starts, Player {message_object.user_id}")
        # TODO: Show buttons?
    elif isinstance(message_object, EndTurnMessage):
        print(f"Turn ended for Player {message_object.user_id}")
        # TODO: Show notepad?
    elif isinstance(message_object, StateUpdateMessage):
        print(f"State Update: {message_object.updates}")
        game_state = GameState.from_dict(message_object.updates)

if __name__ == "__main__":
    main()
