import pygame
import constants
from board import Board



def main():

    #Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((constants.HEIGHT,constants.WIDTH))
    pygame.display.set_caption("Clue-Less") 

    clock = pygame.time.Clock()
    board = Board()
    running = True

    while running:

        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(constants.BLACK) 
        board.grid_draw(screen)
        board.rooms_draw(screen)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
