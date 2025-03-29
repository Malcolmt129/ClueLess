import socket
import select
import json
from messages import (
    message_from_json,
    ErrorMessage
)
from game_state import GameState
import traceback

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5555         # Port number
MAX_CLIENTS = 6     # Maximum number of clients

def start_server(game: GameState):
    game = GameState()
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    server_socket.setblocking(False)
    print(f"Server started at {HOST}:{PORT}")

    # Maintain a list of sockets monitored by select
    sockets_list = [server_socket]

    try:
        while True:
            # Monitor sockets for readability
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for sock in read_sockets:
                if sock is server_socket:
                    # Handle new connections
                    client_socket, client_address = server_socket.accept()
                    print(f"New connection from {client_address}")
                    client_socket.setblocking(False)
                    sockets_list.append(client_socket)
                else:
                    # Handle client messages
                    try:
                        data = sock.recv(1024)
                        if data:
                            decoded_data = data.decode()
                            print(f"Received from {sock.getpeername()}: {decoded_data}")
                            # Process the received JSON message using message objects
                            try:
                                msg_data = json.loads(decoded_data)
                                message = message_from_json(msg_data)
                                print('Message: {}'.format(message))
                                if message:
                                    outgoing_queue = game.process_message(message)
                                    print('Outgoing messages: {}'.format(outgoing_queue))
                                    sock.sendall(message.to_json_str().encode())
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
                            print(f"Client {sock.getpeername()} disconnected")
                            sockets_list.remove(sock)
                            sock.close()
                    except Exception as e:
                        print(f"Error with client {sock.getpeername()}: {e}")
                        traceback.print_exc()
                        sockets_list.remove(sock)
                        sock.close()
    except KeyboardInterrupt:
        print("Server shutting down...")
        for sock in sockets_list:
            sock.close()
    finally:
        server_socket.close()

if __name__ == "__main__":
    # TODO: Load data from database or perform any startup initializations if required
    start_server()
