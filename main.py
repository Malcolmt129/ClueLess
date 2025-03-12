import pygame
import constants
from board import Board

def main():
    # Initialize pygame and create the game window
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Clue-Less")

    clock = pygame.time.Clock()
    board = Board()

    while board.running:
        board.handle_events()  
        board.draw_board()  
        board.draw_characters()  

        pygame.display.flip()  
        clock.tick(constants.FPS)  

    pygame.quit()

if __name__ == "__main__":
    main()
