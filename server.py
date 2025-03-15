import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
#storing the solution envelope in the backend
#compared to the accusation json message received, to determine if accusation is correct
solution_envelope = {
    "person": "mustard",
    "room": "bathroom",
    "weapon": "revolver"
}
    
current_player = 0
clients = []
#this function sends a json message to all  clients
#except for a particular specified client
def broadcast_to_all_others(client_socket,encoded_json):
    global clients
    for client in clients:
        if(client!=client_socket):
              client.send(encoded_json)

#this function handleds messages received from clients
def handle_client(client_socket, address):
    print(f"Client connected: {address}")
    global clients
    global current_player
    while True:
        data = client_socket.recv(1024)
        if not data:
            print('Client disconnected')            
            clients.remove(client_socket)
            return
        message = json.loads(data.decode())
        print(message)
        if clients[current_player] != client_socket:
            print('Player attempting to play out of order')
            client_socket.send(json.dumps( {"type":"error","description":"Not your turn" }).encode())
            continue
        message_type = message.get("type")
        #if the message is of 'accusation' type
        if(message_type=="accusation"):
            #compare accusation message to solution envelope
            if(message.get("person") == solution_envelope.get("person")
               and
              message.get("room") == solution_envelope.get("room") 
              and 
              message.get("weapon") == solution_envelope.get("weapon")):
                #if accusation is correct,send an accusation response message to clients
                accusation_correct_resp = {"type":"accusation_response","correct":"true","player_id":""+str(address[1])}
                #send accusation response message with the player id of the original player that made the accusation included
                #send this accusation response message with player id included, to all clients that did not make the accusation
                #player id is included because other clients need to know which client this message is referring to   
                broadcast_to_all_others(client_socket,json.dumps(accusation_correct_resp).encode())
                #sends the accusation response message without the player id included, to the client that made the accusation in the first place
                #sends accusation message response without the player id, because the accuser client aldready knows that the message refers to them
                accusation_correct_resp.pop("player_id",None)
                client_socket.send(json.dumps(accusation_correct_resp).encode())

            else:
                #this is the response sent if the accusationn is incorrect
                accusation_incorrect_resp = {"type":"accusation_response","correct":"false","player_id":""+str(address[1])}
                #the accusation response with the player id included is sent to all clients who didnt make the accusation
                broadcast_to_all_others(client_socket,json.dumps(accusation_incorrect_resp).encode())
                accusation_incorrect_resp.pop("player_id",None)
                #the accusation response without the player id included is sent to the client that made the accusation
                client_socket.send(json.dumps(accusation_incorrect_resp).encode())
        
        elif(message_type=="suggestion"):
            suggestion_response = { "type": "sugggestion_response","player_id":""+str(address[1])}
            #the suggestion response with the player id included is sent to all client that didnt make the suggestion
            broadcast_to_all_others(client_socket,json.dumps(suggestion_response).encode())
            suggestion_response.pop("player_id",None)
            #the suggestion response without the player id is sent to the client that made the suggestion
            client_socket.send(json.dumps(suggestion_response).encode())

        elif(message_type=="move"):
            move_response = { "type": "move_response","coordinate":""+str(message.get("coordinate")),"player_id":""+str(address[1])}
            move_response["row"] = message.get("row")
            move_response["col"] = message.get("col")
            #the move response with the player id included is sent to all clients that didn't send the move message
            broadcast_to_all_others(client_socket,json.dumps(move_response).encode())
            move_response.pop("player_id",None)
            #the move response without the player id included is sent to the client that sent the move message
            client_socket.send(json.dumps(move_response).encode())

        elif(message_type=="join"):
            join_response = { "type": "join_response","character":""+str(message.get("character")),"player_id":""+str(address[1])}
            broadcast_to_all_others(client_socket,json.dumps(join_response).encode())
            join_response.pop("player_id",None)
            client_socket.send(json.dumps(join_response).encode())

        elif(message_type=="disprove"):
            disprove_response = { "type": "disprove_response","card":""+str(message.get("card")),"player_id":""+str(address[1])}
            broadcast_to_all_others(client_socket,json.dumps(disprove_response).encode())
            disprove_response.pop("player_id",None)
            client_socket.send(json.dumps(disprove_response).encode())

        elif(message_type=="end_turn"):
            client_socket.send(json.dumps( {"type":"end_turn_response","success": True }).encode())
            current_player = (current_player + 1) % len(clients)
            clients[current_player].send(json.dumps( {"type":"start_turn" }).encode())

           
        data = solution_envelope
        data["current_player"] = current_player
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)  # `indent` makes the file human-readable
            print('Writing game state to file')  

print('Loading game state to file') 
# Reading from a JSON file
try:
    with open('data.json', 'r') as file:
        loaded_data = json.load(file)
    current_player = loaded_data.get("current_player")
    print("Data loaded:")
    print(loaded_data)
except FileNotFoundError:
    print('No database found. Starting new game.')

while True:
    client_socket, address = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, address)).start()