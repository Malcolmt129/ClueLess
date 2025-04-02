import socket
import json
import logging
import threading
import pygame

# Configure logger
logger = logging.getLogger("network_client")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

class NetworkClient:
    def __init__(self):
        self.client_socket = None
        self.running = True

    def connect(self):
        """Connect to the server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            logger.info("Connected to server!")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.client_socket = None

    def poll_server(self):
        """Poll for messages from the server and post them to the pygame event queue."""
        buffer = ""
        while self.running and self.client_socket:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    logger.info("Connection to server lost.")
                    self.running = False
                    break

                buffer += data  # Append data to the buffer
                while True:
                    try:
                        # Attempt to parse one complete JSON message
                        json_message = json.loads(buffer)
                        buffer = ""  # Clear the buffer after successful parsing

                        # Create a custom pygame event with the server message
                        event = pygame.event.Event(pygame.USEREVENT, {"message": json_message})
                        pygame.event.post(event)
                        logger.info(f"Posted event: {json_message}")
                    except json.JSONDecodeError:
                        # If JSON parsing fails, wait for more data
                        break
            except Exception as e:
                logger.error(f"Error polling server: {e}")
                self.running = False

    def send_message(self, message):
        """Send a JSON-formatted message to the server."""
        try:
            if self.client_socket:
                json_message = json.dumps(message)
                self.client_socket.send(json_message.encode())
                logger.info(f"Sent message: {json_message}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    def stop(self):
        """Stop the client and close the connection."""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
            logger.info("Connection closed.")

    def start(self):
        """Start the client in a separate thread."""
        thread = threading.Thread(target=self.poll_server, daemon=True)
        thread.start()
        logger.info("Client thread started.")
        return thread
