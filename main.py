import pygame
import constants
from board import Board
#import client

def main():
    # Initialize pygame and create the game window
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Clue-Less")

    clock = pygame.time.Clock()
    board = Board()

    # Track the current player's turn
    current_turn = 0

    # Notify the server that a player has joined
    #client.send_message({"type": "join", "player": board.players[current_turn].name})

    while board.running:
       
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         board.running = False
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         x, y = pygame.mouse.get_pos()
        #         moved = board.move_player(current_turn, x, y)

        #         if moved:
        #             player = board.players[current_turn]
        #             room_name = board.get_player_room(current_turn)

        #             # Send movement update to the server
        #             client.send_message({
        #                 "type": "move",
        #                 "player": player.name,
        #                 "room": room_name
        #             })

        #             # Advance turn to the next player
        #             current_turn = (current_turn + 1) % len(board.players)

        #             # Notify server of the new player's turn
        #             client.send_message({
        #                 "type": "turn",
        #                 "player": board.players[current_turn].name
        #             })

        # screen.fill(constants.BLACK)
        # board.grid_draw(screen)
        # board.rooms_draw(screen)
        # pygame.display.update()
        # clock.tick(constants.FPS)

        board.handle_events()  
        board.draw_board()  
        board.draw_characters()  

        pygame.display.flip() 
        clock.tick(constants.FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
