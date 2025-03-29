import socket
import json
import sys
import logging
import select  # For polling the socket
from defaults import Characters, Weapons, Rooms  # Import the classes from defaults.py

# Create a module-specific logger
logger = logging.getLogger("client")
logger.setLevel(logging.DEBUG)

# Configure logging to stdout
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def display_menu():
    """Display the main menu options."""
    print("\nChoose an action:")
    print("1. Change User ID")
    print("2. Move")
    print("3. Accusation")
    print("4. Suggestion")
    print("5. Disprove")
    print("6. Error")
    print("7. End Turn")
    print("8. Update")
    print("9. Join Game")
    print("10. Poll Socket")
    print("0. Exit")


def get_choice_from_list(options, prompt="Choose an option by number: "):
    """Print a numbered list of options and return the selected item."""
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option.value if hasattr(option, 'value') else option}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                logger.warning("Selection out of range. Try again.")
        except ValueError:
            logger.warning("Invalid input. Please enter a number.")


def build_move_message(user_id):
    """Prompt the user for coordinates and return a move message dictionary."""
    coordinates_str = input("Enter coordinates as x,y: ")
    try:
        x, y = map(int, coordinates_str.split(","))
        return {"type": "move", "user_id": user_id, "coordinates": (x, y)}
    except ValueError:
        logger.warning("Invalid coordinates format. Please use x,y format.")
        return None


def build_accusation_message(user_id):
    """Prompt the user for accusation details and return the message."""
    print("\nAccusation - Select a Character:")
    character = get_choice_from_list(list(Characters))
    print("\nSelect a Weapon:")
    weapon = get_choice_from_list(list(Weapons))
    print("\nSelect a Room:")
    room = get_choice_from_list(list(Rooms))
    return {
        "type": "accusation",
        "user_id": user_id,
        "character": character.value,
        "weapon": weapon.value,
        "room": room.value,
    }


def build_suggestion_message(user_id):
    """Prompt the user for suggestion details and return the message."""
    print("\nSuggestion - Select a Character:")
    character = get_choice_from_list(list(Characters))
    print("\nSelect a Weapon:")
    weapon = get_choice_from_list(list(Weapons))
    print("\nSelect a Room:")
    room = get_choice_from_list(list(Rooms))
    return {
        "type": "suggestion",
        "user_id": user_id,
        "character": character.value,
        "weapon": weapon.value,
        "room": room.value,
    }


def build_disprove_message(user_id):
    """Prompt the user for a card selection for disproving and return the message."""
    print("\nDisprove - Select a Card:")
    cards = list(Characters) + list(Weapons) + list(Rooms)
    card = get_choice_from_list(cards)
    return {"type": "disprove", "user_id": user_id, "card": card.value}


def build_error_message(user_id):
    """Prompt for an error reason and return an error message dictionary."""
    reason = input("Enter error reason: ")
    return {"type": "error", "user_id": user_id, "reason": reason}


def build_end_turn_message(user_id):
    """Return an end-turn message dictionary."""
    return {"type": "end_turn", "user_id": user_id}


def build_update_message(user_id):
    """Return an update message dictionary."""
    return {"type": "update", "user_id": user_id}


def build_join_message(user_id, available_characters):
    """Display available characters and prompt user to choose one for joining the game."""
    if not available_characters:
        logger.warning(
            "Available characters list is not set. Wait for a welcome message from the server first."
        )
        return None
    print("\nJoin Game - Available Characters:")
    for index, char in enumerate(available_characters, start=1):
        print(f"{index}. {char}")
    try:
        choice = int(input("Choose a character by number: "))
        selected_character = available_characters[choice - 1]
        return {"type": "join", "user_id": user_id, "character": selected_character}
    except (ValueError, IndexError):
        logger.warning("Invalid character selection.")
        return None


def poll_for_messages(client_socket: socket.socket, available_characters: list) -> list:
    """
    Poll the socket for incoming messages without blocking.
    If a message is received and is a welcome message, update available_characters.
    Returns the updated available_characters list.
    """
    timeout = 0.5  # 500 ms timeout
    ready_to_read, _, _ = select.select([client_socket], [], [], timeout)
    if ready_to_read:
        try:
            response = client_socket.recv(1024).decode()
            if response:
                data = json.loads(response)
                logger.info("Polled message from server: %s", data)
                if data.get("type") == "welcome":
                    user_id = data.get("assigned_id")
                    available_characters = data.get("available_characters", [])
                    logger.info("Updated available characters: %s", available_characters)
                return user_id, available_characters
            else:
                logger.info("No data received; server might have closed the connection.")
        except Exception as e:
            logger.error("Error polling the socket: %s", e)
    else:
        logger.info("No incoming messages at this time.")
    return -1, available_characters


def send_message(client_socket, message):
    """Send a JSON-formatted message over the socket."""
    try:
        json_message = json.dumps(message)
        client_socket.send(json_message.encode())
        logger.info("Message sent to server: %s", json_message)
    except Exception as e:
        logger.error("Error sending message: %s", e)
        return False
    return True


def receive_message(client_socket):
    """Receive a JSON-formatted message from the server."""
    try:
        response = client_socket.recv(1024).decode()
        if response:
            data = json.loads(response)
            logger.info("Server Response: %s", data)
            return data
        else:
            logger.info("Connection to server lost.")
    except Exception as e:
        logger.error("Error receiving response: %s", e)
    return None


def start_client():
    """Main client loop."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        logger.info("Connected to server")
    except Exception as e:
        logger.error("Failed to connect to server: %s", e)
        sys.exit()

    user_id, available_characters = poll_for_messages(client_socket, [])

    try:
        while True:
            logger.info(f"\nCurrent User ID: {user_id}")
            display_menu()

            choice = input("Enter your choice: ").strip()
            message = None

            if choice == "0":
                logger.info("Exiting client...")
                break

            elif choice == "1":
                try:
                    user_id = int(input("Enter new User ID: "))
                    logger.info(f"User ID updated to {user_id}")
                except ValueError:
                    logger.warning("Invalid User ID. Please enter a valid integer.")
                    continue

            elif choice == "2":
                message = build_move_message(user_id)

            elif choice == "3":
                message = build_accusation_message(user_id)

            elif choice == "4":
                message = build_suggestion_message(user_id)

            elif choice == "5":
                message = build_disprove_message(user_id)

            elif choice == "6":
                message = build_error_message(user_id)

            elif choice == "7":
                message = build_end_turn_message(user_id)

            elif choice == "8":
                message = build_update_message(user_id)

            elif choice == "9":
                message = build_join_message(user_id, available_characters)
                if message is None:
                    continue

            elif choice == "10":
                # Call the separate function to poll the socket.
                _, available_characters = poll_for_messages(client_socket, available_characters)
                continue

            else:
                logger.warning("Invalid choice, please try again.")
                continue

            if message and send_message(client_socket, message):
                # Upon sending, wait for and process the response.
                response_data = receive_message(client_socket)
                if response_data and response_data.get("type") == "welcome":
                    available_characters = response_data.get("available_characters", [])
                    logger.info("Updated available characters: %s", available_characters)

    except KeyboardInterrupt:
        logger.info("Client shutting down due to keyboard interrupt...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
