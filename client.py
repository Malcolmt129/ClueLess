import socket
import json
import sys
import logging
import select
from defaults import Characters, Weapons, Rooms, character_name_mapping, weapon_name_mapping, room_name_mapping

# Create logger
logger = logging.getLogger("client")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

def display_menu():
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
    print("11. Customize Characters/Weapons/Rooms")
    print("0. Exit")

def get_choice_from_list(options, mapping_dict, prompt="Choose an option by number: "):
    for index, option in enumerate(options, start=1):
        print(f"{index}. {mapping_dict.get(option, option.value)}")
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
    coordinates_str = input("Enter coordinates as x,y: ")
    try:
        x, y = map(int, coordinates_str.split(","))
        return {"type": "move", "user_id": user_id, "coordinates": (x, y)}
    except ValueError:
        logger.warning("Invalid coordinates format. Please use x,y format.")
        return None

def build_accusation_message(user_id):
    print("\nAccusation - Select a Character:")
    character = get_choice_from_list(list(Characters), character_name_mapping)
    print("\nSelect a Weapon:")
    weapon = get_choice_from_list(list(Weapons), weapon_name_mapping)
    print("\nSelect a Room:")
    room = get_choice_from_list(list(Rooms), room_name_mapping)
    return {
        "type": "accusation",
        "user_id": user_id,
        "character": character.value,
        "weapon": weapon.value,
        "room": room.value,
    }

def build_suggestion_message(user_id):
    print("\nSuggestion - Select a Character:")
    character = get_choice_from_list(list(Characters), character_name_mapping)
    print("\nSelect a Weapon:")
    weapon = get_choice_from_list(list(Weapons), weapon_name_mapping)
    print("\nSelect a Room:")
    room = get_choice_from_list(list(Rooms), room_name_mapping)
    return {
        "type": "suggestion",
        "user_id": user_id,
        "character": character.value,
        "weapon": weapon.value,
        "room": room.value,
    }

def build_disprove_message(user_id):
    print("\nDisprove - Select a Card:")
    cards = list(Characters) + list(Weapons) + list(Rooms)
    full_mapping = {**character_name_mapping, **weapon_name_mapping, **room_name_mapping}
    card = get_choice_from_list(cards, full_mapping)
    return {"type": "disprove", "user_id": user_id, "card": card.value}

def build_error_message(user_id):
    reason = input("Enter error reason: ")
    return {"type": "error", "user_id": user_id, "reason": reason}

def build_end_turn_message(user_id):
    return {"type": "end_turn", "user_id": user_id}

def build_update_message(user_id):
    return {"type": "update", "user_id": user_id}

def build_join_message(user_id, available_characters):
    if not available_characters:
        logger.warning("Available characters list not set yet.")
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

def build_custom_names_message(user_id):
    print("\nCustomize Character Names:")
    new_chars = []
    for character in Characters:
        new_name = input(f"Enter custom name for {character_name_mapping[character]}: ").strip()
        new_chars.append(new_name if new_name else character_name_mapping[character])

    print("\nCustomize Weapon Names:")
    new_weapons = []
    for weapon in Weapons:
        new_name = input(f"Enter custom name for {weapon_name_mapping[weapon]}: ").strip()
        new_weapons.append(new_name if new_name else weapon_name_mapping[weapon])

    print("\nCustomize Room Names:")
    new_rooms = []
    for room in Rooms:
        new_name = input(f"Enter custom name for {room_name_mapping[room]}: ").strip()
        new_rooms.append(new_name if new_name else room_name_mapping[room])

    return {
        "type": "custom_names",
        "user_id": user_id,
        "updates": {
            "characters": new_chars,
            "weapons": new_weapons,
            "rooms": new_rooms
        }
    }

def poll_for_messages(client_socket, available_characters):
    timeout = 0.5
    ready_to_read, _, _ = select.select([client_socket], [], [], timeout)
    if ready_to_read:
        try:
            response = client_socket.recv(10000).decode()
            if response:
                data = json.loads(response)
                logger.info("Polled message from server: %s", data)
                if data.get("type") == "welcome":
                    user_id = data.get("assigned_id")
                    available_characters = data.get("available_characters", [])
                    logger.info("Updated available characters: %s", available_characters)
                elif data.get("type") == "custom_names_update":
                    apply_custom_names(data)
                elif data.get("type") == "state_update":
                    logger.info("Received StateUpdateMessage with updates: %s", data.get("updates", {}))
                return user_id, available_characters
            else:
                logger.info("No data received; server might have closed the connection.")
        except Exception as e:
            logger.error("Error polling socket: %s", e)
    return -1, available_characters

def apply_custom_names(data):
    chars = data.get("characters", [])
    weapons = data.get("weapons", [])
    rooms = data.get("rooms", [])

    for i, name in enumerate(chars):
        if i < len(Characters):
            character_name_mapping[list(Characters)[i]] = name
    for i, name in enumerate(weapons):
        if i < len(Weapons):
            weapon_name_mapping[list(Weapons)[i]] = name
    for i, name in enumerate(rooms):
        if i < len(Rooms):
            room_name_mapping[list(Rooms)[i]] = name

def send_message(client_socket, message):
    try:
        json_message = json.dumps(message)
        client_socket.send(json_message.encode())
        logger.info("Message sent to server: %s", json_message)
    except Exception as e:
        logger.error("Error sending message: %s", e)
        return False
    return True

def receive_message(client_socket):
    try:
        response = client_socket.recv(10000).decode()
        if response:
            logger.info("Server Response: %s", response)
            data = json.loads(response)
            return data
        else:
            logger.info("Connection to server lost.")
    except Exception as e:
        logger.error("Error receiving response: %s", e)
    return None

def start_client():
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
                    logger.warning("Invalid User ID.")
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
                _, available_characters = poll_for_messages(client_socket, available_characters)
                continue
            elif choice == "11":
                message = build_custom_names_message(user_id)

            else:
                logger.warning("Invalid choice, please try again.")
                continue

            if message and send_message(client_socket, message):
                response_data = receive_message(client_socket)
                if response_data and response_data.get("type") == "welcome":
                    available_characters = response_data.get("available_characters", [])

    except KeyboardInterrupt:
        logger.info("Client shutting down...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
