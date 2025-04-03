import pygame
import constants
import game
from mainMenu import MainMenu
from turnMenu import TurnMenu
from network_client import NetworkClient
from messages import ErrorMessage, UpdateMessage, WelcomeMessage, StartTurnMessage, EndTurnMessage, StateUpdateMessage

# For this example, assume:
# constants.WIDTH = 1200, constants.HEIGHT = 800, constants.FPS is defined appropriately
# Note: Adding 400 for the menu width

pygame.init()
SCREEN = pygame.display.set_mode((constants.WIDTH+400, constants.HEIGHT))
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

def main():
    running = True

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
            # running_game.handle_event(event)  # If your board has interactivity

        # Draw the board on its area.
        running_game.grid_draw()
        running_game.rooms_draw()

        # Draw the turn menu in the right-hand area.
        turn_menu.draw()

        pygame.display.update()

        # Process any action that the turn menu has set.
        if turn_menu.action is not None:
            if turn_menu.action == "suggest":
                print("Action: Make Suggestion")
                # Insert suggestion handling logic here.
                turn_menu.action = None  # Reset after processing
            elif turn_menu.action == "accuse":
                print("Action: Make Accusation")
                # Insert accusation handling logic.
                turn_menu.action = None
            elif turn_menu.action == "end":
                print("Action: End Turn")
                # Notify the server that the turn has ended.
                client.send_message(EndTurnMessage(user_id))  # Replace with your actual user_id
                turn_menu.action = None

    pygame.quit()

def handle_server_message(message_object):
    """Process server messages and update game state accordingly."""
    if isinstance(message_object, ErrorMessage):
        print(f"Error received: {message_object.reason}")
    elif isinstance(message_object, UpdateMessage):
        print(f"Game updated: {message_object}")
    elif isinstance(message_object, WelcomeMessage):
        print(f"Welcome Message: Assigned ID = {message_object.assigned_id}, Available Characters = {message_object.available_characters}")
        global user_id
        user_id = message_object.assigned_id
    elif isinstance(message_object, StartTurnMessage):
        print(f"Your turn starts, Player {message_object.user_id}")
    elif isinstance(message_object, EndTurnMessage):
        print(f"Turn ended for Player {message_object.user_id}")
    elif isinstance(message_object, StateUpdateMessage):
        print(f"State Update: {message_object.updates}")

if __name__ == "__main__":
    main()
