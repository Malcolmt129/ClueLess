import socket
import select
import json
import logging
import struct
import sys
import time
import traceback
from messages import message_from_json, ErrorMessage, ChatMessage, MessageTypes, StateUpdateMessage
import game_logic

# Create a module-specific logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Use DEBUG for more detailed information if needed

def handle_chat_message(sender_sock, message, clients):
    """
    Process a ChatMessage received from a client.
    If a target is provided, send the message directly to that client.
    Otherwise, broadcast to all connected clients (except the sender).
    """
    sender_id = sender_sock.getpeername()[1]  # Using the client's port number as its identifier.
    payload = message.to_json_str()

    if message.target:
        # Direct message: send only to the client with the specified target id.
        if message.target in clients:
            try:
                clients[message.target].sendall(payload.encode())
                logger.info(f"Direct chat from {sender_id} to {message.target}: {message.content}")
            except Exception as e:
                logger.error(f"Error sending direct chat from {sender_id} to {message.target}: {e}")
        else:
            error_response = ErrorMessage(user_id=message.user_id, reason=f"Target {message.target} not found")
            try:
                sender_sock.sendall(error_response.to_json_str().encode())
            except Exception as e:
                logger.error(f"Error sending error message to {sender_id}: {e}")
            logger.warning(f"Direct chat target {message.target} not found for sender {sender_id}")
    else:
        # Broadcast message: send to every client except the sender.
        for client_id, client_sock in clients.items():
            if client_id != sender_id:
                try:
                    client_sock.sendall(payload.encode())
                except Exception as e:
                    logger.error(f"Error broadcasting chat message to {client_id}: {e}")
        logger.info(f"Broadcast chat from {sender_id}: {message.content}")

def start_server():
    game = game_logic.GameLogic()
    # game._create_fake_data()

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    linger_enabled = 1
    linger_time = 10  # This is in seconds.
    linger_struct = struct.pack('ii', linger_enabled, linger_time)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    server_socket.setblocking(False)
    logger.info(f"Server started at {HOST}:{PORT}")

    # Maintain a list of sockets monitored by select
    sockets_list = [server_socket]
    clients = dict()  # Maps client identifiers (using their port number) to their sockets

    try:
        while not game.is_over:
            # Monitor sockets for readability
            read_sockets, _, _ = select.select(sockets_list, [], [], 1.0)
            for sock in read_sockets:
                if sock is server_socket:
                    # Handle new connections
                    client_socket, client_address = server_socket.accept()
                    logger.info(f"New connection from {client_address}")
                    client_socket.setblocking(False)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
                    sockets_list.append(client_socket)
                    # Send a welcome message using game logic; use client's port as identifier.
                    welcome_message = game.get_welcome_message(client_address[1])
                    client_socket.sendall(welcome_message.to_json_str().encode())
                    clients[client_address[1]] = client_socket
                else:
                    # Handle client messages from an already connected client
                    try:
                        data = sock.recv(1024)
                        if data:
                            decoded_data = data.decode()
                            logger.debug(f"Received from {sock.getpeername()}: {decoded_data}")
                            try:
                                msg_data = json.loads(decoded_data)
                                message = message_from_json(msg_data)
                                logger.debug(f"Message deserialized: {message}")
                                
                                # If the message is a chat message, process it separately.
                                if message.type == MessageTypes.CHAT:
                                    handle_chat_message(sock, message, clients)
                                    continue

                                # Otherwise, process it as a game-related message.
                                outgoing_queue = game.process_message(message)
                                logger.debug(f"Outgoing messages from game logic: {outgoing_queue}")
                                for m in outgoing_queue:
                                    try:
                                        target_client = clients[m[1]]
                                        target_client.sendall(m[0].to_json_str().encode())
                                        time.sleep(0.1)
                                    except Exception as send_err:
                                        logger.error(f"Error sending message to client {m[1]}: {send_err}")
                                if message.type == MessageTypes.JOIN:
                                    if (not game.state.game_started) and len(game.players) == MAX_CLIENTS:
                                        logger.debug("All players joined. Starting game.")
                                        outgoing_queue = game.start_game()
                                    else:
                                        outgoing_queue = [(StateUpdateMessage(0, game.state.to_dict()), client_id) for client_id, _ in clients.items()]
                                    logger.debug(f"Outgoing messages from join: {outgoing_queue}")
                                    for m in outgoing_queue:
                                        time.sleep(0.1)
                                        try:
                                            clients[m[1]].sendall(m[0].to_json_str().encode())
                                        except Exception as send_err:
                                            logger.error(f"Error sending start game message to client {m[1]}: {send_err}")
                            except json.JSONDecodeError:
                                error_response = ErrorMessage(user_id=0, reason="Invalid JSON format")
                                sock.sendall(error_response.to_json_str().encode())
                        else:
                            # Client disconnected
                            logger.info(f"Client {sock.getpeername()} disconnected")
                            sockets_list.remove(sock)
                            sock.close()
                    except Exception as e:
                        logger.error(f"Error with client {sock.getpeername()}: {e}")
                        logger.debug(traceback.format_exc())
                        if sock in sockets_list:
                            sockets_list.remove(sock)
                        sock.close()
    except KeyboardInterrupt:
        logger.info("Server shutting down due to keyboard interrupt...")
    finally:
        for sock in sockets_list:
            sock.close()
        server_socket.close()
        logger.info("Server socket closed.")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5555
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
    MAX_CLIENTS = 3
    start_server()
