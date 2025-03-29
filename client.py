import socket
import json
import sys
from defaults import Characters, Weapons, Rooms  # Import the classes from defaults.py

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

def start_client():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server")
    except Exception as e:
        print("Failed to connect to server:", e)
        sys.exit()

    user_id = 1  # Default user ID

    try:
        while True:
            # Display options for the user with current user_id
            print(f"\nCurrent User ID: {user_id}")
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
                print("Exiting client...")
                break

            elif choice == "1":
                # Modify the user ID
                try:
                    user_id = int(input("Enter new User ID: "))
                    print(f"User ID updated to {user_id}")
                except ValueError:
                    print("Invalid User ID. Please enter a valid integer.")
                    continue

            # Build the appropriate message based on user choice
            message = None

            if choice == "2":
                coordinates = input("Enter coordinates as x,y: ")
                try:
                    x, y = map(int, coordinates.split(","))
                    message = {"type": "move", "user_id": user_id, "coordinates": (x, y)}  # Sending coordinates as tuple
                except ValueError:
                    print("Invalid coordinates format. Please use x,y.")
                    continue

            elif choice == "3":
                print("\nAvailable Characters:", [char.value for char in Characters])
                character = input("Choose a character: ")
                print("\nAvailable Weapons:", [weapon.value for weapon in Weapons])
                weapon = input("Choose a weapon: ")
                print("\nAvailable Rooms:", [room.value for room in Rooms])
                room = input("Choose a room: ")
                if character in Characters.__members__.values() and weapon in Weapons.__members__.values() and room in Rooms.__members__.values():
                    message = {"type": "accusation", "user_id": user_id, "character": character, "weapon": weapon, "room": room}
                else:
                    print("Invalid selection. Please choose valid options.")
                    continue

            elif choice == "4":
                print("\nAvailable Characters:", [char.value for char in Characters])
                character = input("Choose a character: ")
                print("\nAvailable Weapons:", [weapon.value for weapon in Weapons])
                weapon = input("Choose a weapon: ")
                print("\nAvailable Rooms:", [room.value for room in Rooms])
                room = input("Choose a room: ")
                if character in Characters.__members__.values() and weapon in Weapons.__members__.values() and room in Rooms.__members__.values():
                    message = {"type": "suggestion", "user_id": user_id, "character": character, "weapon": weapon, "room": room}
                else:
                    print("Invalid selection. Please choose valid options.")
                    continue

            elif choice == "5":
                print("\nAvailable Cards:", [*Characters.__members__.values(), *Weapons.__members__.values(), *Rooms.__members__.values()])
                card = input("Choose a card: ")
                if card in Characters.__members__.values() or card in Weapons.__members__.values() or card in Rooms.__members__.values():
                    message = {"type": "disprove", "user_id": user_id, "card": card}
                else:
                    print("Invalid card. Please choose a valid card.")
                    continue

            elif choice == "6":
                reason = input("Enter error reason: ")
                message = {"type": "error", "user_id": user_id, "reason": reason}

            elif choice == "7":
                message = {"type": "end_turn", "user_id": user_id}

            elif choice == "8":
                message = {"type": "update", "user_id": user_id}

            else:
                print("Invalid choice, please try again.")
                continue

            # Send the message to the server
            try:
                json_message = json.dumps(message)
                client_socket.send(json_message.encode())
                print("Message sent to server:", json_message)
            except Exception as e:
                print("Error sending message:", e)
                break

            # Receive and process the response from the server
            try:
                response = client_socket.recv(1024).decode()
                if response:
                    try:
                        response_data = json.loads(response)
                        print("Server Response:", response_data)
                    except json.JSONDecodeError:
                        print("Invalid JSON response from server:", response)
                else:
                    print("Connection to server lost.")
                    break
            except Exception as e:
                print("Error receiving response:", e)
                break

    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
