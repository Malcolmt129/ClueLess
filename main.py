import pygame
import constants
import game
from game_state import GameState
from mainMenu import MainMenu
from turnMenu import TurnMenu
from network_client import NetworkClient
from messages import (
    DisproveMessage,
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

                # Process turn menu actions
        if turn_menu.action:
            process_turn_menu_action(turn_menu.action, character_index)
            turn_menu.action = None

        # Draw game components
        running_game.grid_draw()
        running_game.rooms_draw()
        running_game.draw_characters()
        turn_menu.draw()        
        pygame.display.update()
    pygame.quit()

def process_turn_menu_action(action, character_index):
    """Processes the action triggered by the turn menu."""
    global user_id, game_state

    if action.startswith("join:"):
        # Process join action
        selected_character = action.split(":", 1)[1]
        join_message = JoinMessage(
            user_id=user_id,
            character=Characters(selected_character)
        )
        print(f"Sending join message: {join_message}")
        client.send_message(join_message)

    elif action.startswith("suggest:"):
        # Process suggestion action
        parts = action.split(":")
        _, character, weapon, room = parts
        suggestion_message = SuggestionMessage(
            user_id=user_id,
            character=Characters(character),
            weapon=Weapons(weapon),
            room=Rooms(room)
        )
        print(f"Sending suggestion message: {suggestion_message}")
        client.send_message(suggestion_message)

    elif action.startswith("accuse:"):
        # Process accusation action
        parts = action.split(":")
        _, character, weapon, room = parts
        accusation_message = AccusationMessage(
            user_id=user_id,
            character=Characters(character),
            weapon=Weapons(weapon),
            room=Rooms(room)
        )
        print(f"Sending accusation message: {accusation_message}")
        client.send_message(accusation_message)

    elif action.startswith("disprove:"):
        parts = action.split(":", 1)
        if len(parts) == 2:
            card_str = parts[1]
            # Try to cast the card string to the appropriate enum.
            try:
                card = Characters(card_str)
            except ValueError:
                try:
                    card = Weapons(card_str)
                except ValueError:
                    card = Rooms(card_str)
            disprove_message = DisproveMessage(
                user_id=user_id,
                card=card
            )
            print("Sending disprove message:", disprove_message)
            client.send_message(disprove_message)

    elif action == "end":
        end_turn_message = EndTurnMessage(user_id=user_id)
        print(f"Sending end turn message: {end_turn_message}")
        client.send_message(end_turn_message)
        running_game._next_turn()

def handle_server_message(message_object):
    """Process server messages and update game state accordingly."""
    global user_id, game_state, turn_menu
    if isinstance(message_object, ErrorMessage):
        print(f"Error received: {message_object.reason}")
        turn_menu.set_text(message_object.reason)
    elif isinstance(message_object, UpdateMessage):
        print(f"Game updated: {message_object}")
        turn_menu.set_text(message_object.msg)
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
        # Update turn menu information
        print(f"Your info: {game_state.players[user_id]}")
        # me = game_state.players[user_id]
        # me.character
        # # board.draw_me_at(me.position)
        turn_menu.set_disprove_cards(game_state.players[user_id].cards)
        for player in game_state.players.values():
            print(f"{player.character} is at {player.position}")
            # TODO: Update board positions  
        if game_state.current_player == user_id:
            print("It is your turn!")
        else:
            print("It is NOT your turn!")

if __name__ == "__main__":
    main()
