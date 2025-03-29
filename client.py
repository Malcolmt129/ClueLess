import socket
import json
import sys
import logging
import select  # Imported for polling the socket
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

def start_client():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        logger.info("Connected to server")
    except Exception as e:
        logger.error("Failed to connect to server: %s", e)
        sys.exit()

    user_id = 1  # Default user ID
    available_characters = []  # This will be updated when a welcome message is received

    try:
        while True:
            # Display the current user ID and the actions menu
            logger.info(f"\nCurrent User ID: {user_id}")
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

            choice = input("Enter your choice: ")
            message = None

            if choice == "0":
                logger.info("Exiting client...")
                break

            elif choice == "1":
                # Modify the user ID
                try:
                    user_id = int(input("Enter new User ID: "))
                    logger.info(f"User ID updated to {user_id}")
                except ValueError:
                    logger.warning("Invalid User ID. Please enter a valid integer.")
                    continue

            elif choice == "9":
                # Join Game: Use the available_characters list (updated from incoming welcome messages)
                if not available_characters:
                    logger.warning("Available characters list is not set. "
                                   "Wait for a welcome message from the server first.")
                    continue
                print("\nAvailable Characters:")
                for index, char in enumerate(available_characters, start=1):
                    print(f"{index}. {char}")
                char_choice = input("Choose a character by number: ")
                try:
                    selected_character = available_characters[int(char_choice) - 1]
                    logger.info(f"Player selected character: {selected_character}")
                    join_message = {"type": "join", "user_id": user_id, "character": selected_character}
                    client_socket.send(json.dumps(join_message).encode())
                except (ValueError, IndexError):
                    logger.warning("Invalid character selection.")
                    continue

            elif choice == "10":
                # Poll Socket option: Check if there are any incoming messages without blocking.
                timeout = 0.5  # 500 ms
                ready_to_read, _, _ = select.select([client_socket], [], [], timeout)
                if ready_to_read:
                    try:
                        response = client_socket.recv(1024).decode()
                        if response:
                            try:
                                response_data = json.loads(response)
                                # If a welcome message is received, update the available characters list.
                                if response_data.get("type") == "welcome":
                                    available_characters = response_data.get("available_characters", [])
                                    logger.info("Updated available characters: %s", available_characters)
                                logger.info("Polled message from server: %s", response_data)
                            except json.JSONDecodeError:
                                logger.warning("Polled message is not valid JSON: %s", response)
                        else:
                            logger.info("No data received; server might have closed the connection.")
                    except Exception as e:
                        logger.error("Error polling the socket: %s", e)
                else:
                    logger.info("No incoming messages at this time.")
                continue  # Return to the menu without sending a new message

            elif choice == "2":
                coordinates = input("Enter coordinates as x,y: ")
                try:
                    x, y = map(int, coordinates.split(","))
                    message = {"type": "move", "user_id": user_id, "coordinates": (x, y)}
                except ValueError:
                    logger.warning("Invalid coordinates format. Please use x,y.")
                    continue

            elif choice == "3":
                # Accusation: Numbered selection for Characters, Weapons, Rooms
                print("\nAvailable Characters:")
                characters = list(Characters)
                for index, char in enumerate(characters, start=1):
                    print(f"{index}. {char.value}")
                char_choice = input("Choose a character by number: ")
                try:
                    character = characters[int(char_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid character selection.")
                    continue

                print("\nAvailable Weapons:")
                weapons = list(Weapons)
                for index, weapon in enumerate(weapons, start=1):
                    print(f"{index}. {weapon.value}")
                weapon_choice = input("Choose a weapon by number: ")
                try:
                    weapon = weapons[int(weapon_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid weapon selection.")
                    continue

                print("\nAvailable Rooms:")
                rooms = list(Rooms)
                for index, room in enumerate(rooms, start=1):
                    print(f"{index}. {room.value}")
                room_choice = input("Choose a room by number: ")
                try:
                    room = rooms[int(room_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid room selection.")
                    continue

                message = {
                    "type": "accusation",
                    "user_id": user_id,
                    "character": character.value,
                    "weapon": weapon.value,
                    "room": room.value
                }

            elif choice == "4":
                # Suggestion: Similar to Accusation
                print("\nAvailable Characters:")
                characters = list(Characters)
                for index, char in enumerate(characters, start=1):
                    print(f"{index}. {char.value}")
                char_choice = input("Choose a character by number: ")
                try:
                    character = characters[int(char_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid character selection.")
                    continue

                print("\nAvailable Weapons:")
                weapons = list(Weapons)
                for index, weapon in enumerate(weapons, start=1):
                    print(f"{index}. {weapon.value}")
                weapon_choice = input("Choose a weapon by number: ")
                try:
                    weapon = weapons[int(weapon_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid weapon selection.")
                    continue

                print("\nAvailable Rooms:")
                rooms = list(Rooms)
                for index, room in enumerate(rooms, start=1):
                    print(f"{index}. {room.value}")
                room_choice = input("Choose a room by number: ")
                try:
                    room = rooms[int(room_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid room selection.")
                    continue

                message = {
                    "type": "suggestion",
                    "user_id": user_id,
                    "character": character.value,
                    "weapon": weapon.value,
                    "room": room.value
                }

            elif choice == "5":
                # Disprove: Numbered selection from a combination of Characters, Weapons, and Rooms
                print("\nAvailable Cards:")
                cards = list(Characters) + list(Weapons) + list(Rooms)
                for index, card in enumerate(cards, start=1):
                    print(f"{index}. {card.value}")
                card_choice = input("Choose a card by number: ")
                try:
                    card = cards[int(card_choice) - 1]
                    message = {"type": "disprove", "user_id": user_id, "card": card.value}
                except (ValueError, IndexError):
                    logger.warning("Invalid card selection.")
                    continue

            elif choice == "6":
                reason = input("Enter error reason: ")
                message = {"type": "error", "user_id": user_id, "reason": reason}

            elif choice == "7":
                message = {"type": "end_turn", "user_id": user_id}

            elif choice == "8":
                message = {"type": "update", "user_id": user_id}

            else:
                logger.warning("Invalid choice, please try again.")
                continue

            # For choices other than join (choice "9") and poll (choice "10"), send the message
            if message:
                try:
                    json_message = json.dumps(message)
                    client_socket.send(json_message.encode())
                    logger.info("Message sent to server: %s", json_message)
                except Exception as e:
                    logger.error("Error sending message: %s", e)
                    break

            # Process the response from the server
            try:
                response = client_socket.recv(1024).decode()
                if response:
                    try:
                        response_data = json.loads(response)
                        # If a welcome message is received, update the available_characters list
                        if response_data.get("type") == "welcome":
                            available_characters = response_data.get("available_characters", [])
                            logger.info("Updated available characters: %s", available_characters)
                        logger.info("Server Response: %s", response_data)
                    except json.JSONDecodeError:
                        logger.warning("Invalid JSON response from server: %s", response)
                else:
                    logger.info("Connection to server lost.")
                    break
            except Exception as e:
                logger.error("Error receiving response: %s", e)
                break

    except KeyboardInterrupt:
        logger.info("Client shutting down...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
