import socket
import threading
import sys
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server")
except Exception as e:
    print("Failed to connect to server:", e)
    sys.exit()

# Function to handle server messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            try:
                data = json.loads(message)
                print("Server:", data)
            except json.JSONDecodeError:
                print("Received non-JSON message:", message)
        except:
            print("Disconnected from server")
            break

# Start a thread to listen for messages from the server
threading.Thread(target=receive_messages, daemon=True).start()

# Function to send messages to the server
def send_message(data):
    try:
        json_message = json.dumps(data)
        client_socket.send(json_message.encode())
    except Exception as e:
        print("Error sending message:", e)

if __name__ == "__main__":
    send_message({"type": "join", "player": "Player1"})
