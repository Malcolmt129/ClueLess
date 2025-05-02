import socket
import select
import json
import logging
import struct
import sys
import time
import traceback

from messages import (
    message_from_json,
    ErrorMessage
)
import game_logic
import defaults  # import your default mappings (important!)

# Create a module-specific logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def start_server():
    game = game_logic.GameLogic()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    linger_enabled = 1
    linger_time = 10
    linger_struct = struct.pack('ii', linger_enabled, linger_time)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    server_socket.setblocking(False)
    logger.info(f"Server started at {HOST}:{PORT}")

    sockets_list = [server_socket]
    clients = dict()

    try:
        while not game.is_over:
            read_sockets, _, _ = select.select(sockets_list, [], [], 1.0)
            if read_sockets:
                for sock in read_sockets:
                    if sock is server_socket:
                        client_socket, client_address = server_socket.accept()
                        logger.info(f"New connection from {client_address}")
                        client_socket.setblocking(False)
                        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
                        sockets_list.append(client_socket)
                        client_socket.sendall(game.get_welcome_message(client_address[1]).to_json_str().encode())
                        clients[client_address[1]] = client_socket
                    else:
                        try:
                            data = sock.recv(1024)
                            if data:
                                decoded_data = data.decode()
                                logger.debug(f"Received from {sock.getpeername()}: {decoded_data}")

                                try:
                                    msg_data = json.loads(decoded_data)
                                    message = message_from_json(msg_data)
                                    logger.debug(f"Message: {message}")

                                    if message:
                                        # ✨ MODIFIED - Changed from 'custom_names' to check state_update with custom fields
                                        if message.type == 'state_update' and 'custom_characters' in message.updates:
                                            logger.info(f"Custom names update received from {message.user_id}")

                                            # ✨ MODIFIED - Get updates directly from message instead of msg_data
                                            updates = message.updates
                                            update_custom_names(updates)

                                            # Broadcast to everyone
                                            broadcast_custom_names(clients)
                                        else:
                                            outgoing_queue = game.process_message(message)
                                            logger.debug(f"Outgoing messages: {outgoing_queue}")
                                            for m in outgoing_queue:
                                                logger.debug(f"Sending message: {m}")
                                                # ✨ MODIFIED - Added error handling for disconnected clients
                                                if m[1] in clients:
                                                    clients[m[1]].sendall(m[0].to_json_str().encode())
                                                    time.sleep(0.1)

                                        # Auto-start game remains unchanged
                                        if not game.state.game_started and message.type == 'join' and len(
                                                game.players) == MAX_CLIENTS:
                                            logger.debug("Starting game")
                                            outgoing_queue = game.start_game()
                                            for m in outgoing_queue:
                                                time.sleep(0.1)
                                                if m[1] in clients:  # Added safety check
                                                    clients[m[1]].sendall(m[0].to_json_str().encode())

                                    else:
                                        error_response = ErrorMessage(user_id=0, reason="Invalid message type or data")
                                        sock.sendall(error_response.to_json_str().encode())

                                except json.JSONDecodeError:
                                    error_response = ErrorMessage(user_id=0, reason="Invalid JSON format")
                                    sock.sendall(error_response.to_json_str().encode())
                            else:
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

# ✨ New server-side helper functions ✨
def update_custom_names(updates):
    if 'characters' in updates:
        for i, name in enumerate(updates['characters']):
            enum_member = list(defaults.Characters)[i]
            defaults.character_name_mapping[enum_member] = name
    if 'weapons' in updates:
        for i, name in enumerate(updates['weapons']):
            enum_member = list(defaults.Weapons)[i]
            defaults.weapon_name_mapping[enum_member] = name
    if 'rooms' in updates:
        for i, name in enumerate(updates['rooms']):
            enum_member = list(defaults.Rooms)[i]
            defaults.room_name_mapping[enum_member] = name

def broadcast_custom_names(clients):
    message = {
        "type": "custom_names_update",
        "characters": list(defaults.character_name_mapping.values()),
        "weapons": list(defaults.weapon_name_mapping.values()),
        "rooms": list(defaults.room_name_mapping.values())
    }
    for client_socket in clients.values():
        try:
            client_socket.sendall(json.dumps(message).encode())
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error broadcasting custom names: {e}")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5555
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = sys.argv[2]
    MAX_CLIENTS = 3
    start_server()
