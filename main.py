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
    MoveMessage,
    UpdateMessage,
    WelcomeMessage,
    StartTurnMessage,
    EndTurnMessage,
    StateUpdateMessage,
    JoinMessage,
    SuggestionMessage,
    AccusationMessage,
    ChatMessage
)
from defaults import Characters, Weapons, Rooms
import logging

# Configure logger
logger = logging.getLogger("pygame")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize pygame and create screen.
pygame.init()
SCREEN = pygame.display.set_mode((constants.WIDTH + 400, constants.HEIGHT))
pygame.display.set_caption("Clue-Less")
CLOCK = pygame.time.Clock()

# Define drawing areas.
BOARD_AREA = pygame.Rect(0, 0, 800, 800)
TURN_MENU_AREA = pygame.Rect(800, 0, 400, 800)

# Initialize game components.
running_game = game.Game(SCREEN)
turn_menu = TurnMenu(SCREEN, TURN_MENU_AREA)

# Initialize the network client.
client = NetworkClient()
client.connect()
client_thread = client.start()

user_id = -1
game_state = GameState()

def main():
    global user_id, game_state
    running = True
    while running:
        SCREEN.fill("Black")
        CLOCK.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.USEREVENT:
                # Process custom events containing server messages.
                message_object = event.message
                handle_server_message(message_object)

            # Let the turn menu handle its own events.
            turn_menu.handle_event(event)

            # Process game movement keys when it's your turn.
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    if game_state.current_player == user_id and turn_menu.action != "end":
                        my_character = game_state.players[user_id].character
                        pos = running_game.characters[my_character].position
                        if event.key == pygame.K_UP:
                            new_pos = (pos[0], pos[1] - 1)
                        elif event.key == pygame.K_DOWN:
                            new_pos = (pos[0], pos[1] + 1)
                        elif event.key == pygame.K_LEFT:
                            new_pos = (pos[0] - 1, pos[1])
                        elif event.key == pygame.K_RIGHT:
                            new_pos = (pos[0] + 1, pos[1])
                        else:
                            new_pos = pos
                        client.send_message(MoveMessage(user_id, new_pos))
                    else:
                        logger.debug("Not your turn or invalid action.")

        # Process turn menu actions.
        if turn_menu.action:
            # The new chat interface will eventually set an action in the format:
            #    "chat:<target>:<message>"
            if turn_menu.action.startswith("chat:"):
                process_turn_menu_action(turn_menu.action)
            else:
                process_turn_menu_action(turn_menu.action)
            turn_menu.action = None

        # Draw game components.
        running_game.grid_draw()
        running_game.rooms_draw()
        running_game.characters_draw()
        turn_menu.draw()

        pygame.display.update()
    pygame.quit()


def process_turn_menu_action(action):
    global user_id, game_state
    if action.startswith("join:"):
        selected_character = action.split(":", 1)[1]
        join_message = JoinMessage(user_id, Characters(selected_character))
        logger.debug(f"Sending join message: {join_message}")
        client.send_message(join_message)
    elif action.startswith("suggest:"):
        parts = action.split(":")
        _, character, weapon, room = parts
        suggestion_message = SuggestionMessage(user_id, Characters(character), Weapons(weapon), Rooms(room))
        logger.debug(f"Sending suggestion message: {suggestion_message}")
        client.send_message(suggestion_message)
    elif action.startswith("accuse:"):
        parts = action.split(":")
        _, character, weapon, room = parts
        accusation_message = AccusationMessage(user_id, Characters(character), Weapons(weapon), Rooms(room))
        logger.debug(f"Sending accusation message: {accusation_message}")
        client.send_message(accusation_message)
    elif action.startswith("disprove:"):
        parts = action.split(":", 1)
        if len(parts) == 2:
            card_str = parts[1]
            try:
                card = Characters(card_str)
            except ValueError:
                try:
                    card = Weapons(card_str)
                except ValueError:
                    card = Rooms(card_str)
            disprove_message = DisproveMessage(user_id, card)
            logger.debug("Sending disprove message: %s", disprove_message)
            client.send_message(disprove_message)
    elif action == "end":
        end_turn_message = EndTurnMessage(user_id)
        logger.debug(f"Sending end turn message: {end_turn_message}")
        client.send_message(end_turn_message)
    elif action.startswith("chat:"):
        # Expected format: "chat:<target>:<message>"
        parts = action.split(":", 2)
        if len(parts) < 3:
            logger.warning("Invalid chat action format.")
            return
        target_str = parts[1]
        content = parts[2]
        chat_message = None
        if target_str.lower() == "broadcast":
            chat_message = ChatMessage(user_id, content, target=None)
        else:
            # Iterate over game_state.players.items() to get (uid, Player) pairs.
            for uid, p in game_state.players.items():
                # Assuming each player object has a 'character' attribute.
                if p.character.value == target_str:
                    chat_message = ChatMessage(user_id, content, target=uid)
                    break
        if chat_message:
            client.send_message(chat_message)
            logger.info(f"Sent chat message: target={target_str}, content={content}")
            turn_menu.chat_log.append(f"ME: {content}")
        else:
            logger.warning(f"Invalid message target={target_str}")



def handle_server_message(message_object):
    global user_id, game_state
    if isinstance(message_object, ErrorMessage):
        logger.info(f"Error received: {message_object.reason}")
        turn_menu.set_text(message_object.reason)
    elif isinstance(message_object, UpdateMessage):
        logger.debug(f"Game updated: {message_object}")
        turn_menu.set_text(message_object.msg)
    elif isinstance(message_object, WelcomeMessage):
        logger.info(
            f"Welcome Message: Assigned ID = {message_object.assigned_id}, "
            f"Available Characters = {message_object.available_characters}"
        )
        user_id = message_object.assigned_id
        turn_menu.set_available_characters(message_object.available_characters)
    elif isinstance(message_object, StateUpdateMessage):
        logger.debug(f"State Update: {message_object.updates}")
        game_state = GameState.from_dict(message_object.updates)
        if user_id in game_state.players:
            logger.debug(f"Your info: {game_state.players[user_id]}")
        else:
            logger.debug("Got StateUpdate before you joined!")
        turn_menu.process_game_state(user_id, game_state)
        for character in game_state.positions:
            logger.info(f"{character} is at {game_state.positions[character]}")
            running_game.characters[character].position = game_state.positions[character]
        if game_state.current_player == user_id:
            logger.info("It is your turn!")
        else:
            logger.info("It is NOT your turn!")
    elif isinstance(message_object, ChatMessage):
        # Use the character name if available; otherwise, default to "Player {user_id}".
        sender_name = f"Player {message_object.user_id}"
        if game_state is not None and message_object.user_id in game_state.players:
            sender_character = game_state.players[message_object.user_id].character
            if sender_character is not None:
                sender_name = sender_character.value
        chat_line = f"{sender_name}: {message_object.content}"
        turn_menu.chat_log.append(chat_line)
        logger.info(f"Chat received: {chat_line}")
    else:
        logger.warning(f"Unhandled message type! {type(message_object)}")


if __name__ == "__main__":
    main()
