import pygame
import constants
import game
from mainMenu import MainMenu
from turnMenu import TurnMenu
from network_client import NetworkClient

def main():
    # Initialize pygame and create the game window
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Clue-Less")

#Initialize the screen
pygame.init()
SCREEN = pygame.display.set_mode((constants.WIDTH,constants.HEIGHT))
pygame.display.set_caption("Clue-Less") 
CLOCK = pygame.time.Clock()
running_game = game.Game(SCREEN)

# Client init
client = NetworkClient()
client.connect()
client_thread = client.start()

    # Notify the server that a player has joined
    #client.send_message({"type": "join", "player": board.players[current_turn].name})

def main():

    running = True
    
    while running:
        SCREEN.fill("Black")
        CLOCK.tick(constants.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                # Handle custom pygame events for server messages
                server_message = event.message
                print(f"Received server message: {server_message}")
                # Process server message (update game state, etc.)
        running_game.grid_draw()
        running_game.rooms_draw()

        pygame.display.update()
    pygame.quit()

        #             # Send movement update to the server
        #             client.send_message({
        #                 "type": "move",
        #                 "player": player.name,
        #                 "room": room_name
        #             })


    
    
if __name__ == "__main__":
    mainMenu = MainMenu(SCREEN)
    mainMenu.display()

    turnMenu = TurnMenu(SCREEN, "player1")
    turnMenu.run()


    main()


    
    
