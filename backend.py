import socket
import select

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5555        # Port number
MAX_CLIENTS = 6     # Maximum number of clients

def start_server():
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    server_socket.setblocking(False)
    print(f"Server started at {HOST}:{PORT}")

    # Maintain a list of sockets for `select`
    sockets_list = [server_socket]

    try:
        while True:
            # Monitor sockets for readiness
            read_sockets, _, _ = select.select(sockets_list, [], [])

            for sock in read_sockets:
                if sock == server_socket:
                    # Handle new connections
                    client_socket, client_address = server_socket.accept()
                    print(f"New connection from {client_address}")
                    client_socket.setblocking(False)
                    sockets_list.append(client_socket)
                    # TODO: Send join message with avaliable characters
                else:
                    # Handle client messages
                    try:
                        data = sock.recv(1024)
                        if data:
                            print(f"Received from {sock.getpeername()}: {data.decode()}")
                            # Echo the message back to the client
                            sock.sendall(data)
                        else:
                            # Remove disconnected clients
                            print(f"Client {sock.getpeername()} disconnected")
                            sockets_list.remove(sock)
                            sock.close()
                    except Exception as e:
                        print(f"Error with client {sock.getpeername()}: {e}")
                        sockets_list.remove(sock)
                        sock.close()

    except KeyboardInterrupt:
        print("Server shutting down...")
        for sock in sockets_list:
            sock.close()
    finally:
        server_socket.close()

if __name__ == "__main__":
    # TODO: Load from database
    start_server()
