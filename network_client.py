import socket
import json
import logging
import threading
import select
import pygame
from messages import message_from_json  # Import your message deserialization function
import sys

# Configure logger
logger = logging.getLogger("network_client")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
if len(sys.argv) > 1:
    SERVER_IP = sys.argv[1]
if len(sys.argv) > 2:
    SERVER_PORT = int(sys.argv[2])  # Convert port to an integer

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
        """
        Poll for messages from the server and post Message objects
        to the pygame event queue using a select loop with a timeout.
        """
        buffer = ""
        while self.running and self.client_socket:
            try:
                # Use select to monitor the socket for readability with a 1-second timeout
                readable, _, _ = select.select([self.client_socket], [], [], 1.0)

                if readable:
                    # Data is available on the socket
                    data = self.client_socket.recv(1024).decode()
                    if not data:
                        logger.warning("Connection to server lost.")
                        self.running = False
                        break

                    buffer += data  # Append new data to the buffer
                    while True:
                        try:
                            # Attempt to parse one complete JSON message
                            json_message = json.loads(buffer)
                            buffer = ""  # Clear the buffer after successful parsing

                            # Deserialize JSON into a Message object
                            message_object = message_from_json(json_message)

                            # Create a custom pygame event with the Message object
                            event = pygame.event.Event(pygame.USEREVENT, {"message": message_object})
                            pygame.event.post(event)
                            logger.debug(f"Posted event with Message object: {message_object}")
                        except json.JSONDecodeError:
                            # If JSON parsing fails, wait for more data
                            break
                        except Exception as e:
                            logger.error(f"Error deserializing message: {e}")
                            break
                else:
                    logger.debug("Timeout occurred")

                # Add additional operations during the 1-second timeout here if needed
                # For example: periodic updates or health checks
            except Exception as e:
                logger.error(f"Error polling server: {e}")
                self.running = False

    def send_message(self, message):
        """Send a JSON-formatted message to the server."""
        try:
            if self.client_socket:
                json_message = json.dumps(message.__dict__)
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
