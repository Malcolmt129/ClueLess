import socket
import select
import json
import logging
from messages import (
    message_from_json,
    ErrorMessage
)
import game_logic
import traceback

# Create a module-specific logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set log level to DEBUG for detailed information

def start_server():
    game = game_logic.GameLogic()
    # game._create_fake_data()
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    server_socket.setblocking(False)
    logger.info(f"Server started at {HOST}:{PORT}")

    # Maintain a list of sockets monitored by select
    sockets_list = [server_socket]
    clients = dict()

    try:
        while not game.is_over:
            # Monitor sockets for readability
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for sock in read_sockets:
                if sock is server_socket:
                    # Handle new connections
                    client_socket, client_address = server_socket.accept()
                    logger.info(f"New connection from {client_address}")
                    client_socket.setblocking(False)
                    sockets_list.append(client_socket)
                    client_socket.sendall(game.get_welcome_message(client_address[1]).to_json_str().encode())
                    # client_socket.sendall(game.get_state_message().to_json_str().encode())
                    clients[client_address[1]] = client_socket
                else:
                    # Handle client messages
                    try:
                        data = sock.recv(1024)
                        if data:
                            decoded_data = data.decode()
                            logger.debug(f"Received from {sock.getpeername()}: {decoded_data}")
                            # Process the received JSON message using message objects
                            try:
                                msg_data = json.loads(decoded_data)
                                message = message_from_json(msg_data)
                                logger.debug(f"Message: {message}")
                                if message:
                                    outgoing_queue = game.process_message(message)
                                    logger.debug(f"Outgoing messages: {outgoing_queue}")
                                    for m in outgoing_queue:
                                        clients[m[1]].sendall(m[0].to_json_str().encode())
                                    if not game.state.game_started and message.type == 'join' and len(game.players) == MAX_CLIENTS:
                                        logger.debug("Starting game")
                                        outgoing_queue = game.start_game()
                                        for m in outgoing_queue:
                                            clients[m[1]].sendall(m[0].to_json_str().encode())
                                else:
                                    error_response = ErrorMessage(
                                        user_id=0,
                                        reason="Invalid message type or data"
                                    )
                                    sock.sendall(error_response.to_json_str().encode())
                            except json.JSONDecodeError:
                                error_response = ErrorMessage(
                                    user_id=0,
                                    reason="Invalid JSON format"
                                )
                                sock.sendall(error_response.to_json_str().encode())
                        else:
                            # Client disconnected
                            logger.info(f"Client {sock.getpeername()} disconnected")
                            sockets_list.remove(sock)
                            sock.close()
                    except Exception as e:
                        logger.error(f"Error with client {sock.getpeername()}: {e}")
                        logger.debug(traceback.format_exc())
                        sockets_list.remove(sock)
                        sock.close()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        for sock in sockets_list:
            sock.close()
        server_socket.close()
        logger.info("Server socket closed.")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5555
    MAX_CLIENTS = 2
    start_server()
