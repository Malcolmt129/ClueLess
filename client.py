import socket
import json
import sys
import logging
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

    try:
        while True:
            # Display options for the user with current user_id
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
            print("0. Exit")

            choice = input("Enter your choice: ")

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

            # Build the appropriate message based on user choice
            message = None

            if choice == "2":
                coordinates = input("Enter coordinates as x,y: ")
                try:
                    x, y = map(int, coordinates.split(","))
                    message = {"type": "move", "user_id": user_id, "coordinates": (x, y)}  # Sending coordinates as tuple
                except ValueError:
                    logger.warning("Invalid coordinates format. Please use x,y.")
                    continue

            elif choice == "3":
                # Numbered selection for Characters
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

                # Numbered selection for Weapons
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

                # Numbered selection for Rooms
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
                # Similar process for suggestion
                print("\nAvailable Characters:")
                for index, char in enumerate(Characters, start=1):
                    print(f"{index}. {char.value}")
                char_choice = input("Choose a character by number: ")
                try:
                    character = characters[int(char_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid character selection.")
                    continue

                print("\nAvailable Weapons:")
                for index, weapon in enumerate(Weapons, start=1):
                    print(f"{index}. {weapon.value}")
                weapon_choice = input("Choose a weapon by number: ")
                try:
                    weapon = weapons[int(weapon_choice) - 1]
                except (ValueError, IndexError):
                    logger.warning("Invalid weapon selection.")
                    continue

                print("\nAvailable Rooms:")
                for index, room in enumerate(Rooms, start=1):
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
                # Numbered selection for cards (Characters, Weapons, Rooms)
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

            # Send the message to the server
            try:
                json_message = json.dumps(message)
                client_socket.send(json_message.encode())
                logger.info("Message sent to server: %s", json_message)
            except Exception as e:
                logger.error("Error sending message: %s", e)
                break

            # Receive and process the response from the server
            try:
                response = client_socket.recv(1024).decode()
                if response:
                    try:
                        response_data = json.loads(response)
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
